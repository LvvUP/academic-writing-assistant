"""Position-preserving, non-executing lexical extraction for fidelity checks.

This is deliberately a bounded scanner, not a TeX engine or a semantic parser.
Unsupported or unclosed constructs are recorded as coverage warnings. Offsets
always index the original Python Unicode string; end offsets are exclusive.
"""
from __future__ import annotations

import bisect
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

CATEGORIES = (
    'citations', 'bracket_citations', 'author_year_citations', 'cross_references',
    'structural_references', 'math_blocks', 'numbers', 'named_entities', 'custom_macros',
)
CITATIONS = {'cite', 'citep', 'citet', 'citeauthor', 'citeyear', 'autocite', 'parencite', 'footcite', 'nocite', 'textcite', 'smartcite', 'supercite'}
REFERENCES = {'ref', 'eqref', 'autoref', 'cref', 'Cref', 'pageref', 'nameref', 'label', 'vref'}
MATH_ENVS = {'equation', 'align', 'alignat', 'flalign', 'gather', 'multline', 'eqnarray', 'split', 'displaymath', 'math', 'cases', 'matrix', 'pmatrix', 'bmatrix', 'array'}
PROSE_ENVS = {'document', 'abstract', 'itemize', 'enumerate', 'description', 'quote', 'quotation', 'center', 'flushleft', 'flushright', 'table', 'tabular', 'figure', 'theorem', 'lemma', 'proof', 'proposition', 'corollary', 'definition', 'remark', 'minipage'}
CODE_ENVS = {'verbatim', 'Verbatim', 'lstlisting', 'minted'}
TEXT_COMMANDS = {'text', 'mbox', 'textrm', 'textnormal', 'textbf', 'textit', 'textsf', 'texttt', 'operatorname'}
KNOWN_COMMANDS = CITATIONS | REFERENCES | TEXT_COMMANDS | {
    'begin', 'end', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph',
    'chapter', 'part', 'emph', 'textsc', 'item', 'footnote', 'caption', 'title', 'author',
    'date', 'maketitle', 'tableofcontents', 'includegraphics', 'documentclass', 'usepackage',
    'bibliography', 'bibliographystyle', 'printbibliography', 'addbibresource', 'url', 'href',
    'left', 'right', 'quad', 'qquad', 'hspace', 'vspace', 'newline', 'par', 'centering',
    'small', 'large', 'Large', 'huge', 'Huge', 'noindent', 'vfill', 'hfill', 'label',
    'mathrm', 'mathbf', 'mathcal', 'frac', 'sum', 'int', 'sqrt', 'alpha', 'beta', 'gamma',
    'delta', 'epsilon', 'theta', 'lambda', 'mu', 'sigma', 'phi', 'psi', 'omega', 'times',
    'cdot', 'leq', 'geq', 'neq', 'approx', 'in', 'hat', 'tilde', 'bar', 'vec', 'mathbb',
    'log', 'exp', 'max', 'min', 'argmax', 'argmin', 'le', 'ge', 'pm', 'mp', 'div',
}
NUMBER_COMMANDS = {'num', 'SI', 'si', 'qty', 'unit', 'numrange', 'SIrange', 'qtyrange', 'numlist', 'SIlist', 'qtylist'}
DYNAMIC_COMMANDS = {'input', 'include', 'write', 'write18', 'openout', 'read', 'catcode', 'csname', 'directlua', 'scantokens', 'newcommand', 'renewcommand', 'def', 'edef', 'gdef', 'xdef', 'let'}
COMMAND = re.compile(r'\\([A-Za-z@]+)(\*)?')
ATOM = re.compile(r'[+\-−]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)(?:[eE][+\-−]?\d+)?')
POWER = re.compile(r'(?:[⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+|\^\{?[+\-−]?\d+\}?)')
NUMERIC_SPACE = ' \t\u00a0~'
LINEWRAP_SPACE = re.compile(r'[ \t\u00a0~]*(?:\r\n?|\n)[ \t\u00a0~\r\n]*')
RELATION_TOKEN = r'(?:<=|>=|!=|[<>=≤≥≠≈]|\\(?:leq?|geq?|neq|approx)(?![A-Za-z@]))'
RELATION_BEFORE = re.compile('(' + RELATION_TOKEN + r')[ \t\u00a0~]*$')
NUMERIC_LINK = re.compile(
    r'[ \t\u00a0~]*(' + RELATION_TOKEN +
    r'|±|∓|\\(?:pm|mp|times|cdot|div)(?![A-Za-z@])|\+/-|×|÷|·|⋅|[*/+]|–|—|−|-|至|到|\bto\b)[ \t\u00a0~]*')
