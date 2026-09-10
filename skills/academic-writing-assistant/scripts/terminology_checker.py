#!/usr/bin/env python3
"""Local terminology clues, without merging distinct research concepts.

A --map file replaces bundled suggestions. Author-confirmed definitions and
preferences take priority. English matching uses configured literal variants,
word boundaries and optional case sensitivity, not semantic equivalence.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from check_utils import configure_cli_streams, markdown_text, read_input
from prose_utils import mask_prose

DEFAULT_MAP = Path(__file__).resolve().parents[1] / 'assets' / 'terminology-map.zh-en.json'
RELATIONS = {'equivalent', 'style_preference', 'related_concepts'}


def validate_entry(entry: Any, field: str, index: int) -> dict:
    where = f'Terminology map field {field!r}, entry {index}'
    if not isinstance(entry, dict):
        raise ValueError(where + ' must be an object.')
    item = dict(entry)
    for key in ('recommended_zh', 'en', 'note'):
        if not isinstance(item.get(key), str) or not item[key].strip():
            raise ValueError(where + f': {key} must be a non-empty string.')
    for key in ('author_confirmed', 'case_sensitive'):
        if key in item and not isinstance(item[key], bool):
            raise ValueError(where + f': {key} must be a boolean.')
        item.setdefault(key, False)
    for key in ('variants_zh', 'variants_en'):
        if key == 'variants_en' and key not in item:
            continue
        variants = item.get(key)
        if not isinstance(variants, list) or not all(isinstance(v, str) and v.strip() for v in variants):
            raise ValueError(where + f': {key} must be an array of non-empty strings.')
        item[key] = list(dict.fromkeys(v.strip() for v in variants))
        if len(item[key]) < 2:
            raise ValueError(where + f': {key} needs at least two distinct variants.')
        if key == 'variants_en' and not item['case_sensitive'] and len({v.casefold() for v in item[key]}) != len(item[key]):
            raise ValueError(where + ': variants_en differ only in case; set case_sensitive=true.')
    if item['recommended_zh'] not in item['variants_zh']:
        raise ValueError(where + ': recommended_zh must be one of variants_zh.')
    if 'recommended_en' in item and (not isinstance(item['recommended_en'], str) or item['recommended_en'] not in item.get('variants_en', [])):
        raise ValueError(where + ': recommended_en must be one of variants_en.')
    item.setdefault('relation_source', 'explicit' if 'relation' in item else 'legacy_style_default')
    if not isinstance(item['relation_source'], str) or item['relation_source'] not in {'explicit', 'legacy_style_default'}:
        raise ValueError(where + ': relation_source is not recognized.')
    item.setdefault('relation', 'style_preference')
    if not isinstance(item['relation'], str) or item['relation'] not in RELATIONS:
        raise ValueError(where + ': relation must be equivalent, style_preference, or related_concepts.')
    all_variants = item['variants_zh'] + item.get('variants_en', [])
    if 'preferred' in item:
        if not isinstance(item['preferred'], str) or item['preferred'] not in all_variants:
            raise ValueError(where + ': preferred must be a configured variant.')
        if not item['author_confirmed']:
            raise ValueError(where + ': preferred requires author_confirmed=true.')
    if 'definitions' in item:
        definitions = item['definitions']
        if not isinstance(definitions, dict) or not all(isinstance(k, str) and k in all_variants and isinstance(v, str) and v.strip() for k, v in definitions.items()):
            raise ValueError(where + ': definitions must map configured variants to non-empty strings.')
    item['field'] = field
    return item


def unique_mapping(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate terminology map key: ' + key)
        result[key] = value
    return result


def load_terms(path: Path = DEFAULT_MAP) -> List[Dict[str, Any]]:
    """Load a replacement glossary; do not merge it with bundled preferences."""
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=unique_mapping)
    except RecursionError:
        raise ValueError('Terminology map nesting exceeds parser limits.') from None
    if not isinstance(data, dict):
        raise ValueError('Terminology map must be an object of field arrays.')
    if '_meta' in data and not isinstance(data['_meta'], dict):
        raise ValueError('Terminology map _meta must be an object.')
    terms = []
    for field, entries in data.items():
        if field.startswith('_'):
            continue
        if not isinstance(entries, list):
            raise ValueError(f'Terminology map field {field!r} must be an array.')
        terms.extend(validate_entry(entry, field, index) for index, entry in enumerate(entries))
    if not terms:
        raise ValueError('Terminology map has no term entries.')
    return terms


def read_text(path: Optional[str]) -> str:
    return read_input(path)


def variant_pattern(variant: str) -> str:
    left = r'(?<![A-Za-z0-9_])' if variant[0].isascii() and variant[0].isalnum() else ''
    right = r'(?![A-Za-z0-9_])' if variant[-1].isascii() and variant[-1].isalnum() else ''
    return left + re.escape(variant) + right


def scan_terms(text: str, terms: Iterable[dict], language: str = 'both') -> tuple:
    if language not in {'zh', 'en', 'both'}:
        raise ValueError('language must be zh, en, or both.')
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Input must be non-empty text.')
    prose, warnings, excluded = mask_prose(text)
    newline_offsets = [-1] + [i for i, char in enumerate(text) if char == '\n']
    findings = []
    for index, raw_entry in enumerate(terms):
        field = raw_entry.get('field', 'general') if isinstance(raw_entry, dict) else 'general'
        if not isinstance(field, str):
            raise ValueError('Term entry field must be a string.')
        entry = validate_entry(raw_entry, field, index)
        for selected in ('zh', 'en') if language == 'both' else (language,):
            variants = entry.get('variants_' + selected, [])
            if not variants:
                continue
            ordered = sorted(variants, key=lambda value: (-len(value), variants.index(value)))
            pattern = re.compile('|'.join('(?P<v' + str(i) + '>' + variant_pattern(v) + ')' for i, v in enumerate(ordered)), 0 if entry['case_sensitive'] else re.IGNORECASE)
            counts, occurrences = {}, []
            for match in pattern.finditer(prose):
                variant = ordered[int(match.lastgroup[1:])]
                counts[variant] = counts.get(variant, 0) + 1
                line = bisect.bisect_left(newline_offsets, match.start())
                occurrences.append({'variant': variant, 'raw': text[match.start():match.end()], 'start': match.start(), 'end': match.end(), 'line': line,
                                    'column': match.start() - newline_offsets[line - 1], 'context': text[max(0, match.start() - 50):min(len(text), match.end() + 50)]})
            related = entry['relation'] == 'related_concepts'
            preferred = entry.get('preferred') if entry['author_confirmed'] else None
            preference_mismatch = not related and preferred in variants and any(variant != preferred for variant in counts)
            if len(counts) < 2 and not preference_mismatch:
                continue
            dominant = max(counts, key=counts.get)
            recommended = '' if related else preferred if preferred in variants else entry.get('recommended_' + selected, dominant)
            findings.append({'type': 'author_preference_mismatch' if preference_mismatch else 'variant_cooccurrence', 'field': field, 'found': counts, 'dominant': dominant, 'recommended': recommended,
                             'english': entry['en'], 'note': entry['note'], 'relation': entry['relation'], 'relation_source': entry['relation_source'],
                             'language': selected, 'priority': 'author_confirmed' if entry['author_confirmed'] else 'map_suggestion',
                             'action': 'preserve_distinction' if related else 'review_consistency' if entry['relation'] == 'equivalent' else 'optional_style_review',
                             'requires_review': not related, 'occurrences': occurrences, 'definitions': entry.get('definitions', {}), 'coverage': 'configured_variants_only'})
    return findings, warnings, excluded


def find_inconsistencies(text: str, terms: Iterable[Dict[str, Any]], language: str = 'both') -> List[Dict[str, Any]]:
    return scan_terms(text, terms, language)[0]


def format_counts(found: Dict[str, int]) -> str:
    return ' / '.join(f'{variant}（{count} 次）' for variant, count in sorted(found.items(), key=lambda pair: (-pair[1], pair[0])))


def render_markdown(findings: List[Dict[str, Any]]) -> str:
    lines = ['# Terminology Consistency Report', '']
    if not findings:
        lines.extend(['No configured variant groups co-occur in this text.', '', '仅检查所选词表的字面变体；未发现共现不代表全文术语或概念已验证。'])
        return '\n'.join(lines) + '\n'
    lines.extend([f'Found {len(findings)} terminology review/info item(s); co-occurrence alone is not an error.', '',
                  '| 领域 | 变体与次数 | 关系 | 建议用法 | 处理 | English | 说明 |', '|---|---|---|---|---|---|---|'])
    for finding in findings:
        values = [finding['field'], format_counts(finding['found']), finding['relation'], finding['recommended'] or '保留概念区分', finding['action'], finding['english'], finding['note']]
        lines.append('| ' + ' | '.join(markdown_text(value) for value in values) + ' |')
    lines.extend(['', '作者已确认术语与研究定义优先。related_concepts 表示可能不同的概念，应保留区分；equivalent 和 style_preference 也只提示核对，不自动替换。英文仅匹配配置形式，默认忽略大小写并使用词边界，不推断词形变化或语义。JSON 给出原文位置。'])
    return '\n'.join(lines) + '\n'


def main(argv: Optional[Sequence[str]] = None) -> int:
    configure_cli_streams()
    parser = argparse.ArgumentParser(description='Report configured terminology variants without merging distinct concepts.')
    parser.add_argument('file', nargs='?', help='UTF-8 file; stdin when omitted or -.')
    parser.add_argument('--map', default=str(DEFAULT_MAP), help='Replacement glossary JSON; author definitions take priority over bundled suggestions.')
    parser.add_argument('--language', choices=['zh', 'en', 'both'], default='both', help='English requires configured variants_en.')
    parser.add_argument('--json', action='store_true', help='Emit the backward-compatible findings list with additional fields.')
    parser.add_argument('--strict', action='store_true', help='Exit 1 for consistency/style review or incomplete extraction; related concepts alone are informational.')
    args = parser.parse_args(argv)
    try:
        text, glossary = read_text(args.file), load_terms(Path(args.map))
        findings, warnings, _ = scan_terms(text, glossary, args.language)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        sys.stderr.write(f'Cannot check terminology input: {exc}\n')
        return 2
    sys.stdout.write(json.dumps(findings, ensure_ascii=False, indent=2) + '\n' if args.json else render_markdown(findings))
    if warnings:
        sys.stderr.write('Coverage incomplete: ' + '; '.join(warning['reason'] for warning in warnings[:5]) + '\n')
    return 1 if args.strict and (warnings or any(f['requires_review'] for f in findings)) else 0


if __name__ == '__main__':
    raise SystemExit(main())
