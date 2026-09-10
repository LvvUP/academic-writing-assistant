#!/usr/bin/env python3
"""Compare recognized protected content with source locations and coverage limits.

Uses a non-executing lexical scanner, never a LaTeX compiler. A clean result is
limited to recognized tokens. Semantic claim/evidence relationships still need
human or Agent review. Default exit behavior remains advisory; --strict returns
1 for differences or insufficient coverage, and input errors always return 2.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from check_utils import configure_cli_streams
from fidelity_parser import CATEGORIES, extract_document, sentence_spans

LABELS = {
    'citations': 'LaTeX citation keys and commands',
    'bracket_citations': 'Bracket citations [n]',
    'author_year_citations': 'Author-year citations',
    'cross_references': '\\ref / \\label types and targets',
    'structural_references': 'Section / Table / Figure references',
    'math_blocks': 'Math blocks',
    'numbers': 'Numeric values, relations and recognized units',
    'named_entities': 'Dataset / model / benchmark names',
    'custom_macros': 'Custom macros and explicit arguments',
}
PREVIEW_LIMIT = 12


def read_text(path: str) -> str:
    text = sys.stdin.read() if path == '-' else Path(path).read_text(encoding='utf-8-sig')
    return text.removeprefix('\ufeff')


def extract_numbers(text: str) -> List[str]:
    """Compatibility helper: values now include recognized signs/units/relations."""
    return [item['value'] for item in extract_document(text).items['numbers']]


def extract_math(text: str) -> List[str]:
    return [item['value'] for item in extract_document(text).items['math_blocks']]


def extract_citation_keys(text: str) -> List[str]:
    return [item['key'] for item in extract_document(text).items['citations']]


def extract_macros(text: str) -> List[str]:
    return [item['value'] for item in extract_document(text).items['custom_macros']]


def extract_named_entities(text: str) -> List[str]:
    return [item['value'] for item in extract_document(text).items['named_entities']]


def compare(before: List[str], after: List[str]) -> Dict:
    """Multiset comparison retaining every missing/added occurrence."""
    left, right = Counter(before), Counter(after)
    return {
        'before_count': len(before), 'after_count': len(after),
        'missing': sorted((left - right).elements()),
        'added': sorted((right - left).elements()),
    }


def association_map(text: str, items: Dict[str, List[dict]]) -> dict:
    """Map stable prose skeletons to their protected values, with positions.

    Exact skeleton matches identify mechanical reassignments, including moving a
    citation to another unchanged claim. Rephrased/ambiguous contexts are not
    semantic proof and are explicitly outside this comparison's coverage.
    """
    by_sentence = defaultdict(list)
    for category, occurrences in items.items():
        for occurrence in occurrences:
            by_sentence[occurrence['sentence_id']].append(occurrence)
    result = defaultdict(list)
    for sentence_id, (start, end) in enumerate(sentence_spans(text)):
        occurrences = sorted(by_sentence[sentence_id], key=lambda item: (item['start'], item['end']))
        chars = list(text[start:end])
        for item in occurrences:
            for offset in range(max(item['start'], start), min(item['end'], end)):
                chars[offset - start] = ' '
        # Punctuation and whitespace alone do not identify a claim. Preserve
        # letter/digit labels outside protected spans rather than treating all
        # sentences as interchangeable.
        skeleton = re.sub(r'[^\w\u4e00-\u9fff]+', ' ', ''.join(chars)).lower().strip()
        if not skeleton:
            continue
        values = {category: [item['value'] for item in occurrences if item['category'] == category]
                  for category in CATEGORIES}
        result[skeleton].append({'start': start, 'end': end,
                                 'context': text[start:end].strip()[:300], 'values': values})
    return result


def context_differences(before: str, after: str, left: dict, right: dict) -> dict:
    changes = {name: [] for name in CATEGORIES}
    before_map, after_map = association_map(before, left), association_map(after, right)
    anchored_counts = {name: 0 for name in CATEGORIES}
    for skeleton in before_map.keys() & after_map.keys():
        before_contexts, after_contexts = before_map[skeleton], after_map[skeleton]
        for category in CATEGORIES:
            before_values = [tuple(item['values'][category]) for item in before_contexts]
            after_values = [tuple(item['values'][category]) for item in after_contexts]
            # A whole sentence/paragraph reorder with its values intact is safe.
            # Multisets of associations permit that without masking value swaps.
            if Counter(before_values) == Counter(after_values):
                anchored_counts[category] += sum(len(values) for values in before_values)
            else:
                changes[category].append({
                    'kind': 'association_changed',
                    'before': [{key: item[key] for key in ('start', 'end', 'context')}
                               | {'values': item['values'][category]} for item in before_contexts],
                    'after': [{key: item[key] for key in ('start', 'end', 'context')}
                              | {'values': item['values'][category]} for item in after_contexts],
                    'note': 'Protected items differ beside matching prose; confirm the intended claim/evidence association.',
                })
    for category in CATEGORIES:
        before_values = [item['value'] for item in left[category]]
        after_values = [item['value'] for item in right[category]]
        if (before_values != after_values and Counter(before_values) == Counter(after_values)
                and anchored_counts[category] < len(before_values) and not changes[category]):
            changes[category].append({
                'kind': 'unresolved_sequence_change',
                'before': [{'start': item['start'], 'end': item['end'], 'context': item['context'], 'values': [item['value']]} for item in left[category]],
                'after': [{'start': item['start'], 'end': item['end'], 'context': item['context'], 'values': [item['value']]} for item in right[category]],
                'note': 'The occurrence order changed outside stable prose anchors (for example, table cells); verify associations manually.',
            })
    return changes


def build_report(before: str, after: str) -> Dict[str, Dict]:
    left, right = extract_document(before), extract_document(after)
    contexts = context_differences(before, after, left.items, right.items)
    report: Dict[str, Dict] = {}
    for category in CATEGORIES:
        before_items, after_items = left.items[category], right.items[category]
        data = compare([item['value'] for item in before_items], [item['value'] for item in after_items])
        data.update(before_items=before_items, after_items=after_items,
                    context_changes=contexts[category])
        data['status'] = ('REVIEW_NEEDED' if data['missing'] or data['added'] or data['context_changes']
                          else 'UNCHANGED_WITHIN_COVERAGE' if before_items or after_items
                          else 'NOT_CHECKED_NO_ITEMS')
        report[category] = data
    differences = any(data['status'] == 'REVIEW_NEEDED' for data in report.values())
    insufficient = any(item.coverage['status'] == 'INSUFFICIENT' for item in (left, right))
    report['_meta'] = {
        'schema_version': 2,
        'status': 'REVIEW_NEEDED' if differences else 'INSUFFICIENT' if insufficient else 'UNCHANGED_WITHIN_COVERAGE',
        'coverage_insufficient': insufficient,
        'before_coverage': left.coverage, 'after_coverage': right.coverage,
        'semantic_review_required': True,
        'association_scope': 'Exact unchanged prose contexts only; rephrased claims and semantic evidence support require separate review.',
        'normalization': 'Width-folded digits/punctuation; Unicode minus, E/e and numeric thousands separators; escaped percent; equivalent comparison glyphs; math layout whitespace excluding text arguments/control-word boundaries. No unit conversion or rounding.',
        'offset_unit': 'Unicode code points, zero-based start and exclusive end; lines/columns are one-based.',
    }
    return report


def safe_text(value: object) -> str:
    """Escape original material for Markdown and raw-HTML renderers."""
    text = html.escape(str(value), quote=False).replace('\n', ' ').replace('\r', ' ')
    return re.sub(r'([\\`*_{}\[\]()#+!|>~])', r'\\\1', text)


def render(report: Dict[str, Dict]) -> Tuple[str, bool]:
    meta = report.get('_meta', {})
    categories = [(name, data) for name, data in report.items() if not name.startswith('_')]
    problems = [(name, data) for name, data in categories
                if data['missing'] or data['added'] or data.get('context_changes')]
    insufficient = meta.get('coverage_insufficient', not any(data['before_count'] for _, data in categories))
    clean = not problems and not insufficient
    lines = ['# Fidelity Check Report', '']
    if problems:
        lines.append('Status: REVIEW NEEDED — recognized protected items or their local associations differ.')
    elif insufficient:
        lines.append('Status: INSUFFICIENT — no differences found in recognized items, but coverage is insufficient.')
    else:
        total = sum(data['before_count'] for _, data in categories)
        lines.append(f'Status: PASS (recognized scope only) — no differences found among {total} recognized protected items.')
    lines.extend(['', 'This does not verify full semantic fidelity or claim strength. Rephrased claim/evidence associations, unrecognized units/names and external or expanded LaTeX content require human/Agent review.'])
    if insufficient:
        lines.extend(['', '## Coverage limitations', ''])
        for side in ('before', 'after'):
            coverage = meta.get(side + '_coverage', {})
            for warning in coverage.get('warnings', [])[:PREVIEW_LIMIT]:
                lines.append(f'- {side}, offset {warning["start"]}: {safe_text(warning["detail"])}')
    for name, data in problems:
        lines.extend(['', f'## {LABELS.get(name, name)}', '',
                      f'Before: {data["before_count"]} · After: {data["after_count"]}', ''])
        for key, title, item_key in [('missing', 'Missing from revised text', 'before_items'),
                                     ('added', 'Present only in revised text', 'after_items')]:
            if not data[key]:
                continue
            lines.append(title + ':')
            lookup = defaultdict(list)
            for item in data.get(item_key, []):
                lookup[item['value']].append(item)
            for value in data[key][:PREVIEW_LIMIT]:
                location = lookup[value].pop(0) if lookup[value] else None
                suffix = f' (line {location["line"]}, column {location["column"]})' if location else ''
                lines.append('- ' + safe_text(value) + suffix)
                if location:
                    lines.append('  Context: ' + safe_text(location['context']))
            if len(data[key]) > PREVIEW_LIMIT:
                lines.append(f'- … and {len(data[key]) - PREVIEW_LIMIT} more occurrences (see JSON).')
        for change in data.get('context_changes', [])[:PREVIEW_LIMIT]:
            lines.append('- Local association requires review:')
            for side in ('before', 'after'):
                for context in change[side][:2]:
                    lines.append(f'  - {side}, offset {context["start"]}: {safe_text(context["context"])}')
    if not problems:
        lines.extend(['', '| Category | Before | After | Coverage |', '|---|---:|---:|---|'])
        for name, data in categories:
            coverage = 'recognized items' if data['before_count'] or data['after_count'] else 'no items recognized'
            lines.append(f'| {LABELS.get(name, name)} | {data["before_count"]} | {data["after_count"]} | {coverage} |')
    lines.extend(['', 'Comments and code/verbatim regions are excluded from manuscript checks; their ranges are listed in JSON. Explicitly authorized formatting conversions can produce legitimate differences: record their reason instead of hiding them.'])
    return '\n'.join(lines) + '\n', clean


def main(argv: Sequence[str] | None = None) -> int:
    configure_cli_streams()
    parser = argparse.ArgumentParser(description='Compare protected manuscript content within a documented static scope.')
    parser.add_argument('--before', required=True, help='Original UTF-8 file; use - for stdin on one side.')
    parser.add_argument('--after', required=True, help='Revised UTF-8 file; use - for stdin on one side.')
    parser.add_argument('--json', action='store_true', help='Emit schema v2 JSON (legacy categories retained; _meta added).')
    parser.add_argument('--strict', action='store_true', help='Exit 1 for differences or insufficient coverage; default remains advisory.')
    args = parser.parse_args(argv)
    if args.before == args.after == '-':
        parser.error('stdin can supply only one side; provide a file for the other side.')
    try:
        before, after = read_text(args.before), read_text(args.after)
        if not before.strip() or not after.strip():
            raise ValueError('Both inputs must contain non-whitespace text.')
        report = build_report(before, after)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        sys.stderr.write(f'Cannot check input: {exc}\n')
        return 2
    if args.json:
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        clean = report['_meta']['status'] == 'UNCHANGED_WITHIN_COVERAGE'
    else:
        rendered, clean = render(report)
        sys.stdout.write(rendered)
    return 0 if clean or not args.strict else 1


if __name__ == '__main__':
    raise SystemExit(main())