INTERVAL_CONTEXT = re.compile(
    r'(?:\bCI|confidence\s+interval|\binterval|\brange|置信区间|区间|范围)'
    r'(?:\s+(?:is|was))?[ \t\u00a0~]*[:：=]?[ \t\u00a0~]*$', re.IGNORECASE)
UNKNOWN_UNIT = re.compile(r'[A-Za-zμµ][A-Za-z0-9μµ]*(?:[/·][A-Za-z0-9]+)*')
COUNT_NOUN = re.compile(r'\s+(?:participants|subjects|samples|patients|runs|seeds|times|units)\b')
PROSE_WORDS = {'and', 'or', 'to', 'for', 'of', 'in', 'on', 'at', 'was', 'were', 'is', 'are', 'with', 'without', 'than', 'compared', 'participants', 'subjects', 'samples', 'patients', 'runs', 'seeds', 'times', 'units'}
# Longest units first. Unknown adjacent alphabetic suffixes are reported as a
# coverage warning rather than silently asserted to have been protected.
UNIT = re.compile(
    r'(?:percentage\s+points?|percent(?:age)?|points?|百分点|百分比|个百分[点比]|'
    r'\\%|[%‰‱]|'
    r'(?:[numcdhkMGTμµ]?mol|[numcdhkMGTμµ]?g|[numcdhkMGTμµ]?m|[numcdhkMGTμµ]?s|'
    r'[numcdhkMGTμµ]?[Ll]|[numcdhkMGTμµ]?A|[numcdhkMGTμµ]?V|[numcdhkMGTμµ]?W|'
    r'[numcdhkMGTμµ]?Hz|[numcdhkMGTμµ]?Pa|[numcdhkMGTμµ]?J|[numcdhkMGTμµ]?K|'
    r'dB|rpm|bpm|fps|IU|mmHg|eV|Da|Bq|Gy|Sv|°C|°F|°|'
    r'min|hours?|hrs?|days?|weeks?|years?|bytes?|bits?|px|dpi|ppi|'
    r'千克|毫克|微克|克|公斤|毫米|厘米|千米|米|毫升|微升|升|秒|分钟|小时|天)'
    r'(?:\^\{?[+\-−]?\d+\}?|[²³⁻¹⁰⁴⁵⁶⁷⁸⁹]+|[23])?'
    r'(?:\s*[/·⋅]\s*(?:[numcdhkMGTμµ]?[gmsLl]|min|h|kg|mol)'
    r'(?:\^\{?[+\-−]?\d+\}?|[²³⁻¹⁰⁴⁵⁶⁷⁸⁹]+)?)*)'
    r'(?![A-Za-z0-9])',
)
STRUCTURE = re.compile(r'(?<![A-Za-z])(?P<kind>Section|Sect\.|Sec\.|Table|Tab\.|Figure|Fig\.|Equation|Eq\.|Algorithm|Alg\.|Appendix|Chapter|表|图|公式|附录|章节)\s*~?\s*\(?(?P<id>\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\)?', re.IGNORECASE)
BRACKET = re.compile(r'(?<!\\)\[(\d+(?:\s*[-,–]\s*\d+)*)\]')
AUTHOR_YEAR = re.compile(r"\(([A-Z][A-Za-z\u00C0-\u024F'’\-]+(?:\s+(?:et\s+al\.?|and|&)\s*[A-Za-z\u00C0-\u024F'’\-]*)?,?\s*\d{4}[a-z]?)\)")
ENTITY = re.compile(r'(?<![\w-])([A-Z][A-Za-z]*(?:-[A-Z0-9][A-Za-z0-9]*)+|[A-Z]{2,}[A-Za-z0-9]*|[A-Z][a-z]+[A-Z][A-Za-z0-9]*|[A-Z][A-Za-z]+\d+[A-Za-z0-9]*)(?![\w-])')


def escaped(text: str, index: int) -> bool:
    start = index
    while start and text[start - 1] == '\\':
        start -= 1
    return (index - start) % 2 == 1


