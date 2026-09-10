"""Bounded static prose masking. Never expands, compiles or executes TeX.

Every masked character becomes a space except newlines, so original offsets
remain valid. Text environments/formatting arguments survive; math, comments
and code are excluded. Unknown constructions are reported as coverage limits.
"""
from __future__ import annotations

import re

MATH_ENVS = {'equation', 'align', 'alignat', 'gather', 'multline', 'eqnarray',
             'displaymath', 'math', 'split', 'aligned', 'gathered', 'cases'}
CODE_ENVS = {'verbatim', 'Verbatim', 'lstlisting', 'minted', 'comment'}
TEXT_ENVS = {'document', 'abstract', 'itemize', 'enumerate', 'description',
             'quote', 'quotation', 'center', 'flushleft', 'flushright',
             'theorem', 'lemma', 'proof', 'proposition', 'corollary', 'remark'}
TEXT_COMMANDS = {'textbf', 'textit', 'emph', 'texttt', 'textrm', 'textsc',
                 'textsf', 'underline', 'section', 'subsection', 'subsubsection',
                 'paragraph', 'subparagraph', 'title', 'caption', 'footnote',
                 'text', 'mbox', 'MakeUppercase', 'MakeLowercase'}
OPAQUE_COMMANDS = {'documentclass', 'usepackage', 'includegraphics', 'bibliography',
                   'bibliographystyle', 'label', 'ref', 'eqref', 'autoref', 'cref',
                   'Cref', 'pageref', 'nameref', 'cite', 'citep', 'citet', 'citeauthor',
                   'citeyear', 'autocite', 'parencite', 'footcite', 'nocite', 'url',
                   'input', 'include', 'newcommand', 'renewcommand', 'providecommand',
                   'def', 'let', 'write', 'write18', 'special', 'hspace', 'vspace'}


def escaped(text, index):
    n = 0
    while index > 0 and text[index - 1] == '\\':
        n += 1
        index -= 1
    return n % 2 == 1


