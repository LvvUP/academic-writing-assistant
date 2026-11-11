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
    python structure_checker.py --section results draft.tex --json
    python structure_checker.py --section method --research-type interpretive draft.md
    cat draft.md | python structure_checker.py --section introduction

``results`` and ``literature_review`` are discipline-neutral names for the
``experiment`` and ``related_work`` checklists; both spellings are accepted.
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
                             '认为',
                             '结论',
                             'suggest',
                             'indicate',
                             'demonstrate',
                             'show that',
                             'conclude',
                             'argue'))])),
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
                           ('What was found', ('实验', '结果', '表明', '发现', '认为', 'results', 'show', 'demonstrate', 'find', 'argue')),
                           ('Bounded scope', ('在所', '数据集上', '范围内', '条件下', '限于', 'evaluated', 'on the', 'under', 'within', 'limited to')),
                           ('Outlook', ('未来', '后续', 'future', 'further'))]))])

# Discipline-neutral section names share the checklist of the original name.
SECTION_ALIASES = {'literature_review': 'related_work', 'results': 'experiment'}
for _alias, _section in SECTION_ALIASES.items():
    SECTION_RULES[_alias] = SECTION_RULES[_section]

# The first four names predate the others and stay valid. Together the list
# mirrors the research types described in references/research-types.md.
RESEARCH_TYPES = ('empirical', 'theoretical', 'review', 'qualitative',
                  'observational', 'interpretive', 'case_study', 'design')
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
    # Surveys, cohorts, secondary data and econometric analysis.
    'observational': OrderedDict([
        ('Data source and sample', ('数据来源', '样本', '问卷', '调查', '队列', 'data source', 'sample', 'survey', 'cohort', 'respondents')),
        ('Variables and measures', ('变量', '测量', '量表', '指标', 'variables', 'measures', 'scale', 'instrument')),
        ('Analysis and identification', ('回归', '模型', '识别', '分析', 'regression', 'model', 'identification', 'analysis')),
        ('Robustness or sensitivity', ('稳健性', '敏感性', 'robustness', 'sensitivity')),
    ]),
    # Humanities and legal argument from sources, texts, statutes and cases.
    'interpretive': OrderedDict([
        ('Question and thesis', ('问题', '论点', '主张', 'question', 'thesis', 'argument')),
        ('Sources and materials', ('史料', '文本', '文献', '法条', '判例', '档案', 'sources', 'texts', 'archival', 'statutes', 'cases')),
        ('Approach or framework', ('方法', '视角', '框架', '解释', 'approach', 'framework', 'perspective', 'interpretation')),
        ('Existing scholarship', ('既有研究', '已有研究', '学界', 'scholarship', 'literature', 'debate')),
    ]),
    'case_study': OrderedDict([
        ('Case selection', ('案例选择', '选取', '典型', 'case selection', 'selected', 'sampling')),
        ('Data sources', ('访谈', '档案', '文件', '观察', '二手资料', 'interviews', 'archival', 'documents', 'observation')),
        ('Analysis approach', ('编码', '分析', '比较', 'coding', 'analysis', 'comparison', 'pattern')),
        ('Validity and limits', ('三角', '信度', '效度', '局限', 'triangulation', 'validity', 'limitations')),
    ]),
    # Systems, devices, software, engineering solutions and teaching designs.
    'design': OrderedDict([
        ('Requirements or problem', ('需求', '问题', '目标', 'requirements', 'problem', 'objective')),
        ('Design and rationale', ('设计', '方案', '架构', '依据', 'design', 'architecture', 'rationale')),
        ('Implementation', ('实现', '开发', '原型', 'implementation', 'prototype', 'developed')),
        ('Validation plan', ('验证', '测试', '试验', '仿真', '评估', 'validation', 'testing', 'simulation', 'evaluation')),
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
    'observational': OrderedDict([
        ('Estimates or associations', ('系数', '相关', '效应', '估计', 'coefficient', 'association', 'correlation', 'effect', 'estimate')),
        ('Uncertainty', ('置信区间', '标准误', '显著', 'confidence interval', 'standard error', 'p value', 'significan*')),
        ('Scope and limitations', ('局限', '样本', '范围', 'limitations', 'sample', 'scope', 'generaliz*')),
    ]),
    'interpretive': OrderedDict([
        ('Claims and argument', ('论证', '认为', '主张', 'argue', 'claim', 'contend')),
        ('Supporting material', ('史料', '引文', '条文', '判例', '材料', 'sources', 'quotation', 'provision', 'cases', 'evidence')),
        ('Qualifications and counterarguments', ('然而', '但', '可能', '或许', 'however', 'although', 'may', 'counterargument')),
    ]),
    'case_study': OrderedDict([
        ('Case findings', ('发现', '案例', 'findings', 'case')),
        ('Evidence from the case', ('访谈', '资料', '数据', '引语', 'interviews', 'documents', 'data', 'quotes')),
        ('Scope of generalization', ('推广', '情境', '边界', 'generaliz*', 'context', 'boundary', 'transferab*')),
    ]),
    'design': OrderedDict([
        ('Validation results', ('结果', '测试', '试验', '仿真', 'results', 'test', 'simulation', 'trial')),
        ('Measures and conditions', ('指标', '条件', '工况', '性能', 'metrics', 'conditions', 'performance')),
        ('Limitations', ('局限', '限制', '不足', 'limitations', 'constraints')),
    ]),
}
# Evidence clues an abstract may use instead of experiments or datasets.
ABSTRACT_EVIDENCE = {
    'empirical': ('observations', 'outcomes', '观察', '测量'),
    'theoretical': ('theorem', 'proof', '定理', '证明'),
    'review': ('synthesis', 'reviewed studies', '综合', '纳入文献'),
    'qualitative': ('themes', 'interviews', '主题', '访谈'),
    'observational': ('survey', 'cohort', 'regression', 'association', '问卷', '调查', '队列', '回归', '相关'),
    'interpretive': ('sources', 'texts', 'archival', 'statutes', 'cases', '史料', '文本', '文献', '档案', '法条', '判例'),
    'case_study': ('case study', 'cases', 'interviews', 'documents', '案例', '访谈', '档案'),
    'design': ('prototype', 'simulation', 'test', 'trial', 'validation', '原型', '仿真', '试验', '测试'),
}
SUGGESTIONS = {
    'Source scope': 'State the scope of the reviewed material. A narrative review need not claim an exhaustive systematic search.',
    'Selection approach': 'Explain source selection as appropriate to the review subtype; formal eligibility/search protocols are specific to systematic or scoping approaches.',
    'Evidence': 'Use evidence appropriate to the study: results, proof, source synthesis or qualitative material. If unavailable, use an explicit placeholder; do not invent it.',
    'Contributions': 'State supported contributions and their scope.',
    'Uncertainty and limitations': 'Describe uncertainty and limits appropriate to the design. A standard deviation is not itself a significance test.',
    'Reflexivity and ethics': 'Report the researcher role and applicable ethics facts only when confirmed.',
    'Robustness or sensitivity': 'Mention robustness or sensitivity analyses only if they were actually carried out.',
    'Analysis and identification': 'State the analysis and any identification assumptions the author actually relied on; causal wording should match them.',
    'Sources and materials': 'Name the sources, editions or legal materials the argument rests on; do not add sources the author did not use.',
    'Qualifications and counterarguments': 'Interpretive qualifiers and counterarguments are part of the argument; keep those the author made.',
    'Scope of generalization': 'A case supports analytic rather than statistical generalization; state the context the findings apply to.',
    'Validation plan': 'An implemented design is not yet a validated one; describe only validation that was planned or performed.',
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
    section = SECTION_ALIASES.get(section, section)
    if section == 'method' and research_type != 'empirical':
        rules = OrderedDict(RESEARCH_METHODS[research_type])
    if section == 'experiment' and research_type != 'empirical':
        rules = OrderedDict(RESEARCH_RESULTS[research_type])
    if section == 'abstract':
        rules['Evidence'] = tuple(rules['Evidence']) + ABSTRACT_EVIDENCE[research_type]
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