def mask_region(chars: List[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] not in '\r\n':
            chars[index] = ' '


def balanced(text: str, start: int, opener: str = '{', closer: str = '}') -> Optional[int]:
    """Return exclusive end of a balanced group, without expanding any macro."""
    if start >= len(text) or text[start] != opener:
        return None
    depth = 0
    for index in range(start, len(text)):
        if escaped(text, index):
            continue
        if text[index] == opener:
            depth += 1
            if depth > 128:
                return None
        elif text[index] == closer:
            depth -= 1
            if depth == 0:
                return index + 1
    return None


def arguments(text: str, start: int, max_required: Optional[int] = None) -> Tuple[List[Tuple[int, int]], int, bool]:
    groups: List[Tuple[int, int]] = []
    cursor = start
    required_count = 0
    while cursor < len(text):
        if max_required is not None and required_count >= max_required:
            break
        probe = cursor
        while probe < len(text) and text[probe] in ' \t\r\n':
            probe += 1
        if probe >= len(text) or text[probe] not in '[{':
            break
        end = balanced(text, probe, text[probe], ']' if text[probe] == '[' else '}')
        if end is None:
            return groups, len(text), False
        groups.append((probe, end))
        required_count += text[probe] == '{'
        cursor = end
    return groups, cursor, True


def normalize_math(body: str) -> str:
    """Ignore TeX math layout whitespace, retain text and control-word boundaries."""
    out: List[str] = []
    cursor = 0
    while cursor < len(body):
        # TeX control symbols (especially escaped spaces) are single tokens;
        # dropping their whitespace would turn \\ b into the macro \\b.
        if body[cursor] == '\\' and cursor + 1 < len(body) and not (body[cursor + 1].isalpha() or body[cursor + 1] == '@'):
            symbol = ' ' if body[cursor + 1].isspace() else body[cursor + 1]
            out.append('\\' + symbol)
            cursor += 2
            continue
        command = COMMAND.match(body, cursor)
        if command:
            out.append(command.group(0))
            end = command.end()
            if command.group(1) in TEXT_COMMANDS:
                probe = end
                while probe < len(body) and body[probe].isspace():
                    probe += 1
                group_end = balanced(body, probe)
                if group_end:
                    out.append(re.sub(r'\s+', ' ', body[probe:group_end]))
                    cursor = group_end
                    continue
            # A separating space after a control word is significant for lexing:
            # \\alpha x cannot be normalized into the different macro \\alphax.
            if end < len(body) and body[end].isspace():
                probe = end
                while probe < len(body) and body[probe].isspace():
                    probe += 1
                if probe < len(body) and body[probe].isalpha():
                    out.append(' ')
            cursor = end
            continue
        if not body[cursor].isspace():
            out.append(body[cursor])
        cursor += 1
    return ''.join(out)


def sentence_spans(text: str) -> List[Tuple[int, int]]:
    """Lightweight context boundaries, retaining offsets and common abbreviations."""
    spans: List[Tuple[int, int]] = []
    start = 0
    for index, char in enumerate(text):
        boundary = char in '。！？!?'
        if char == '.':
            if index and index + 1 < len(text) and text[index - 1].isdigit() and text[index + 1].isdigit():
                continue
            token = re.search(r'([A-Za-z.]+)\.$', text[max(start, index - 12):index + 1])
            if token and (token.group(1).lower() in {'dr', 'mr', 'mrs', 'ms', 'prof', 'fig', 'eq', 'sec', 'e.g', 'i.e', 'al', 'vs'} or len(token.group(1)) == 1):
                continue
            boundary = index + 1 == len(text) or text[index + 1].isspace()
        if char == '\n':
            boundary = True
        if boundary:
            end = index + 1
            if text[start:end].strip():
                spans.append((start, end))
            start = end
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


@dataclass
class Extraction:
    items: Dict[str, List[dict]]
    coverage: dict


class Scanner:
    def __init__(self, text: str):
        self.text = text
        self.items: Dict[str, List[dict]] = {name: [] for name in CATEGORIES}
        self.lines = [-1] + [i for i, char in enumerate(text) if char == '\n']
        self.sentences = sentence_spans(text)
        self.sentence_ends = [end for _, end in self.sentences]
        self.warnings: List[dict] = []
        self.excluded: List[dict] = []

    def warn(self, kind: str, start: int, end: int, detail: str) -> None:
        self.warnings.append({'kind': kind, 'start': start, 'end': end, 'detail': detail})

    def add(self, category: str, start: int, end: int, value: str, **extra) -> None:
        line = bisect.bisect_left(self.lines, start)  # lines stores newline offsets
        sentence_id = bisect.bisect_right(self.sentence_ends, start)
        if sentence_id < len(self.sentences):
            context_start, context_end = self.sentences[sentence_id]
        else:
            context_start, context_end = start, end
        context_start = max(context_start, start - 140)
        context_end = min(context_end, end + 140)
        self.items[category].append({
            'value': value, 'raw': self.text[start:end], 'category': category,
            'start': start, 'end': end, 'line': max(line, 1),
            'column': start - self.lines[max(line - 1, 0)],
            'context': self.text[context_start:context_end].strip(),
            'context_start': context_start, 'context_end': context_end,
            'sentence_id': sentence_id, **extra,
        })

    def exclusions(self) -> str:
        text = self.text
        chars = list(text)
        cursor = 0
        line_start = 0
        math_mode = ''
        # Detect document syntax only while scanning active material. Code and
        # comments are skipped before they can affect the enclosing format.
        full_latex = False
        while cursor < len(text):
            end = None
            kind = ''
            if text[cursor] in '`~' and not text[line_start:cursor].strip():
                fence = re.match(r'(`{3,}|~{3,})[^\n]*', text[cursor:])
                if fence:
                    token = fence.group(1)
                    closer = re.search(r'(?m)^\s{0,3}' + re.escape(token[0]) + '{' + str(len(token)) + r',}[^\S\n]*$', text[cursor + len(fence.group(0)):])
                    end = cursor + len(fence.group(0)) + closer.end() if closer else len(text)
                    kind = 'fenced_code'
                    if not closer:
                        self.warn('unclosed_code', cursor, end, 'Fenced code has no closing fence.')
            if end is None and text[cursor] == '`' and not escaped(text, cursor):
                run = re.match(r'`+', text[cursor:]).group(0)
                close = text.find(run, cursor + len(run))
                if close >= 0:
                    end, kind = close + len(run), 'inline_code'
                else:
                    self.warn('unclosed_code', cursor, cursor + len(run), 'Unclosed inline code delimiter.')
            if end is None and text.startswith('\\verb', cursor):
                match = re.match(r'\\verb\*?([^A-Za-z\s])', text[cursor:])
                if match:
                    close = text.find(match.group(1), cursor + len(match.group(0)))
                    end, kind = (close + 1 if close >= 0 else len(text)), 'verbatim'
                    if close < 0:
                        self.warn('unclosed_code', cursor, end, 'Unclosed verbatim delimiter.')
            if end is None and text.startswith('\\begin{', cursor):
                match = re.match(r'\\begin\{([^}]+)\}', text[cursor:])
                if match and match.group(1).rstrip('*') in CODE_ENVS:
                    closing = '\\end{' + match.group(1) + '}'
                    close = text.find(closing, cursor + len(match.group(0)))
                    end, kind = (close + len(closing) if close >= 0 else len(text)), 'verbatim'
                    if close < 0:
                        self.warn('unclosed_code', cursor, end, 'Unclosed verbatim environment.')
            if end is None and text[cursor] == '%' and not escaped(text, cursor):
                # A numeric percent suffix in ordinary prose is not a comment.
                prefix = text[max(0, cursor - 8):cursor].rstrip(' \t')
                prev = prefix[-1] if prefix else ''
                if math_mode or full_latex or not prev or not (prev.isdigit() or prev in '.,'):
                    newline = text.find('\n', cursor)
                    end, kind = (newline if newline >= 0 else len(text)), 'latex_comment'
            if end is not None:
                self.excluded.append({'kind': kind, 'start': cursor, 'end': end})
                mask_region(chars, cursor, end)
                cursor = end
                line_start = text.rfind('\n', 0, cursor) + 1
            else:
                if text.startswith('\\begin{document}', cursor) or (text.startswith('\\documentclass', cursor) and re.compile(r'\\documentclass(?![A-Za-z@])').match(text, cursor)):
                    full_latex = True
                if text[cursor] == '\n':
                    line_start = cursor + 1
                if text[cursor] == '$' and not escaped(text, cursor):
                    token = '$$' if text.startswith('$$', cursor) else '$'
                    math_mode = '' if math_mode == token else token
                    cursor += len(token)
                    continue
                if text.startswith(('\\(', '\\['), cursor) and not escaped(text, cursor):
                    math_mode = text[cursor:cursor + 2]
                elif text.startswith(('\\)', '\\]'), cursor) and not escaped(text, cursor):
                    math_mode = ''
                environment = re.match(r'\\(begin|end)\{([^}]+)\}', text[cursor:]) if text.startswith('\\', cursor) else None
                if environment and environment.group(2).rstrip('*') in MATH_ENVS:
                    math_mode = environment.group(2) if environment.group(1) == 'begin' else ''
                cursor += 1
        return ''.join(chars)

    def math(self, text: str) -> str:
        chars = list(text)
        cursor = 0
        while cursor < len(text):
            opening = closing = ''
            body_start = cursor
            name = ''
            if not escaped(text, cursor) and text[cursor] == '$':
                opening = '$$' if text.startswith('$$', cursor) else '$'
                closing = opening
                body_start = cursor + len(opening)
            elif text.startswith(('\\(', '\\['), cursor) and not escaped(text, cursor):
                opening = text[cursor:cursor + 2]
                closing = '\\)' if opening == '\\(' else '\\]'
                body_start = cursor + 2
            elif text.startswith('\\begin{', cursor) and not escaped(text, cursor):
                match = re.match(r'\\begin\{([^}]+)\}', text[cursor:])
                if match and match.group(1).rstrip('*') in MATH_ENVS:
                    opening = match.group(0)
                    name = match.group(1)
                    closing = '\\end{' + name + '}'
                    body_start = cursor + len(opening)
            if not opening:
                cursor += 1
                continue
            probe = body_start
            depth = 1
            end = None
            while probe < len(text):
                if name and text.startswith(opening, probe) and not escaped(text, probe):
                    depth += 1
                    probe += len(opening)
                    continue
                if text.startswith(closing, probe) and not escaped(text, probe):
                    depth -= 1
                    if depth == 0:
                        end = probe + len(closing)
                        break
                    probe += len(closing)
                    continue
                probe += 1
            if end is None:
                self.warn('unclosed_math', cursor, len(text), 'Math delimiter/environment is not closed.')
                mask_region(chars, cursor, len(text))
                break
            body = text[body_start:probe]
            for command in COMMAND.finditer(body):
                if command.group(1) in DYNAMIC_COMMANDS:
                    self.warn('dynamic_latex', body_start + command.start(), body_start + command.end(), 'Macro expansion/external input is not executed: ' + command.group(1) + '.')
            # Check brace balance in math independently of delimiter closure.
            braces = 0
            for offset, char in enumerate(body):
                if not escaped(body, offset):
                    braces += (char == '{') - (char == '}')
                    if braces < 0:
                        break
            if braces != 0:
                self.warn('unbalanced_math_braces', cursor, end, 'Math has unbalanced groups.')
            if not body.strip():
                self.warn('empty_math', cursor, end, 'Empty math block.')
            # Preserve math environment and delimiter type; changing them is an
            # explicit formatting conversion for the author to approve.
            self.add('math_blocks', cursor, end, opening + normalize_math(body) + closing)
            mask_region(chars, cursor, end)
            cursor = end
        return ''.join(chars)

    def commands(self, text: str) -> str:
        chars = list(text)
        cursor = 0
        while cursor < len(text):
            match = COMMAND.match(text, cursor)
            if not match or escaped(text, cursor):
                cursor += 1
                continue
            name = match.group(1)
            expected = (3 if name in {'SIrange', 'qtyrange'} else 2 if name in {'SI', 'qty', 'numrange', 'SIlist', 'qtylist'} else 1) if name in NUMBER_COMMANDS else None
            max_required = 1 if name in CITATIONS | REFERENCES | {'begin', 'end'} else expected
            groups, end, complete = arguments(text, match.end(), max_required)
            if not complete:
                self.warn('unclosed_command_argument', cursor, end, 'Unclosed argument or nesting beyond 128 groups for ' + name + '.')
                mask_region(chars, cursor, end)
                break
            signature = match.group(0) + ''.join(text[a:b] for a, b in groups)
            required = [(a, b) for a, b in groups if text[a] == '{']
            if name in DYNAMIC_COMMANDS:
                self.warn('dynamic_latex', cursor, end, 'Macro expansion/external input is not executed: ' + name + '.')
            if name in CITATIONS:
                if not required:
                    self.warn('missing_citation_argument', cursor, end, 'Citation has no braced keys.')
                else:
                    a, b = required[0]
                    keys = [key.strip() for key in text[a + 1:b - 1].split(',') if key.strip()]
                    if not keys:
                        self.warn('empty_citation_argument', a, b, 'Citation key list is empty.')
                    if any(not key.strip() for key in text[a + 1:b - 1].split(',')):
                        self.warn('invalid_citation_key_list', a, b, 'Citation key list contains an empty key.')
                    signature = match.group(0) + ''.join(text[x:y] for x, y in groups if x != a) + '{' + ','.join(keys) + '}'
                    # A key item retains the complete command signature as well:
                    # changing command type/options/order cannot pass silently.
                    for key in keys:
                        self.add('citations', cursor, end, signature + '::key=' + key, key=key, command=name)
                mask_region(chars, cursor, end)
                cursor = end
                continue
            if name in REFERENCES:
                if not required:
                    self.warn('missing_reference_argument', cursor, end, 'Reference has no braced target.')
                elif not text[required[0][0] + 1:required[0][1] - 1].strip():
                    self.warn('empty_reference_argument', cursor, end, 'Reference target is empty.')
                self.add('cross_references', cursor, end, signature, command=name)
                mask_region(chars, cursor, end)
                cursor = end
                continue
            if name in NUMBER_COMMANDS:
                if len(required) != expected:
                    self.warn('invalid_numeric_arguments', cursor, end, 'Numeric command argument count is unsupported or incomplete.')
                numeric_groups = required if name in {'num', 'numrange', 'numlist'} else required[:-1]
                for a, b in numeric_groups:
                    body = text[a + 1:b - 1]
                    values = body.split(';') if name in {'numlist', 'SIlist', 'qtylist'} else [body]
                    if not all(ATOM.fullmatch(value.strip()) for value in values):
                        self.warn('unsupported_numeric_argument', a, b, 'Numeric command argument is not a supported literal number/list.')
                if any(not text[a + 1:b - 1].strip() for a, b in required):
                    self.warn('empty_numeric_argument', cursor, end, 'Numeric or unit argument is empty.')
                self.add('numbers', cursor, end, normalize_numeric_command(signature), command=name)
                mask_region(chars, cursor, end)
                cursor = end
                continue
            if name in {'begin', 'end'}:
                if required:
                    a, b = required[0]
                    environment = text[a + 1:b - 1].rstrip('*')
                    if environment not in PROSE_ENVS and environment not in MATH_ENVS and environment not in CODE_ENVS:
                        self.warn('unsupported_environment', cursor, end, 'Environment is scanned as text without expansion: ' + environment + '.')
                mask_region(chars, cursor, end)
                cursor = end
                continue
            if name not in KNOWN_COMMANDS:
                if not groups and text[end:].lstrip() and text[end:].lstrip()[0].isalpha():
                    self.warn('unknown_macro_arity', cursor, end, 'Unbraced arguments or expansion of custom macro cannot be determined: ' + name + '.')
                self.add('custom_macros', cursor, end, signature, command=name)
                mask_region(chars, cursor, end)
                cursor = end
                continue
            # Formatting commands retain their contents for prose extraction;
            # exclude only command names so syntax digits cannot become values.
            if name not in {'le', 'leq', 'ge', 'geq', 'neq', 'approx', 'pm', 'mp', 'times', 'cdot', 'div'}:
                mask_region(chars, cursor, match.end())
            cursor = match.end()
        return ''.join(chars)

    def prose(self, text: str) -> None:
        chars = list(text)
        for match in STRUCTURE.finditer(text):
            self.add('structural_references', match.start(), match.end(), match.group('kind').lower() + ':' + match.group('id'))
            mask_region(chars, match.start(), match.end())
        text = self.intervals(''.join(chars))
        chars = list(text)
        for match in BRACKET.finditer(text):
            # A confidence interval/range is numeric evidence, not a reference.
            prefix = text[max(0, match.start() - 80):match.start()]
            if INTERVAL_CONTEXT.search(prefix):
                continue
            self.add('bracket_citations', match.start(), match.end(), re.sub(r'\s+', '', match.group(0)))
            mask_region(chars, match.start(), match.end())
        for match in AUTHOR_YEAR.finditer(text):
            self.add('author_year_citations', match.start(), match.end(), re.sub(r'\s+', ' ', match.group(0)))
            mask_region(chars, match.start(), match.end())
        text = ''.join(chars)
        for match in ENTITY.finditer(text):
            self.add('named_entities', match.start(), match.end(), match.group(0))
            # Names like ResNet-50 carry their own complete identity.
            mask_region(chars, match.start(), match.end())
        self.numbers(''.join(chars))

    def warn_linewrapped_operand(self, text: str, start: int, end: int, limit: int) -> None:
        """Do not claim coverage when a unit/operator resumes on another line.

        Newlines also delimit paragraphs, list items and contexts. Keep the
        horizontal parser conservative instead of silently joining those regions.
        """
        gap = LINEWRAP_SPACE.match(text, end, limit)
        if gap:
            continuation = UNIT.match(text, gap.end(), limit) or NUMERIC_LINK.match(text, gap.end(), limit)
            if continuation:
                self.warn('linewrapped_numeric_relationship', start, continuation.end(),
                          'Unit or numeric operator resumes after a line break; the relationship requires manual review.')

    def operand(self, text: str, start: int, limit: Optional[int] = None) -> Optional[Tuple[str, int]]:
        """One literal, its power, then its unit; no operator is consumed here."""
        limit = len(text) if limit is None else limit
        atom = ATOM.match(text, start, limit)
        if not atom:
            return None
        value, end = normalize_atom(atom.group(0)), atom.end()
        power = POWER.match(text, end, limit)
        if power:
            value += normalize_atom(power.group(0))
            end = power.end()
        probe = end
        while probe < limit and text[probe] in NUMERIC_SPACE:
            probe += 1
        unit = UNIT.match(text, probe, limit)
        if unit:
            self.warn_linewrapped_operand(text, start, unit.end(), limit)
            return value + ' ' + normalize_unit(unit.group(0)), unit.end()
        unknown = UNKNOWN_UNIT.match(text, probe, limit)
        count_noun = COUNT_NOUN.match(text, unknown.end(), limit) if unknown else None
        if unknown and unknown.group(0).lower() not in PROSE_WORDS and not count_noun:
            end = unknown.end()
            value += ' unknown-unit:' + unknown.group(0)
            self.warn('unrecognized_unit_candidate', probe, end, 'Adjacent token preserved, but its unit meaning is not recognized.')
        self.warn_linewrapped_operand(text, start, end, limit)
        return value, end

    def intervals(self, text: str) -> str:
        """Bind explicit CI/interval/range endpoint brackets before citations.

        Only labelled, two-endpoint literal intervals are recognized here.
        Unlabelled [1,2] remains a citation. Ambiguous/malformed labelled input
        gets a warning rather than having its parentheses silently discarded.
        """
        folded = fold_width(text)
        chars = list(text)
        covered_until = 0
        for opening in re.finditer(r'[\[(]', folded):
            start = opening.start()
            if start < covered_until or escaped(folded, start):
                continue
            if not INTERVAL_CONTEXT.search(folded[max(0, start - 80):start]):
                continue
            # Bounded lookahead; this scanner does not parse nested intervals.
            closing = re.search(r'[\])\r\n]', folded[start + 1:start + 513])
            if not closing or closing.group(0) in '\r\n':
                self.warn('unsupported_interval', start, min(start + 513, len(text)), 'Labelled interval is unclosed or exceeds the literal interval bound.')
                continue
            close = start + 1 + closing.start()
            commas = [i for i in range(start + 1, close) if folded[i] == ',']
            values = []
            if len(commas) == 1:
                for left, right in [(start + 1, commas[0]), (commas[0] + 1, close)]:
                    while left < right and folded[left] in NUMERIC_SPACE:
                        left += 1
                    while right > left and folded[right - 1] in NUMERIC_SPACE:
                        right -= 1
                    item = self.operand(folded, left, right)
                    if item and item[1] == right:
                        values.append(item[0])
            if len(values) != 2:
                self.warn('unsupported_interval', start, close + 1, 'Labelled interval requires two literal endpoints separated by one comma; nested/symbolic endpoints and ambiguous thousands separators are not interpreted.')
                continue
            end = close + 1
            self.add('numbers', start, end, 'interval:' + folded[start] + ','.join(values) + folded[close], numeric_kind='interval')
            mask_region(chars, start, end)
            covered_until = end
        return ''.join(chars)

    def numbers(self, text: str) -> None:
        # Width folding is character-for-character: original offsets survive.
        folded = fold_width(text)
        cursor = 0
        while cursor < len(folded):
            match = ATOM.match(folded, cursor)
            if not match:
                cursor += 1
                continue
            prefix_start = max(0, cursor - 16)
            relation = RELATION_BEFORE.search(folded[prefix_start:cursor])
            gap_start = cursor
            while gap_start and folded[gap_start - 1] in NUMERIC_SPACE + '\r\n':
                gap_start -= 1
            if '\n' in folded[gap_start:cursor] or '\r' in folded[gap_start:cursor]:
                preceding_start = max(0, gap_start - 16)
                preceding = RELATION_BEFORE.search(folded[preceding_start:gap_start])
                if preceding:
                    self.warn('linewrapped_numeric_relationship', preceding_start + preceding.start(), match.end(),
                              'Comparison and numeric bound are separated by a line break; the relationship requires manual review.')
            # Latin identifiers/model labels are outside bare number coverage;
            # unlike \w this intentionally permits adjacent CJK prose. A TeX
            # control word ends before a digit, so \leq0.05 needs no space.
            if not relation and cursor and (folded[cursor - 1].isascii() and (folded[cursor - 1].isalpha() or folded[cursor - 1] == '_')):
                cursor = match.end()
                continue
            start = match.start()
            value, end = self.operand(folded, start)
            # Bind immediately preceding comparison operator to this value.
            if relation:
                start = prefix_start + relation.start()
                value = normalize_relation(relation.group(1)) + value
            # Each operand owns its power and unit before an operator joins it
            # to the next. Preserve range punctuation separately from minus:
            # subtraction and a word such as "to" are not interchangeable.
            while True:
                link = NUMERIC_LINK.match(folded, end)
                if not link:
                    break
                token = link.group(1)
                connector = normalize_numeric_link(token)
                wrapped_operand = LINEWRAP_SPACE.match(folded, link.end(1))
                if wrapped_operand:
                    self.warn('linewrapped_numeric_relationship', start, wrapped_operand.end(),
                              'Numeric operator and following operand are separated by a line break; the relationship requires manual review.')
                following = self.operand(folded, link.end())
                if not following:
                    # A numeric bound may precede a symbolic side: 5 < x.
                    # Keep that comparison even when x is not a literal number.
                    if re.fullmatch(RELATION_TOKEN, token):
                        value += connector
                        end = link.end(1)
                        # Ending punctuation is not a symbolic operand. Inspect
                        # only its first non-space character, without repeatedly
                        # copying the remaining manuscript for each comparison.
                        probe = link.end()
                        while probe < len(folded) and folded[probe].isspace():
                            probe += 1
                        if probe == len(folded) or folded[probe] in '.,;:!?。；，：！？)]':
                            self.warn('incomplete_numeric_relation', start, end, 'Comparison has no following operand.')
                    else:
                        value += connector
                        end = link.end(1)
                        self.warn('unsupported_numeric_relation', start, end, 'Arithmetic/range operand is not a supported literal number.')
                    break
                value += connector + following[0]
                end = following[1]
            self.add('numbers', start, end, value)
            cursor = end

    def scan(self) -> Extraction:
        clean = self.exclusions()
        clean = self.math(clean)
        clean = self.commands(clean)
        self.prose(clean)
        for items in self.items.values():
            items.sort(key=lambda item: (item['start'], item['end']))
        total = sum(len(items) for items in self.items.values())
        coverage = {
            'status': 'INSUFFICIENT' if self.warnings or not total else 'RECOGNIZED_ITEMS_ONLY',
            'recognized_count': total,
            'warnings': self.warnings,
            'excluded_regions': self.excluded,
            'semantic_verification': False,
            'scope': 'Static lexical comparison; no macro expansion, external inputs, or full semantic verification.',
        }
        if not total:
            coverage['warnings'] = self.warnings + [{'kind': 'zero_coverage', 'start': 0, 'end': len(self.text), 'detail': 'No supported protected items were recognized.'}]
        return Extraction(self.items, coverage)


def normalize_atom(value: str) -> str:
    return value.replace('−', '-').replace(',', '').replace('E', 'e')


def fold_width(text: str) -> str:
    return ''.join(chr(ord(char) - 0xFEE0) if '\uff01' <= char <= '\uff5e' else char for char in text)


def normalize_numeric_link(value: str) -> str:
    return {'\\pm': '±', '+/-': '±', '\\mp': '∓', '\\times': '×', '\\cdot': '·', '\\div': '÷', '−': '-', 'to': ' to '}.get(value, normalize_relation(value))


def normalize_relation(value: str) -> str:
    return {'<=': '≤', '>=': '≥', '!=': '≠', '\\le': '≤', '\\leq': '≤', '\\ge': '≥', '\\geq': '≥', '\\neq': '≠', '\\approx': '≈'}.get(value, value)


def normalize_unit(value: str) -> str:
    value = value.replace('\\%', '%').replace('µ', 'μ')
    value = re.sub(r'\s*([/·⋅])\s*', r'\1', value)
    return re.sub(r'\s+', ' ', value)


def normalize_numeric_command(value: str) -> str:
    # Commands/options/units remain opaque protected syntax. Only numeric
    # spelling and layout spaces outside arguments are normalized.
    return re.sub(r'(?<=\{)[+\-−]?(?:\d+(?:\.\d+)?)(?:[eE][+\-−]?\d+)?(?=\})', lambda m: normalize_atom(m.group(0)), value)


def extract_document(text: str) -> Extraction:
    if not isinstance(text, str):
        raise TypeError('Manuscript input must be a string.')
    return Scanner(text).scan()