def group_end(text, start, left='{', right='}'):
    depth, i = 1, start + 1
    while i < len(text):
        if text[i] == '%' and not escaped(text, i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end + 1
            continue
        if not escaped(text, i):
            if text[i] == left:
                depth += 1
            elif text[i] == right:
                depth -= 1
                if not depth:
                    return i + 1
        i += 1
    return None


def mask_prose(text):
    out, warnings, excluded = list(text), [], []
    text_env_stack = []
    # Establish TeX context while scanning actual source, never from code examples.
    is_tex = False

    def mask(start, end, kind):
        for pos in range(start, end):
            if text[pos] not in '\r\n':
                out[pos] = ' '
        excluded.append({'start': start, 'end': end, 'kind': kind})

    def warn(start, reason):
        warnings.append({'start': start, 'line': text.count('\n', 0, start) + 1, 'reason': reason})

    i = 0
    while i < len(text):
        # Fenced and inline Markdown code. An unclosed fence masks the remainder.
        if (i == 0 or text[i - 1] == '\n'):
            match = re.match(r' {0,3}(`{3,}|~{3,})[^\n]*', text[i:])
            if match:
                marker = match.group(1)
                end = re.search(r'(?m)^ {0,3}' + re.escape(marker[0]) + '{' + str(len(marker)) + r',}[ \t]*(?:\n|$)', text[i + match.end():])
                stop = i + match.end() + end.end() if end else len(text)
                if not end:
                    warn(i, 'Unclosed Markdown code fence')
                mask(i, stop, 'code'); i = stop; continue
        if text[i] == '`' and not escaped(text, i):
            match = re.match(r'`+', text[i:]); marker = match.group()
            stop = text.find(marker, i + len(marker))
            if stop >= 0:
                stop += len(marker); mask(i, stop, 'code'); i = stop; continue
        if text[i] == '%' and not escaped(text, i) and (is_tex or not text[text.rfind('\n', 0, i) + 1:i].strip()):
            stop = text.find('\n', i)
            stop = len(text) if stop < 0 else stop
            mask(i, stop, 'comment'); i = stop; continue
        if text[i] == '$' and not escaped(text, i) or text.startswith(('\\(', '\\['), i) and not escaped(text, i):
            opener = '$$' if text.startswith('$$', i) else text[i:i+2] if text[i] == '\\' else '$'
            closer = {'\\(': '\\)', '\\[': '\\]'}.get(opener, opener)
            j = i + len(opener)
            while True:
                stop = text.find(closer, j)
                if stop < 0 or not escaped(text, stop):
                    break
                j = stop + len(closer)
            if stop < 0:
                warn(i, 'Unclosed math delimiter'); stop = len(text)
            else:
                stop += len(closer)
            mask(i, stop, 'math'); i = stop; continue
        if text[i] == '\\' and not escaped(text, i):
            if re.match(r'\\(?:documentclass|begin|section|subsection|textbf|emph)(?![A-Za-z@])', text[i:]):
                is_tex = True
            env = re.match(r'\\(begin|end)\s*\{([^{}]+)\}', text[i:])
            if env:
                name = env.group(2); base = name.rstrip('*'); stop = i + env.end()
                if env.group(1) == 'begin' and base in MATH_ENVS | CODE_ENVS:
                    closing = re.search(r'\\end\s*\{' + re.escape(name) + r'\}', text[stop:])
                    if closing:
                        stop += closing.end()
                    else:
                        warn(i, 'Unclosed excluded environment: ' + name); stop = len(text)
                    mask(i, stop, 'math' if base in MATH_ENVS else 'code')
                else:
                    mask(i, stop, 'markup')
                    if env.group(1) == 'begin':
                        text_env_stack.append((name, i))
                    elif text_env_stack and text_env_stack[-1][0] == name:
                        text_env_stack.pop()
                    else:
                        warn(i, 'Unmatched or mismatched environment end: ' + name)
                    if base not in TEXT_ENVS:
                        warn(i, 'Environment semantics not interpreted: ' + name)
                i = stop; continue
            command = re.match(r'\\([A-Za-z@]+)\*?', text[i:])
            if command:
                name = command.group(1); stop = i + command.end()
                if name in {'verb', 'lstinline'} and stop < len(text):
                    delimiter = text[stop]; end = text.find(delimiter, stop + 1)
                    if end < 0:
                        warn(i, 'Unclosed inline verbatim'); end = len(text) - 1
                    mask(i, end + 1, 'code'); i = end + 1; continue
                mask(i, stop, 'markup')
                j = stop
                while j < len(text) and text[j] in ' \t':
                    j += 1
                if j < len(text) and text[j] == '[':
                    end = group_end(text, j, '[', ']')
                    if end is None:
                        warn(j, 'Unclosed command option'); end = len(text)
                    mask(j, end, 'markup'); j = end
                if name in {'input', 'include', 'def', 'let', 'write', 'write18', 'special'}:
                    warn(i, 'External input or executable TeX command not evaluated: ' + name)
                if name in TEXT_COMMANDS and j < len(text) and text[j] == '{' and group_end(text, j) is None:
                    warn(j, 'Unclosed text command argument')
                if name in OPAQUE_COMMANDS:
                    last_end = stop
                    mandatory = 0
                    arity = 2 if name in {'newcommand', 'renewcommand', 'providecommand'} else 1
                    while j < len(text):
                        while j < len(text) and text[j].isspace():
                            j += 1
                        if j >= len(text) or text[j] not in '{[':
                            break
                        if text[j] == '{':
                            mandatory += 1
                        end = group_end(text, j, text[j], '}' if text[j] == '{' else ']')
                        if end is None:
                            warn(j, 'Unclosed command argument'); end = len(text)
                        mask(j, end, 'markup'); j = end; last_end = end
                        if mandatory >= arity:
                            break
                    mask(i, last_end, 'markup')
                    i = last_end; continue
                if name not in TEXT_COMMANDS | {'item', 'par', 'newline', 'centering', 'small', 'large'}:
                    warn(i, 'Command not expanded; arguments treated as source text: ' + name)
                i = stop; continue
            if i + 1 < len(text) and text[i + 1] in '%&_#$ {}':
                mask(i, i + 1, 'markup'); i += 2; continue
            mask(i, min(i + 2, len(text)), 'markup'); i += 2; continue
        if text[i] in '{}':
            mask(i, i + 1, 'markup')
        i += 1
    for name, start in text_env_stack:
        warn(start, 'Unclosed text environment: ' + name)
    return ''.join(out), warnings, excluded


def sentence_spans(text):
    """Offsets for prose sentences, preserving decimal points and common abbreviations."""
    boundaries = [0]
    for match in re.finditer(r'[.!?。！？]|\n[ \t]*\n', text):
        pos = match.start(); char = text[pos]
        if char == '.':
            if pos and pos + 1 < len(text) and text[pos - 1].isdigit() and text[pos + 1].isdigit():
                continue
            prefix = text[max(0, pos - 12):pos + 1]
            if re.search(r'(?:\b(?:Mr|Mrs|Ms|Dr|Prof|Fig|Eq|Sec|vs|al)|\be\.g|\bi\.e|\betc)\.$', prefix, re.I):
                continue
            if pos + 1 < len(text) and not text[pos + 1].isspace():
                continue
            if re.search(r'\b[A-Z]\.$', prefix):
                continue
        boundaries.append(match.end())
    boundaries.append(len(text))
    for left, right in zip(boundaries, boundaries[1:]):
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if left < right:
            yield left, right, text[left:right]
