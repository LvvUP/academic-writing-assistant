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

from check_utils import configure_cli_streams, read_input, markdown_text
from prose_utils import mask_prose, sentence_spans, escaped


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
        (r"\bthe first\b|\bwe are the first\b", "Verify the defined novelty scope and literature evidence; to our knowledge is not evidence."),
        (r"\boutperforms?\s+all\b", "Identify the comparison set and check that the reported results support its full stated scope."),
        (r"\bbest performance\b", "Specify on which datasets and against which baselines."),
        (r"\bsuperior to (?:all|existing|other)\b", "Unbounded comparison claim."),
        (r"\buniversally\b|\bin all cases\b|\balways achieves\b", "Absolute coverage claim."),
        (r"\bperfectly\b|\bcompletely solves?\b|\bfully solves?\b", "Check the stated domain and proof/evidence; a bounded theoretical result may be justified."),
        (r"首次(?:提出|实现)", "核对首次主张的范围和文献依据；据我们所知不能替代证据。"),
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
    return read_input(path)


def strip_markup(text: str) -> str:
    """Mask non-prose without changing original offsets or line breaks."""
    return mask_prose(text)[0]


def split_sentences(text: str) -> List[str]:
    return [sentence for _, _, sentence in sentence_spans(text)]


def source_location(text, start, end):
    return {"line": locate(text, start), "start": start, "end": end,
            "source": text[start:end]}


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
                    **source_location(text, first_use, first_use + len(acronym)),
                    "note": f"'{acronym}' is used on line {use_line} but {where}. "
                    "Move the definition to first use.",
                }
            )
        elif len(positions) <= 1:
            findings.append(
                {
                    "type": "abbreviation_defined_once",
                    "item": acronym,
                    **source_location(text, definition + 1, definition + 1 + len(acronym)),
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
                    **source_location(text, min(usages[acronym]), min(usages[acronym]) + len(acronym)),
                    "note": f"'{acronym}' is used {len(usages[acronym])} times without a "
                    "parenthesized definition. Confirm it is standard enough for the venue.",
                }
            )

    return findings


# A small lexical predicate inventory separates obvious independent clauses.
# It is not a parser or a guarantee that a test belongs to the claimed outcome.
CLAUSE_PREDICATE = (
    r"(?:is|are|was|were|has|have|had|can|could|does|do|did|"
    r"changed?|changes|improves?|improved|increases?|increased|decreases?|decreased|"
    r"reduces?|reduced|differs?|differed|shows?|showed|causes?|caused|"
    r"leads?|led|outperforms?|outperformed|establish(?:es|ed)?|"
    r"conclude[sd]?|observes?|observed|returned|yielded|remained|plan(?:ned|s)?)"
)
INDEPENDENT_CLAUSE = re.compile(
    r"\s*(?P<subject>(?:(?!(?:significantly|statistically|not|only|also)\b)"
    r"[A-Za-z][\w'-]*\s+){1,7})"
    r"(?:(?:significantly|statistically|not|only|also)\s+){0,3}"
    + CLAUSE_PREDICATE + r"\b", re.I)
PREDICATION = re.compile(r"\b" + CLAUSE_PREDICATE + r"\b", re.I)
TEST_SUBJECT = re.compile(
    r"(?:(?:a|an|the)\s+)?(?:(?:paired|unpaired|statistical)\s+)?"
    r"(?:t[- ]test|test|wilcoxon(?:\s+test)?|anova|chi[- ]squared?(?:\s+test)?)\s*", re.I)
EXTRA_COMPARISON_OBJECT = re.compile(r"\b(?:and|or)\s+(?:to\s+)?(?:all|every)\b", re.I)


def claim_clauses(sentence):
    """Yield original-relative spans, preserving shared-subject/test phrases."""
    boundaries, previous, cursor, depth = [], 0, 0, 0
    has_predication = False
    for match in re.finditer(r"[;；]|\b(?:and|or|but|whereas|while)\b|但", sentence, re.I):
        has_predication = has_predication or bool(PREDICATION.search(sentence, cursor, match.start()))
        for char in sentence[cursor:match.start()]:
            if char in "([":
                depth += 1
            elif char in ")]":
                depth = max(0, depth - 1)
        cursor = match.end()
        if match.group().lower() in {"and", "or"}:
            # Do not split outcome lists, shared verbs, tests joined by "and",
            # or a test-subject clause reporting evidence for the same outcome.
            following = INDEPENDENT_CLAUSE.match(sentence, match.end())
            if (depth or not following or not has_predication
                    or TEST_SUBJECT.fullmatch(following.group("subject").strip())):
                continue
        boundaries.append((previous, match.start()))
        previous = match.end()
        has_predication = False
    boundaries.append((previous, len(sentence)))
    for start, end in boundaries:
        while start < end and sentence[start].isspace():
            start += 1
        while end > start and sentence[end - 1].isspace():
            end -= 1
        if start < end:
            yield start, end, sentence[start:end]


