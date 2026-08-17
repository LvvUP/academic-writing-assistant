#!/usr/bin/env python3
"""Whole-draft hygiene checks for academic manuscripts.

These are the errors that survive paragraph-level editing because they only
exist across a whole document: an abbreviation defined three sections after its
first use, a superlative with no statistical test behind it, an abstract two
hundred words over the venue limit.

Every finding is a prompt to look, not a verdict. Rule-based scanning cannot
know that a draft deliberately distinguishes two nearby terms, or that a
significance test appears in a table rather than the prose. Report findings as
questions for the author.

Usage::

    python manuscript_audit.py draft.md
    python manuscript_audit.py abstract.txt --limit-words 250
    python manuscript_audit.py highlights.txt --limit-chars 85 --per-line
    python manuscript_audit.py draft.tex --checks abbreviations,claims --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence


# --------------------------------------------------------------------------
# Claim-strength vocabulary
# --------------------------------------------------------------------------

# Words that assert statistical significance. In a paper these read as a claim
# that a test was run, so an author who never ran one is overclaiming without
# realizing it.
SIGNIFICANCE_TERMS = ("significantly", "significant", "statistically")

# Evidence that a test actually was performed somewhere in the text.
STATISTICAL_EVIDENCE = (
    "p <", "p<", "p =", "p=", "p-value", "p value", "t-test", "t test",
    "wilcoxon", "mann-whitney", "anova", "chi-square", "chi-squared",
    "bonferroni", "confidence interval", "95% ci", "std", "standard deviation",
    "±", "significance test", "显著性检验", "置信区间", "标准差",
)

# Absolute or unverifiable claims a reviewer will ask the author to defend.
SUPERLATIVE_PATTERNS = OrderedDict(
    (
        (r"\bstate[- ]of[- ]the[- ]art\b", "Bind to a named comparison set and date, or drop."),
        (r"\bthe first\b|\bwe are the first\b", "Nearly indefensible; consider 'to our knowledge, the first'."),
        (r"\boutperforms? all\b", "Requires comparison against every existing method."),
        (r"\bbest performance\b", "Specify on which datasets and against which baselines."),
        (r"\bsuperior to (?:all|existing|other)\b", "Unbounded comparison claim."),
        (r"\buniversally\b|\bin all cases\b|\balways achieves\b", "Absolute coverage claim."),
        (r"\bperfectly\b|\bcompletely solves?\b|\bfully solves?\b", "Overclaim; no method fully solves a research problem."),
        (r"首次(?:提出|实现)", "首次主张极难辩护，建议改为'据我们所知，首次'。"),
        (r"完美(?:解决|实现)", "宣传性表述，建议改为具体、可核查的描述。"),
        (r"彻底(?:解决|消除)", "绝对化表述，建议限定范围。"),
        (r"全面(?:超越|优于)", "无界比较主张，需绑定具体对比方法。"),
        (r"明显优于", "'明显'在论文语境中接近显著性主张；建议给出具体差值。"),
    )
)

# Causal verbs applied where the evidence is often only associational.
CAUSAL_PATTERNS = OrderedDict(
    (
        (r"\bcauses?\b|\bcaused by\b", "Causal claim — confirm the design supports causation."),
        (r"\bleads? to\b", "Causal phrasing; consider 'is associated with' for observational data."),
        (r"\bdue to\b", "Attributes cause; confirm this is established rather than inferred."),
        (r"导致", "断言因果；相关性证据建议改为'与……相关'。"),
    )
)

# Ceremonial openers that consume the most valuable sentence in the paper.
FILLER_PATTERNS = OrderedDict(
    (
        (r"[Ww]ith the rapid development of", "Ceremonial opener; start from the specific problem."),
        (r"[Ii]n recent years, with", "Ceremonial opener."),
        (r"[Ii]t is well known that", "Either common knowledge (cut) or needs a citation."),
        (r"[Pp]lays? an important role", "Vague; state the specific function."),
        (r"has important (?:theoretical )?significance", "Reads as an unsupported grand claim in English."),
        (r"随着.{0,12}的(?:快速|迅速)发展", "惯例性开头，建议直接从具体问题切入。"),
        (r"众所周知", "通常可删除。"),
        (r"具有重要的?(?:理论意义|应用价值|意义)", "空泛表述；建议改为具体贡献。"),
        (r"起到了?.{0,8}的作用", "建议还原为动词表述。"),
    )
)

# Stacked hedges: three or more in one sentence reads as evasion.
HEDGE_WORDS = (
    "may", "might", "could", "possibly", "potentially", "perhaps", "somewhat",
    "relatively", "to some extent", "in a certain sense", "arguably",
    "可能", "或许", "一定程度", "有所", "较为", "往往",
)


def read_text(path: Optional[str]) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def strip_markup(text: str) -> str:
    """Remove math and LaTeX commands so prose checks do not fire inside them."""
    cleaned = re.sub(r"\$\$.+?\$\$", " ", text, flags=re.DOTALL)
    cleaned = re.sub(r"(?<!\$)\$[^$\n]+?\$(?!\$)", " ", cleaned)
    cleaned = re.sub(r"\\begin\{(\w+\*?)\}.*?\\end\{\1\}", " ", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])*(?:\{[^}]*\})*", " ", cleaned)
    cleaned = re.sub(r"^\s*%.*$", " ", cleaned, flags=re.MULTILINE)
    return cleaned


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?。！？])\s+|\n{2,}", text)
    return [part.strip() for part in parts if part and part.strip()]


def locate(text: str, index: int) -> int:
    """1-based line number for a character offset."""
    return text.count("\n", 0, index) + 1


def excerpt(sentence: str, width: int = 110) -> str:
    collapsed = re.sub(r"\s+", " ", sentence).strip()
    if len(collapsed) <= width:
        return collapsed
    return collapsed[: width - 1] + "…"


# --------------------------------------------------------------------------
# Individual checks
# --------------------------------------------------------------------------


def check_abbreviations(text: str) -> List[Dict]:
    """Abbreviations used before definition, or defined but never reused.

    An abbreviation is treated as defined when it appears parenthesized after
    its expansion -- "convolutional neural network (CNN)" -- which is the
    convention every venue expects.
    """
    prose = strip_markup(text)
    findings: List[Dict] = []

    defined: Dict[str, int] = {}
    for match in re.finditer(r"\(([A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*)\)", prose):
        acronym = match.group(1)
        if acronym not in defined:
            defined[acronym] = match.start()

    usages: Dict[str, List[int]] = {}
    for match in re.finditer(r"(?<![A-Za-z0-9])([A-Z]{2,6}[0-9]{0,2})(?![A-Za-z0-9])", prose):
        usages.setdefault(match.group(1), []).append(match.start())

    for acronym, positions in sorted(usages.items()):
        if acronym not in defined:
            continue
        first_use = min(positions)
        definition = defined[acronym]
        if first_use < definition:
            use_line = locate(prose, first_use)
            def_line = locate(prose, definition)
            where = (
                f"is defined later on line {def_line}"
                if def_line != use_line
                else "is defined later in the same paragraph"
            )
            findings.append(
                {
                    "type": "abbreviation_used_before_definition",
                    "item": acronym,
                    "line": use_line,
                    "note": f"'{acronym}' is used on line {use_line} but {where}. "
                    "Move the definition to first use.",
                }
            )
        elif len(positions) <= 1:
            findings.append(
                {
                    "type": "abbreviation_defined_once",
                    "item": acronym,
                    "line": locate(prose, definition),
                    "note": f"'{acronym}' is defined but used only once. "
                    "Spelling it out costs the reader less than an abbreviation "
                    "they must remember.",
                }
            )

    for acronym in sorted(set(usages) - set(defined)):
        if len(usages[acronym]) >= 2 and acronym not in {"DOI", "URL", "PDF", "IEEE", "ACM"}:
            findings.append(
                {
                    "type": "abbreviation_never_defined",
                    "item": acronym,
                    "line": locate(prose, min(usages[acronym])),
                    "note": f"'{acronym}' is used {len(usages[acronym])} times without a "
                    "parenthesized definition. Confirm it is standard enough for the venue.",
                }
            )

    return findings


def check_claims(text: str) -> List[Dict]:
    """Superlatives, unearned significance language, and causal overreach."""
    prose = strip_markup(text)
    lowered = prose.lower()
    has_stats = any(marker in lowered for marker in STATISTICAL_EVIDENCE)
    findings: List[Dict] = []

    for sentence in split_sentences(prose):
        sentence_lower = sentence.lower()
        offset = prose.find(sentence)
        line = locate(prose, offset) if offset >= 0 else 0

        if not has_stats and any(term in sentence_lower for term in SIGNIFICANCE_TERMS):
            findings.append(
                {
                    "type": "significance_without_test",
                    "item": excerpt(sentence),
                    "line": line,
                    "note": "Uses significance language, but no statistical test appears "
                    "anywhere in the text. In a paper this reads as a claim that a test "
                    "was run. Use 'consistent' or report the difference directly, or add "
                    "the test.",
                }
            )

        for pattern, note in SUPERLATIVE_PATTERNS.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                findings.append(
                    {
                        "type": "unbounded_claim",
                        "item": excerpt(sentence),
                        "line": line,
                        "note": note,
                    }
                )
                break

        for pattern, note in CAUSAL_PATTERNS.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                findings.append(
                    {
                        "type": "causal_language",
                        "item": excerpt(sentence),
                        "line": line,
                        "note": note,
                    }
                )
                break

    return findings


def check_style(text: str) -> List[Dict]:
    """Ceremonial filler and stacked hedges."""
    prose = strip_markup(text)
    findings: List[Dict] = []

    for pattern, note in FILLER_PATTERNS.items():
        for match in re.finditer(pattern, prose):
            findings.append(
                {
                    "type": "filler",
                    "item": match.group(0),
                    "line": locate(prose, match.start()),
                    "note": note,
                }
            )

    for sentence in split_sentences(prose):
        lowered = sentence.lower()
        hits = [word for word in HEDGE_WORDS if word in lowered]
        if len(hits) >= 3:
            offset = prose.find(sentence)
            findings.append(
                {
                    "type": "hedge_stacking",
                    "item": excerpt(sentence),
                    "line": locate(prose, offset) if offset >= 0 else 0,
                    "note": f"Stacked hedges ({', '.join(hits[:4])}). One deliberate hedge "
                    "is stronger than several.",
                }
            )

    return findings


def check_tense(text: str) -> List[Dict]:
    """Paragraphs mixing method-present and experiment-past narration."""
    findings: List[Dict] = []
    paragraphs = [p for p in re.split(r"\n{2,}", strip_markup(text)) if p.strip()]

    past = re.compile(
        r"\b(?:we|the authors)\s+(?:\w+ed|ran|trained|used|conducted|performed|built|chose|set)\b",
        re.IGNORECASE,
    )
    present = re.compile(
        r"\b(?:we|the (?:proposed )?"
        r"(?:method|model|framework|network|encoder|decoder|module|architecture|"
        r"system|algorithm|approach|branch|backbone))\s+"
        r"(?:propose|present|introduce|use|extract|employ|adopt|consist|apply|"
        r"compute|produce|generate|aggregate|predict|learn|take|output)s?\b",
        re.IGNORECASE,
    )

    for paragraph in paragraphs:
        past_hits = past.findall(paragraph)
        present_hits = present.findall(paragraph)
        if past_hits and present_hits:
            offset = text.find(paragraph[:40])
            findings.append(
                {
                    "type": "mixed_tense",
                    "item": excerpt(paragraph, 90),
                    "line": locate(text, offset) if offset >= 0 else 0,
                    "note": "Mixes past-tense experimental narration with present-tense "
                    "method description. Convention: present for what the method does, "
                    "past for what was done and found.",
                }
            )

    return findings


def check_length(
    text: str,
    limit_words: Optional[int],
    limit_chars: Optional[int],
    per_line: bool,
) -> List[Dict]:
    """Word and character counts against a venue limit.

    Character limits count spaces -- Elsevier highlights are 85 characters
    including them -- so estimating instead of counting reliably overshoots.
    """
    findings: List[Dict] = []
    prose = strip_markup(text)

    if per_line:
        for number, line in enumerate(text.splitlines(), start=1):
            content = line.strip().lstrip("-*• ").strip()
            if not content:
                continue
            length = len(content)
            if limit_chars and length > limit_chars:
                findings.append(
                    {
                        "type": "line_over_limit",
                        "item": excerpt(content, 60),
                        "line": number,
                        "note": f"{length} characters including spaces, "
                        f"limit {limit_chars}. Over by {length - limit_chars}.",
                    }
                )
            else:
                findings.append(
                    {
                        "type": "line_count",
                        "item": excerpt(content, 60),
                        "line": number,
                        "note": f"{length} characters"
                        + (f" (limit {limit_chars})" if limit_chars else ""),
                    }
                )
        return findings

    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", prose))
    cjk = len(re.findall(r"[\u4e00-\u9fff]", prose))
    total_chars = len(prose.strip())

    summary = f"{words} English words"
    if cjk:
        summary += f", {cjk} Chinese characters"
    summary += f", {total_chars} characters including spaces"

    findings.append({"type": "count", "item": summary, "line": 0, "note": ""})

    counted = words + cjk
    if limit_words and counted > limit_words:
        findings.append(
            {
                "type": "over_word_limit",
                "item": f"{counted} / {limit_words}",
                "line": 0,
                "note": f"Over the limit by {counted - limit_words}. Cut intensifiers, "
                "nominalizations, and repeated content before touching hedges or scope "
                "conditions -- those carry the claim.",
            }
        )
    if limit_chars and total_chars > limit_chars:
        findings.append(
            {
                "type": "over_char_limit",
                "item": f"{total_chars} / {limit_chars}",
                "line": 0,
                "note": f"Over the limit by {total_chars - limit_chars} characters.",
            }
        )

    return findings


def check_terminology_drift(text: str) -> List[Dict]:
    """Nearby English terms that may denote one concept under two names."""
    prose = strip_markup(text).lower()
    findings: List[Dict] = []

    pairs = [
        ("feature fusion", "feature aggregation"),
        ("feature fusion", "feature merging"),
        ("proposed method", "our method"),
        ("dataset", "data set"),
        ("baseline", "benchmark method"),
        ("fine-tuning", "finetuning"),
        ("pre-training", "pretraining"),
        ("multi-scale", "multiscale"),
        ("state-of-the-art", "state of the art"),
    ]

    for first, second in pairs:
        first_count = prose.count(first)
        second_count = prose.count(second)
        if first_count and second_count:
            findings.append(
                {
                    "type": "terminology_drift",
                    "item": f"'{first}' ({first_count}×) / '{second}' ({second_count}×)",
                    "line": 0,
                    "note": "Both variants appear. Normalize to the dominant one unless "
                    "the draft distinguishes them deliberately.",
                }
            )

    return findings


CHECKS: "OrderedDict[str, Callable[[str], List[Dict]]]" = OrderedDict(
    (
        ("abbreviations", check_abbreviations),
        ("claims", check_claims),
        ("style", check_style),
        ("tense", check_tense),
        ("terminology", check_terminology_drift),
    )
)

SECTION_NOTES = {
    "abstract": "Abstracts carry the highest claim-inflation risk: they are written "
    "last, under a word limit, and read the most. Verify every claim here is no "
    "stronger than the results section supports.",
    "introduction": "Check that the stated gap connects to the contributions, and "
    "that novelty claims are defensible.",
    "method": "Check symbol definitions and that no architectural detail was supplied "
    "that the author did not provide.",
    "experiment": "Check that no metric value, dataset size, or baseline number "
    "originated anywhere other than the author.",
    "discussion": "Hedging is correct here. Check that limitations are real rather "
    "than decorative.",
    "rebuttal": "Check the promised-versus-done distinction: never state that an "
    "experiment was run or text was added unless the author confirmed it.",
}

TITLES = {
    "abbreviations": "Abbreviations",
    "claims": "Claim strength",
    "style": "Style and filler",
    "tense": "Tense consistency",
    "terminology": "Terminology drift",
    "length": "Length",
}


def render(results: "OrderedDict[str, List[Dict]]", section: Optional[str]) -> str:
    lines = ["# Manuscript Audit", ""]

    if section and section in SECTION_NOTES:
        lines.extend([f"Section: {section}", "", SECTION_NOTES[section], ""])

    total = sum(
        len([f for f in findings if f["type"] not in {"count", "line_count"}])
        for findings in results.values()
    )

    if total == 0 and "length" not in results:
        lines.append("No configured issues detected.")
        lines.extend(
            [
                "",
                "This scan is rule-based. It cannot see claim strength relative to "
                "evidence, fabricated content, or whether the argument holds. Those "
                "still need review.",
            ]
        )
        return "\n".join(lines) + "\n"

    for name, findings in results.items():
        if not findings:
            continue
        lines.append(f"## {TITLES.get(name, name.title())}")
        lines.append("")
        for finding in findings:
            location = f" (line {finding['line']})" if finding.get("line") else ""
            lines.append(f"- **{finding['item']}**{location}")
            if finding.get("note"):
                lines.append(f"  - {finding['note']}")
        lines.append("")

    lines.extend(
        [
            "## Note",
            "",
            "Findings are prompts to look, not verdicts. Rule-based scanning cannot "
            "tell a deliberate distinction from an accidental one, and it cannot "
            "detect the failures that matter most -- fabricated content and claims "
            "that outrun their evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Whole-draft hygiene checks for academic manuscripts."
    )
    parser.add_argument("file", nargs="?", help="Text file. Reads stdin when omitted.")
    parser.add_argument(
        "--checks",
        default="all",
        help="Comma-separated subset of: " + ", ".join(CHECKS) + ". Default: all.",
    )
    parser.add_argument("--limit-words", type=int, help="Word limit to check against.")
    parser.add_argument(
        "--limit-chars", type=int, help="Character limit, counting spaces."
    )
    parser.add_argument(
        "--per-line",
        action="store_true",
        help="Count each non-empty line separately (highlights, key points).",
    )
    parser.add_argument(
        "--section",
        choices=sorted(SECTION_NOTES),
        help="Section context, which adds targeted guidance to the report.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args(argv)

    try:
        text = read_text(args.file)
    except OSError as exc:
        sys.stderr.write(f"Cannot read input: {exc}\n")
        return 2

    if not text.strip():
        sys.stderr.write("Input is empty.\n")
        return 2

    if args.checks == "all":
        selected = list(CHECKS)
    else:
        selected = [name.strip() for name in args.checks.split(",") if name.strip()]
        unknown = [name for name in selected if name not in CHECKS]
        if unknown:
            sys.stderr.write(
                f"Unknown check(s): {', '.join(unknown)}. "
                f"Available: {', '.join(CHECKS)}\n"
            )
            return 2

    results: "OrderedDict[str, List[Dict]]" = OrderedDict()
    for name in selected:
        results[name] = CHECKS[name](text)

    if args.limit_words or args.limit_chars or args.per_line:
        results["length"] = check_length(
            text, args.limit_words, args.limit_chars, args.per_line
        )

    if args.json:
        sys.stdout.write(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render(results, args.section))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
