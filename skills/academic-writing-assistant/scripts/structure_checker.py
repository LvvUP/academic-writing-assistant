#!/usr/bin/env python3
"""Check whether a draft section contains the elements reviewers expect.

This is a keyword scan, and it should be read as one: it detects whether a
draft *mentions* something, not whether it does so well. A section can pass
every check and still be poorly argued, and a good section can fail a check
because the author phrased something unusually. Treat findings as a list of
things to look at.

The value is catching outright omissions -- an abstract with no results
sentence, an experiment section that never names a baseline -- which are easy
to miss when re-reading your own draft.

Usage::

    python structure_checker.py --section abstract draft.md
    python structure_checker.py --section experiment draft.tex --json
    cat draft.md | python structure_checker.py --section introduction
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from check_utils import configure_cli_streams, read_input, markdown_text, placeholder_spans
from prose_utils import mask_prose


# General empirical research does not imply neural networks or ablation studies.
SECTION_RULES = OrderedDict([('abstract',
              OrderedDict([('Context and problem',
                            ('背景',
                             '问题',
                             '挑战',
                             '难以',
                             'challenge',
                             'problem',
                             'remains',
                             'difficult')),
                           ('Gap in existing work',
                            ('不足', '局限', '现有方法', 'however', 'limitation', 'existing', 'prior')),
                           ('Proposed approach',
                            ('本文',
                             '提出',
                             '我们',
                             'we propose',
                             'we present',
                             'this paper',
                             'this study',
                             'method')),
                           ('Evidence',
                            ('实验',
                             '数据集',
                             '验证',
                             '结果',
                             'experiment',
                             'dataset',
                             'evaluat',
                             'results',
                             'achiev')),
                           ('Conclusion',
                            ('表明',
                             '说明',
                             '结果显示',
                             'suggest',
                             'indicate',
                             'demonstrate',
                             'show that'))])),
             ('introduction',
              OrderedDict([('Research background',
                            ('背景', '近年来', '研究', 'background', 'recent', 'widely')),
                           ('Specific problem',
                            ('问题', '挑战', '难点', 'problem', 'challenge', 'difficult')),
                           ('Prior work and its limits',
                            ('现有',
                             '已有方法',
                             '然而',
                             '不足',
                             'existing',
                             'however',
                             'limitation',
                             'prior work')),
                           ('Proposed response',
                            ('提出', '本文', '为此', 'we propose', 'to address', 'this paper')),
                           ('Contributions',
                            ('贡献', '主要工作', 'contribution', 'summarized as', 'as follows'))])),
             ('related_work',
              OrderedDict([('Organizing principle',
                            ('可分为', '分为', '两类', '三类', 'categor', 'grouped', 'broadly')),
                           ('Prior approaches',
                            ('方法', '研究', '工作', 'method', 'approach', 'studies', 'work')),
                           ('Stated limitation',
                            ('局限', '不足', '难以', 'limitation', 'however', 'fail', 'struggle')),
                           ('Transition to this work',
                            ('与之不同',
                             '本文',
                             '相比之下',
                             'in contrast',
                             'unlike',
                             'differ',
                             'this work'))])),
             ('method',
              OrderedDict([('Study design', ('研究设计', '设计', 'study design', 'design', 'protocol')),
                           ('Materials or data',
                            ('材料',
                             '样本',
                             '数据',
                             'materials',
                             'data',
                             'participants',
                             'observations')),
                           ('Procedure', ('步骤', '程序', '过程', 'procedure', 'protocol', 'process')),
                           ('Analysis approach',
                            ('分析', '估计', 'analysis', 'estimation', 'measurement')),
                           ('Assumptions and scope',
                            ('假设', '条件', '范围', 'assumptions', 'conditions', 'scope'))])),
             ('experiment',
              OrderedDict([('Materials or data',
                            ('数据',
                             '材料',
                             '观察',
                             '样本',
                             'data',
                             'materials',
                             'observations',
                             'samples')),
                           ('Outcomes or measures',
                            ('结果',
                             '指标',
                             '评价',
                             'outcomes',
                             'measures',
                             'metrics',
                             'accuracy',
                             'precision',
                             'recall')),
                           ('Procedure', ('流程', '设置', '步骤', 'procedure', 'settings', 'protocol')),
                           ('Results', ('结果', '发现', 'results', 'outcomes', 'findings')),
                           ('Uncertainty and limitations',
                            ('不确定性',
                             '误差',
                             '局限',
                             'uncertainty',
                             'limitations',
                             'confidence interval'))])),
             ('discussion',
              OrderedDict([('Interpretation',
                            ('原因',
                             '解释',
                             '分析',
                             '这表明',
                             'suggest',
                             'indicate',
                             'explain',
                             'attribute')),
                           ('Where it works',
                            ('优势', '有效', '改善', 'benefit', 'advantage', 'improve')),
                           ('Where it fails',
                            ('失败', '不足', '受限', 'fail', 'degrade', 'struggle', 'worse')),
                           ('Limitations', ('局限', '限制', 'limitation', 'constrain')),
                           ('Future work',
                            ('未来', '后续', '下一步', 'future', 'further work', 'plan to'))])),
             ('conclusion',
              OrderedDict([('What was done', ('本文', '提出', 'we propose', 'this paper', 'presented')),
                           ('What was found', ('实验', '结果', '表明', 'results', 'show', 'demonstrate')),
                           ('Bounded scope', ('在所', '数据集上', 'evaluated', 'on the', 'under')),
                           ('Outlook', ('未来', '后续', 'future', 'further'))]))])

RESEARCH_TYPES = ('empirical', 'theoretical', 'review', 'qualitative')
RESEARCH_METHODS = {
    'theoretical': OrderedDict([
        ('Assumptions and definitions', ('假设', '定义', 'assumptions', 'define', 'definitions')),
        ('Formal statement', ('定理', '命题', '结论', 'theorem', 'proposition', 'statement')),
        ('Proof strategy', ('证明', '引理', 'prove', 'proof', 'lemma')),
        ('Scope and counterexamples', ('适用条件', '反例', '边界', 'conditions', 'counterexample', 'scope')),
    ]),
    'review': OrderedDict([
        ('Source scope', ('范围', '文献', 'scope', 'sources', 'literature', 'search')),
        ('Selection approach', ('选取', '选择', '纳入', '依据', 'selection', 'selected', 'eligibility', 'inclusion')),
        ('Synthesis approach', ('综合', '归纳', '整合', 'synthesis', 'synthesize', 'synthesise')),
        ('Sources and limitations', ('来源', '偏倚', '局限', 'sources', 'bias', 'limitations')),
    ]),
    'qualitative': OrderedDict([
        ('Sampling and context', ('抽样', '招募', '情境', 'sampling', 'recruitment', 'context')),
        ('Data collection', ('访谈', '观察', '焦点小组', 'interviews', 'interview', 'observation', 'focus group')),
        ('Analysis approach', ('编码', '主题分析', '分析', 'coding', 'thematic', 'analysis')),
        ('Reflexivity and ethics', ('反思', '研究者立场', '伦理', 'reflexivity', 'positionality', 'ethics')),
    ]),
}
RESEARCH_RESULTS = {
    'theoretical': OrderedDict([
        ('Formal result', ('定理', '命题', 'theorem', 'proposition')),
        ('Proof or derivation', ('证明', '推导', 'proof', 'derivation')),
        ('Applicability and limits', ('条件', '反例', '范围', 'conditions', 'counterexample', 'scope')),
    ]),
    'review': OrderedDict([
        ('Evidence synthesis', ('综合', '归纳', 'synthesis', 'synthesize')),
        ('Source support', ('来源', '文献', 'sources', 'studies', 'references')),
        ('Gaps and limitations', ('缺口', '局限', '偏倚', 'gaps', 'limitations', 'bias')),
    ]),
    'qualitative': OrderedDict([
        ('Themes or interpretations', ('主题', '解释', 'themes', 'interpretations')),
        ('Material support', ('引语', '访谈', '材料', 'quotes', 'interviews', 'excerpts')),
        ('Context and limits', ('情境', '边界', '可迁移', 'context', 'limits', 'transferability')),
    ]),
}
SUGGESTIONS = {
    'Source scope': 'State the scope of the reviewed material. A narrative review need not claim an exhaustive systematic search.',
    'Selection approach': 'Explain source selection as appropriate to the review subtype; formal eligibility/search protocols are specific to systematic or scoping approaches.',
    'Evidence': 'Use evidence appropriate to the study: results, proof, source synthesis or qualitative material. If unavailable, use an explicit placeholder; do not invent it.',
    'Contributions': 'State supported contributions and their scope.',
    'Uncertainty and limitations': 'Describe uncertainty and limits appropriate to the design. A standard deviation is not itself a significance test.',
    'Reflexivity and ethics': 'Report the researcher role and applicable ethics facts only when confirmed.',
}


def read_text(path: Optional[str]) -> str:
    return read_input(path)


def keyword_pattern(keyword: str) -> str:
    keyword = keyword.strip()
    stems = {'evaluat', 'achiev', 'categor', 'minimiz', 'maximiz', 'optimiz', 'constrain'}
    wildcard = keyword.endswith('*') or keyword in stems
    base = keyword.rstrip('*')
    left = r'(?<![A-Za-z0-9_])' if base and base[0].isascii() and base[0].isalnum() else ''
    right = r'(?![A-Za-z0-9_])' if base and base[-1].isascii() and base[-1].isalnum() else ''
    return left + re.escape(base) + (r'[A-Za-z]*' if wildcard else '') + right


def contains_keyword(text: str, keywords: Sequence[str]) -> bool:
    return any(re.search(keyword_pattern(keyword), text, re.IGNORECASE) for keyword in keywords)


def rules_for(section: str, research_type: str) -> OrderedDict:
    if section not in SECTION_RULES:
        raise ValueError('Unknown section: ' + section)
    if research_type not in RESEARCH_TYPES:
        raise ValueError('Unknown research type: ' + research_type)
    rules = OrderedDict(SECTION_RULES[section])
    if section == 'method' and research_type != 'empirical':
        rules = OrderedDict(RESEARCH_METHODS[research_type])
    if section == 'experiment' and research_type != 'empirical':
        rules = OrderedDict(RESEARCH_RESULTS[research_type])
    if section == 'abstract':
        rules['Evidence'] = tuple(rules['Evidence']) + {
            'empirical': ('observations', 'outcomes', '观察', '测量'),
            'theoretical': ('theorem', 'proof', '定理', '证明'),
            'review': ('synthesis', 'reviewed studies', '综合', '纳入文献'),
            'qualitative': ('themes', 'interviews', '主题', '访谈'),
        }[research_type]
    return rules


def audit(section: str, text: str, research_type: str = 'empirical') -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Input must be non-empty text.')
    prose, warnings, excluded = mask_prose(text)
    rules = rules_for(section, research_type)
    present, missing, matches = [], [], []
    newlines = [-1] + [i for i, char in enumerate(text) if char == '\n']
    for label, keywords in rules.items():
        candidates = [match for keyword in keywords if (match := re.search(keyword_pattern(keyword), prose, re.IGNORECASE))]
        if not candidates:
            missing.append(label)
            continue
        present.append(label)
        match = min(candidates, key=lambda item: item.start())
        line = bisect.bisect_left(newlines, match.start())
        matches.append({'element': label, 'raw': text[match.start():match.end()], 'start': match.start(), 'end': match.end(), 'line': line,
                        'column': match.start() - newlines[line - 1]})
    placeholder_items = placeholder_spans(prose)
    for item in placeholder_items:
        item['raw'] = text[item['start']:item['end']]
    return {'present': present, 'missing': missing, 'research_type': research_type,
            'placeholders': len(placeholder_items), 'placeholder_items': placeholder_items,
            'coverage': 'keyword_clues_only', 'matches': matches, 'warnings': warnings, 'excluded_regions': excluded,
            'match_scope': 'First recognized clue per checklist item; no scientific or argument-quality validation.',
            'study_note': 'Review subtype determines whether a formal search protocol and eligibility criteria apply; a narrative review does not automatically require them.' if research_type == 'review' else 'Adapt these optional clues to the actual study design.'}


def count_placeholders(text: str) -> int:
    return len(placeholder_spans(mask_prose(text)[0]))


def render(section: str, result: dict, placeholders: int) -> str:
    lines = ['# Section Structure Check', '', f'Section: {section}', f'Research type: {result.get("research_type", "empirical")}', result.get('study_note', ''), '', '## Detected', '']
    lines.extend('- ' + markdown_text(item) for item in result['present'])
    if not result['present']:
        lines.append('- No configured clues detected.')
    lines.extend(['', '## Possibly missing', ''])
    for item in result['missing']:
        lines.append('- **' + markdown_text(item) + '** — ' + SUGGESTIONS.get(item, 'Include only if relevant to the study and supported by provided material.'))
    if not result['missing']:
        lines.append('- All configured clues were mentioned; this does not certify section quality.')
    if placeholders:
        lines.extend(['', '## Placeholders', '', f'- {placeholders} placeholder(s) found. Resolve these with confirmed information before submission.'])
    if result.get('warnings'):
        lines.extend(['', '## Coverage limitations', ''])
        lines.extend('- ' + markdown_text(warning['reason']) for warning in result['warnings'])
    lines.extend(['', 'This is a keyword scan. Hits are clues, not proof of section quality, completed work, valid evidence or real citations. The selected study type determines the checklist; adapt it to the actual design.'])
    return '\n'.join(lines) + '\n'


def main(argv: Optional[Sequence[str]] = None) -> int:
    configure_cli_streams()
    parser = argparse.ArgumentParser(description='Study-aware section clues; no automatic judgment of scientific quality.')
    parser.add_argument('--section', choices=sorted(SECTION_RULES), required=True)
    parser.add_argument('--research-type', choices=RESEARCH_TYPES, default='empirical')
    parser.add_argument('file', nargs='?', help='UTF-8 file; stdin when omitted or -.')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--strict', action='store_true', help='Exit 1 for missing clues, unresolved placeholders or incomplete extraction; default remains advisory.')
    args = parser.parse_args(argv)
    try:
        text = read_text(args.file)
        result = audit(args.section, text, args.research_type)
        placeholders = result['placeholders']
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        sys.stderr.write(f'Cannot check structure input: {exc}\n')
        return 2
    payload = dict(result, section=args.section)
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + '\n' if args.json else render(args.section, result, placeholders))
    return 1 if args.strict and (result['missing'] or placeholders or result['warnings']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