def bounded_comparison(clause, match, extra_object_at):
    """Recognize a locally specified comparison object, not any qualifier."""
    if not re.search(r"(?:outperforms?\s+all|superior\s+to\s+all)$", match.group(), re.I):
        return False
    count = r"(?:[1-9]\d*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    scope = r"(?:evaluated|tested|selected|listed|included|reported)"
    objects = r"(?:baselines?|methods?|models?|comparators?|systems?|approaches?|algorithms?|variants?)\b"
    bounded = re.compile(
        r"\s+(?:the\s+)?(?:" + count + r"\s+(?:" + scope + r"\s+)?" + objects
        + r"|" + scope + r"\s+" + objects
        + r"|" + objects + r"\s+(?:(?:that|which)\s+(?:were\s+)?)?" + scope + r"\b)",
        re.I).match(clause, match.end())
    if not bounded:
        return False
    # A bounded first object must not hide an additional universal object.
    # Its last position is computed once per clause, avoiding repeated suffix
    # copies/scans when a long clause contains many bounded comparisons.
    return extra_object_at < bounded.end()


def nonasserted_cause(clause, position):
    """Recognize direct denial or a short explicit inference/question frame."""
    prefix = clause[:position]
    if re.search(r"\b(?:not|cannot|can't|couldn't|doesn't|don't|didn't|isn't|aren't|wasn't|weren't)\s+$|(?:未|没有|不会|不)$", prefix, re.I):
        return True
    subject = r"(?:[A-Za-z][\w'-]*\s+){0,8}"
    denied_inference = (
        r"\b(?:(?:do|does|did)\s+not|cannot|can't|could\s+not|couldn't|doesn't|don't|didn't)\s+"
        r"(?:establish|conclude|infer|prove|show|demonstrate|imply)\s+"
        r"(?:that\s+)?" + subject + r"$"
    )
    question = r"\b(?:tested?|asked?|examined?|investigated?)\s+whether\s+" + subject + r"$"
    chinese_denial = r"(?:不能|无法|不足以)(?:证明|推断|说明)[^，,；;。]{0,24}$"
    return bool(re.search(denied_inference + "|" + question + "|" + chinese_denial, prefix, re.I))


def check_claims(text: str) -> List[Dict]:
    """Flag positive claims lacking a nearby reported test, not absent research."""
    prose, _, excluded = mask_prose(text)
    evidence_view = list(prose)
    for span in excluded:
        if span["kind"] == "math":
            evidence_view[span["start"]:span["end"]] = text[span["start"]:span["end"]]
    # Restoring inline math must not restore TeX comments as evidence.
    for span in excluded:
        if span["kind"] == "math":
            for match in re.finditer(r"%[^\n]*", text[span["start"]:span["end"]]):
                at = span["start"] + match.start()
                if not escaped(text, at):
                    evidence_view[at:span["start"] + match.end()] = " " * (match.end() - match.start())
    evidence_view = "".join(evidence_view)
    findings = []
    test_pattern = re.compile(
        r"\bp\s*(?:[- ]value\s*)?[<>=≤≥]\s*(?:0?\.\d+|\d+)"
        r"|\b(?:paired |unpaired )?t[- ]test\b|\bwilcoxon\b"
        r"|\bmann[- ]whitney\b|\banova\b|\bchi[- ]squared?\b"
        r"|显著性检验|置换检验", re.I)
    positive = re.compile(
        r"\bstatistically\s+significant\b|\bsignificantly\b"
        r"|\bsignificant\s+(?:difference|improvement|increase|decrease|effect|association|correlation|reduction|gain)s?\b"
        r"|\bdifferences?\s+(?:is|was|are|were)\s+(?:statistically\s+)?significant\b"
        r"|(?:统计)?显著(?:的)?(?:性|提升|提高|改善|优于|高于|低于|增加|降低|差异|相关|影响)|差异显著", re.I)
    negation = re.compile(
        r"\b(?:not|no|without|non[- ]?)\s+(?:a\s+)?(?:statistically\s+)?$"
        r"|\b(?:cannot|can't|could not)\s+(?:conclude|establish|claim)[^.;；。]{0,55}$"
        r"|(?:不(?:具有|存在|呈现|是)?|未(?:观察到|发现|达到|见)?|不能(?:认定|推断|说明))[^。；]{0,12}$", re.I)
    nonstat = re.compile(r"significant (?:digit|figure|challenge|role)|practical significance|显著性(?:水平|图|检测)", re.I)
    for begin, _, sentence in sentence_spans(prose):
        for start, stop, clause in claim_clauses(sentence):
            offset, end = begin + start, begin + stop
            raw = evidence_view[offset:end]
            extra_object_at = max((m.start() for m in EXTRA_COMPARISON_OBJECT.finditer(clause)), default=-1)
            positive_matches = list(positive.finditer(clause))
            asserted = any(not negation.search(clause[:m.start()]) and not nonstat.match(clause, m.start()) for m in positive_matches)
            if asserted:
                # Inline math is available only inside this clause's source span.
                has_evidence = bool(test_pattern.search(raw))
                evidence_denied = bool(re.search(r"(?:no|without|not (?:run|performed|conducted)|plan(?:ned)? to|intend to|will|would|should).{0,65}(?:test|p[- ]value)|(?:未|计划|将).*检验", raw, re.I))
                if not has_evidence or evidence_denied:
                    findings.append(dict(type="significance_without_test", item=excerpt(clause),
                        **source_location(text, offset, end),
                        note="Significance evidence review: 当前主张所在子句未找到可关联的检验或 p 值，请核对相应结果位置；"
                        "这不证明作者未做检验。标准差、方差或区间本身不等于显著性证据，"
                        "也不能自动替换为 consistent。"))
            for patterns, kind in [(SUPERLATIVE_PATTERNS, "unbounded_claim"), (CAUSAL_PATTERNS, "causal_language")]:
                for pattern, note in patterns.items():
                    matches = re.finditer(pattern, clause, re.I)
                    if any(not (bounded_comparison(clause, m, extra_object_at) if kind == "unbounded_claim"
                                else nonasserted_cause(clause, m.start())) for m in matches):
                        findings.append(dict(type=kind, item=excerpt(clause), note=note,
                                             **source_location(text, offset, end)))
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
                    **source_location(text, match.start(), match.end()),
                    "note": note,
                }
            )

    for offset, end, sentence in sentence_spans(prose):
        lowered = sentence.lower()
        hits = [word for word in HEDGE_WORDS if word in lowered]
        if len(hits) >= 3:
            findings.append(
                {
                    "type": "hedge_stacking",
                    "item": excerpt(sentence),
                    **source_location(text, offset, end),
                    "note": f"Stacked hedges ({', '.join(hits[:4])}). Review each hedge separately; changing frequency, strength or scope is L3.",
                }
            )

    return findings


