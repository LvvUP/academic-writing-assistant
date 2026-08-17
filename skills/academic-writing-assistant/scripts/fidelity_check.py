#!/usr/bin/env python3
"""Verify that protected content survived a rewrite.

Citations, numbers, equations, and cross-references are exactly the tokens that
proofreading skips: a dropped ``\\cite{}`` still compiles, and a changed decimal
still reads fluently. This compares the before and after text and reports what
actually happened to each protected item, so the author gets evidence instead of
reassurance.

Extraction is intentionally conservative. It reports what changed and leaves the
judgement to a human -- a diff here is a question, not a verdict.

Usage::

    python fidelity_check.py --before original.tex --after revised.tex
    python fidelity_check.py --before a.md --after b.md --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


# Each pattern captures one class of locked-zone content. Order matters only for
# readability of the report; extraction is independent per category.
PATTERNS: Dict[str, str] = {
    # \cite{a,b}, \citep{}, \citet{}, \autocite{}, \parencite{}, \footcite{}
    "citation_command": r"\\(?:cite|citep|citet|citeauthor|citeyear|autocite|parencite|footcite|nocite)\*?(?:\[[^\]]*\])*\{([^}]*)\}",
    # \ref{}, \eqref{}, \autoref{}, \cref{}, \Cref{}, \pageref{}, \label{}
    "cross_reference": r"\\(?:ref|eqref|autoref|cref|Cref|pageref|nameref|label)\{([^}]*)\}",
    # Numeric citation markers such as [12] or [3, 5-7] in non-LaTeX drafts
    "bracket_citation": r"(?<!\\)\[(\d+(?:\s*[-,–]\s*\d+)*)\]",
    # Author-year markers: (Zhang et al., 2021), (Smith & Lee, 2019)
    "author_year": r"\(([A-Z][A-Za-z\u00C0-\u024F'’-]+(?:\s+(?:et\s+al\.?|and|&)\s*[A-Za-z\u00C0-\u024F'’-]*)?,?\s*\d{4}[a-z]?)\)",
    # Section 3.2, Table 4, Fig. 5, Figure 1, Eq. (2), Algorithm 1, Appendix B
    "structural_reference": r"\b(?:Section|Sect\.|Sec\.|Table|Tab\.|Figure|Fig\.|Equation|Eq\.|Algorithm|Alg\.|Appendix|Chapter|附录|第\s*\d+\s*[节章])\s*~?\s*\(?([0-9]+(?:\.[0-9]+)*|[A-Z](?:\.[0-9]+)*)\)?",
}

# Math environments and inline math, captured as opaque blocks.
MATH_PATTERNS: Sequence[str] = (
    r"\$\$(.+?)\$\$",
    r"(?<!\$)\$([^$\n]+?)\$(?!\$)",
    r"\\\((.+?)\\\)",
    r"\\\[(.+?)\\\]",
    r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|split)\}(.*?)\\end\{\1\}",
)

# Numbers that carry evidence: 92.3, 1,024, 45%, 3.2e-4, 89.2±0.3
NUMBER_PATTERN = (
    r"(?<![\w.])"
    r"(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+)"
    r"\s*(?:[eE][-+]?\d+)?"
    r"\s*(%|±|‰)?"
    r"(?![\w.]*\d)"
)

# Dataset, benchmark, and model names -- LEVIR-CD, ImageNet, U-Net, ResNet-50,
# CIFAR-10, COCO. These are locked-zone content but carry no digits of their
# own, so the numeric check misses them entirely. Requiring an internal capital,
# a digit, or a hyphenated capital keeps ordinary sentence-initial words out.
NAMED_ENTITY_PATTERN = (
    r"(?<![\w-])"
    r"("
    r"[A-Z][A-Za-z]*(?:-[A-Z0-9][A-Za-z0-9]*)+"       # LEVIR-CD, U-Net, ResNet-50
    r"|[A-Z]{2,}[A-Za-z0-9]*"                          # COCO, ADE20K, MSFF
    r"|[A-Z][a-z]+[A-Z][A-Za-z0-9]*"                   # ImageNet, DeepLab
    r"|[A-Z][A-Za-z]+\d+[A-Za-z0-9]*"                  # S2Looking, VGG16
    r")"
    r"(?![\w-])"
)

# A LaTeX command that is not one of the known citation/reference/math kinds is
# very likely an author macro such as \ours{} or \method{}. Losing one silently
# changes the method name throughout the paper.
MACRO_PATTERN = r"\\([a-zA-Z@]+)\*?(?:\{|\s|$)"

KNOWN_COMMANDS = {
    "cite", "citep", "citet", "citeauthor", "citeyear", "autocite", "parencite",
    "footcite", "nocite", "ref", "eqref", "autoref", "cref", "Cref", "pageref",
    "nameref", "label", "begin", "end", "section", "subsection", "subsubsection",
    "paragraph", "textbf", "textit", "emph", "texttt", "textrm", "textsc",
    "item", "footnote", "caption", "includegraphics", "left", "right", "quad",
    "qquad", "hspace", "vspace", "newline", "par", "centering", "small",
    "large", "Large", "huge", "text", "mathrm", "mathbf", "mathcal", "frac",
    "sum", "int", "sqrt", "alpha", "beta", "gamma", "delta", "epsilon", "theta",
    "lambda", "mu", "sigma", "phi", "psi", "omega", "times", "cdot", "leq",
    "geq", "neq", "approx", "in", "hat", "tilde", "bar", "vec", "mathbb",
    "operatorname", "log", "exp", "max", "min", "argmax", "argmin",
}


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def extract(pattern: str, text: str, group: int = 1) -> List[str]:
    """Return every match of ``pattern``, normalized for whitespace."""
    found: List[str] = []
    for match in re.finditer(pattern, text, re.DOTALL):
        try:
            value = match.group(group)
        except IndexError:
            value = match.group(0)
        if value is None:
            continue
        found.append(re.sub(r"\s+", " ", value).strip())
    return [item for item in found if item]


def extract_citation_keys(text: str) -> List[str]:
    """Split multi-key citations so \\cite{a,b} counts as two protected keys."""
    keys: List[str] = []
    for group in extract(PATTERNS["citation_command"], text):
        keys.extend(key.strip() for key in group.split(",") if key.strip())
    return keys


def extract_math(text: str) -> List[str]:
    blocks: List[str] = []
    for pattern in MATH_PATTERNS:
        for match in re.finditer(pattern, text, re.DOTALL):
            body = match.group(match.lastindex or 0) or ""
            normalized = re.sub(r"\s+", "", body)
            if normalized:
                blocks.append(normalized)
    return blocks


def extract_numbers(text: str) -> List[str]:
    """Numbers with their unit suffix, excluding math, commands, and citations.

    Citation markers are stripped first because their digits are already tracked
    as citations; counting them again would report one dropped reference twice
    and bury the numbers that carry evidence.
    """
    stripped = text
    for pattern in MATH_PATTERNS:
        stripped = re.sub(pattern, " ", stripped, flags=re.DOTALL)
    stripped = re.sub(PATTERNS["bracket_citation"], " ", stripped)
    stripped = re.sub(PATTERNS["author_year"], " ", stripped)
    # Drop LaTeX command names so \section2 style tokens do not register.
    stripped = re.sub(r"\\[a-zA-Z@]+", " ", stripped)
    numbers: List[str] = []
    for match in re.finditer(NUMBER_PATTERN, stripped):
        value = match.group(1)
        suffix = match.group(2) or ""
        numbers.append(f"{value}{suffix}")
    return numbers


def extract_macros(text: str) -> List[str]:
    return [
        name
        for name in re.findall(MACRO_PATTERN, text)
        if name not in KNOWN_COMMANDS
    ]


def extract_named_entities(text: str) -> List[str]:
    """Dataset, benchmark, and model names, excluding math and LaTeX commands."""
    stripped = text
    for pattern in MATH_PATTERNS:
        stripped = re.sub(pattern, " ", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\\[a-zA-Z@]+", " ", stripped)
    stripped = re.sub(PATTERNS["citation_command"], " ", stripped)
    stripped = re.sub(PATTERNS["cross_reference"], " ", stripped)
    return re.findall(NAMED_ENTITY_PATTERN, stripped)


def compare(before: List[str], after: List[str]) -> Dict[str, List[str]]:
    """Multiset comparison: repeated items must survive the same number of times."""
    before_counts = Counter(before)
    after_counts = Counter(after)
    missing: List[str] = []
    added: List[str] = []
    for item, count in before_counts.items():
        delta = count - after_counts.get(item, 0)
        if delta > 0:
            missing.extend([item] * delta)
    for item, count in after_counts.items():
        delta = count - before_counts.get(item, 0)
        if delta > 0:
            added.extend([item] * delta)
    return {
        "before_count": len(before),
        "after_count": len(after),
        "missing": sorted(set(missing)),
        "added": sorted(set(added)),
    }


def build_report(before: str, after: str) -> Dict[str, Dict]:
    categories: Dict[str, Tuple[List[str], List[str]]] = {
        "citations": (extract_citation_keys(before), extract_citation_keys(after)),
        "bracket_citations": (
            extract(PATTERNS["bracket_citation"], before),
            extract(PATTERNS["bracket_citation"], after),
        ),
        "author_year_citations": (
            extract(PATTERNS["author_year"], before),
            extract(PATTERNS["author_year"], after),
        ),
        "cross_references": (
            extract(PATTERNS["cross_reference"], before),
            extract(PATTERNS["cross_reference"], after),
        ),
        "structural_references": (
            extract(PATTERNS["structural_reference"], before),
            extract(PATTERNS["structural_reference"], after),
        ),
        "math_blocks": (extract_math(before), extract_math(after)),
        "numbers": (extract_numbers(before), extract_numbers(after)),
        "named_entities": (
            extract_named_entities(before),
            extract_named_entities(after),
        ),
        "custom_macros": (extract_macros(before), extract_macros(after)),
    }
    return {
        name: compare(before_items, after_items)
        for name, (before_items, after_items) in categories.items()
    }


LABELS = {
    "citations": "LaTeX citation keys",
    "bracket_citations": "Bracket citations [n]",
    "author_year_citations": "Author-year citations",
    "cross_references": "\\ref / \\label targets",
    "structural_references": "Section / Table / Figure references",
    "math_blocks": "Math blocks",
    "numbers": "Numeric values",
    "named_entities": "Dataset / model / benchmark names",
    "custom_macros": "Custom macros",
}

PREVIEW_LIMIT = 12


def render(report: Dict[str, Dict]) -> Tuple[str, bool]:
    lines = ["# Fidelity Check Report", ""]
    problems: List[Tuple[str, Dict]] = [
        (name, data)
        for name, data in report.items()
        if data["missing"] or data["added"]
    ]

    if not problems:
        total = sum(data["before_count"] for data in report.values())
        lines.append(f"Status: PASS — all {total} protected items preserved.")
        lines.extend(["", "| Category | Count |", "|---|---|"])
        for name, data in report.items():
            if data["before_count"]:
                lines.append(f"| {LABELS[name]} | {data['before_count']} |")
        lines.extend(
            [
                "",
                "This covers the categories listed above only. It does not confirm "
                "that claim strength was preserved -- hedges, scope conditions, and "
                "quantifiers need a separate read -- and lowercase proper nouns or "
                "prose descriptions of results are outside its reach.",
            ]
        )
        return "\n".join(lines) + "\n", True

    lines.append("Status: REVIEW NEEDED")
    lines.append("")
    lines.append(
        "The items below differ between the two versions. Confirm each one was "
        "intentional; unintended changes to citations, numbers, or equations are "
        "the failure mode this check exists to catch."
    )
    lines.append("")

    for name, data in problems:
        lines.append(f"## {LABELS[name]}")
        lines.append("")
        lines.append(
            f"Before: {data['before_count']} · After: {data['after_count']}"
        )
        lines.append("")
        if data["missing"]:
            lines.append("Missing from the revised text:")
            lines.append("")
            preview = data["missing"][:PREVIEW_LIMIT]
            lines.extend(f"- `{item}`" for item in preview)
            if len(data["missing"]) > PREVIEW_LIMIT:
                lines.append(f"- … and {len(data['missing']) - PREVIEW_LIMIT} more")
            lines.append("")
        if data["added"]:
            lines.append("Present only in the revised text:")
            lines.append("")
            preview = data["added"][:PREVIEW_LIMIT]
            lines.extend(f"- `{item}`" for item in preview)
            if len(data["added"]) > PREVIEW_LIMIT:
                lines.append(f"- … and {len(data['added']) - PREVIEW_LIMIT} more")
            lines.append("")

    lines.append("## Note")
    lines.append("")
    lines.append(
        "Some differences are legitimate: splitting a sentence can duplicate a "
        "reference, and rounding requested by the author changes a number. "
        "Report the reason rather than dismissing the finding."
    )
    return "\n".join(lines) + "\n", False


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that citations, numbers, equations, and references "
        "survived a rewrite."
    )
    parser.add_argument("--before", required=True, help="Original text file.")
    parser.add_argument("--after", required=True, help="Revised text file.")
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any protected item differs.",
    )
    args = parser.parse_args(argv)

    try:
        before = read_text(args.before)
        after = read_text(args.after)
    except OSError as exc:
        sys.stderr.write(f"Cannot read input: {exc}\n")
        return 2

    report = build_report(before, after)

    if args.json:
        sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        clean = not any(
            data["missing"] or data["added"] for data in report.values()
        )
    else:
        rendered, clean = render(report)
        sys.stdout.write(rendered)

    return 0 if clean or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
