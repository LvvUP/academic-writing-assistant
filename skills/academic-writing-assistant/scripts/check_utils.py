"""Local-only input, display and placeholder conventions shared by checks."""
from __future__ import annotations

import bisect
import html
import re
import sys
from pathlib import Path


def read_input(path=None):
    """Caller-relative UTF-8 input; one leading BOM is not manuscript content."""
    if path and path != '-':
        value = Path(path).read_text(encoding='utf-8-sig')
    else:
        value = sys.stdin.read().removeprefix('\ufeff')
    if not value.strip():
        raise ValueError('Input is empty.')
    return value


def markdown_text(value):
    """Render untrusted excerpts as inert text, including within Markdown tables."""
    text = html.escape(str(value), quote=True)
    text = text.replace('\r', ' ').replace('\n', ' ')
    return re.sub(r'([\\`*_{}\[\]()#+.!|>~-])', r'\\\1', text)


# Recognize manuscript slots used by this project, not all bracketed labels.
PLACEHOLDER = re.compile(
    r'^(?:请|待|需|作者|补充|填写|确认|已确认|已提供|用户提供|用户指定|对应|实际|按目标|'
    r'据其|各方向|与本文|与目标|修改后|必要|重要 L[23]|候选表述|结果与结论|'
    r'数据集|主要指标|评价指标|真实位置|工具|TODO\b|TBD\b|FIXME\b|please\b|'
    r'citation needed\b|dataset name\b|tool(?: name|/version)\b|metric\b|'
    r'author\b|editor\b|title\b|journal\b|X(?:\b|[–-]))', re.IGNORECASE)
SLOT = re.compile(r'\[([^\]\n]{1,500})\]|【([^】\n]{1,500})】')
BARE_SLOT = re.compile(r'(?<![\w])(?:TODO|TBD|FIXME)(?![\w])', re.IGNORECASE)
LINK_DEFINITION = re.compile(r':\s*(?:https?://|[^\s]{1,512}\.(?:md|html)\b)')


def placeholder_spans(text):
    candidates, bracketed = [], []
    for match in SLOT.finditer(text):
        bracketed.append((match.start(), match.end()))
        content = match.group(1) if match.group(1) is not None else match.group(2)
        # Match at the original offset: copying every remaining suffix makes
        # a long sequence of bracketed citations quadratic.
        is_link = text.startswith(('(', '['), match.end()) or bool(LINK_DEFINITION.match(text, match.end()))
        if not is_link and PLACEHOLDER.search(content.strip()):
            candidates.append(match)
    bracket_index = 0
    for match in BARE_SLOT.finditer(text):
        while bracket_index < len(bracketed) and bracketed[bracket_index][1] <= match.start():
            bracket_index += 1
        if bracket_index == len(bracketed) or match.start() < bracketed[bracket_index][0]:
            candidates.append(match)
    newlines = [index for index, char in enumerate(text) if char == '\n']
    return [{'start': m.start(), 'end': m.end(), 'raw': m.group(),
             'line': bisect.bisect_left(newlines, m.start()) + 1}
            for m in sorted(candidates, key=lambda item: item.start())]