def check_tense(text: str) -> List[Dict]:
    """Compatibility entry point: tense correctness requires semantic review.

    Method-present and experiment-past legitimately coexist. A keyword mixture
    provides no defensible error criterion, so it produces no automatic finding.
    """
    return []


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
    prose, _, excluded = mask_prose(text)

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
    included = bytearray(b"1") * len(text)
    for span in excluded:
        included[span["start"]:span["end"]] = b"0" * (span["end"] - span["start"])
    visible = "".join(c for pos, c in enumerate(prose) if included[pos] == ord("1"))
    total_chars = len(visible.strip())

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
        ("dataset", "data set"),
        ("fine-tuning", "finetuning"),
        ("pre-training", "pretraining"),
        ("multi-scale", "multiscale"),
        ("state-of-the-art", "state of the art"),
    ]

    for first, second in pairs:
        first_count = len(re.findall(r"(?<!\w)" + re.escape(first) + r"(?!\w)", prose))
        second_count = len(re.findall(r"(?<!\w)" + re.escape(second) + r"(?!\w)", prose))
        if first_count and second_count:
            findings.append(
                {
                    "type": "terminology_drift",
                    "item": f"'{first}' ({first_count}×) / '{second}' ({second_count}×)",
                    "line": 0,
                    "note": "Both spelling/style variants appear. Check author terminology and context before proposing changes.",
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
                "still need review. Tense and mathematical symbol definitions are NOT RUN by this scanner.",
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
            lines.append(f"- **{markdown_text(finding['item'])}**{location}")
            if finding.get("note"):
                lines.append(f"  - {markdown_text(finding['note'])}")
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
    configure_cli_streams()
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
    parser.add_argument("--strict", action="store_true", help="Exit 1 for review findings, length overruns or insufficient coverage.")
    args = parser.parse_args(argv)
    if any(value is not None and value <= 0 for value in [args.limit_words, args.limit_chars]):
        parser.error("Length limits must be positive integers.")
    if not args.checks.strip():
        parser.error("At least one check is required.")

    try:
        text = read_text(args.file)
    except (OSError, UnicodeError, ValueError) as exc:
        sys.stderr.write(f"Cannot read input: {exc}\n")
        return 2

    if not text.strip():
        sys.stderr.write("Input is empty.\n")
        return 2

    if args.checks == "all":
        selected = [name for name in CHECKS if name != "tense"]
    else:
        selected = [name.strip() for name in args.checks.split(",") if name.strip()]
        if not selected:
            parser.error("At least one check is required.")
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

    prose, warnings, excluded = mask_prose(text)
    if "tense" in selected:
        warnings.append({"line": 0, "start": 0, "reason": "NOT RUN: tense correctness requires semantic review"})
    if not prose.strip():
        warnings.append({"line": 0, "start": 0, "reason": "No readable prose covered"})
    if warnings:
        results["coverage"] = [dict(type="coverage_limit", item=w["reason"],
            line=w["line"], start=w["start"], note="INSUFFICIENT: this construct needs source review.") for w in warnings]
    if args.json:
        sys.stdout.write(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render(results, args.section))

    issues = any(f["type"] not in {"count", "line_count"} for group in results.values() for f in group)
    return 1 if args.strict and issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
