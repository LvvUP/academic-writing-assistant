#!/usr/bin/env python3
"""Report Chinese terminology variants that appear together in one draft.

Mixing 目标检测 and 对象检测 for the same concept makes a reader wonder whether
two different things are meant. This scans for configured variant groups and
reports which ones co-occur, with occurrence counts so the author can see which
form dominates.

It does not decide anything. Some drafts distinguish nearby terms deliberately,
and where both variants are standard in a field the choice belongs to the
author -- the report says so rather than pretending otherwise.

Usage::

    python terminology_checker.py draft.md
    python terminology_checker.py draft.md --map custom-terms.json
    cat draft.md | python terminology_checker.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


DEFAULT_MAP = Path(__file__).resolve().parents[1] / "assets" / "terminology-map.zh-en.json"


def load_terms(path: Path = DEFAULT_MAP) -> List[Dict[str, Any]]:
    """Flatten the field-keyed map into a list of entries.

    Keys beginning with an underscore hold documentation rather than terms.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    terms: List[Dict[str, Any]] = []
    for field, entries in data.items():
        if field.startswith("_") or not isinstance(entries, list):
            continue
        for entry in entries:
            item = dict(entry)
            item["field"] = field
            terms.append(item)
    return terms


def read_text(path: Optional[str]) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def find_inconsistencies(
    text: str, terms: Iterable[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for entry in terms:
        counts = {
            variant: text.count(variant)
            for variant in entry.get("variants_zh", [])
            if variant
        }
        present = {variant: count for variant, count in counts.items() if count}
        if len(present) < 2:
            continue

        dominant = max(present, key=lambda variant: present[variant])
        findings.append(
            {
                "field": entry.get("field", "general"),
                "found": present,
                "dominant": dominant,
                "recommended": entry.get("recommended_zh", dominant),
                "english": entry.get("en", ""),
                "note": entry.get("note", ""),
            }
        )
    return findings


def format_counts(found: Dict[str, int]) -> str:
    ordered = sorted(found.items(), key=lambda item: (-item[1], item[0]))
    return " / ".join(f"{variant}（{count} 次）" for variant, count in ordered)


def render_markdown(findings: List[Dict[str, Any]]) -> str:
    lines = ["# Terminology Consistency Report", ""]

    if not findings:
        lines.extend(
            [
                "No configured variant groups co-occur in this text.",
                "",
                "The scan covers the variant pairs in the bundled map only. It cannot "
                "detect the harder problem -- one term used for two different concepts "
                "-- which still needs a read-through.",
            ]
        )
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            f"Found {len(findings)} variant group(s) used inconsistently.",
            "",
            "| 领域 | 出现的变体 | 全文占多数 | 推荐 | English | 说明 |",
            "|---|---|---|---|---|---|",
        ]
    )
    for finding in findings:
        lines.append(
            "| {field} | {found} | {dominant} | {recommended} | {english} | {note} |".format(
                field=finding["field"],
                found=format_counts(finding["found"]),
                dominant=finding["dominant"],
                recommended=finding["recommended"],
                english=finding["english"],
                note=finding["note"].replace("|", "/"),
            )
        )

    lines.extend(
        [
            "",
            "## How to read this",
            "",
            "- Normalizing to the dominant variant is usually right, since it means "
            "fewer edits and preserves the author's own preference.",
            "- Where the note says both forms are standard, the choice belongs to the "
            "author; consistency is what matters.",
            "- If the draft distinguishes two nearby terms deliberately, keep the "
            "distinction and define it at first use.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Chinese terminology consistency in an academic draft."
    )
    parser.add_argument("file", nargs="?", help="Text file. Reads stdin when omitted.")
    parser.add_argument(
        "--map",
        default=str(DEFAULT_MAP),
        help="Terminology map JSON path. Defaults to the bundled map.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args(argv)

    try:
        text = read_text(args.file)
        terms = load_terms(Path(args.map))
    except OSError as exc:
        sys.stderr.write(f"Cannot read input: {exc}\n")
        return 2
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Terminology map is not valid JSON: {exc}\n")
        return 2

    findings = find_inconsistencies(text, terms)

    if args.json:
        sys.stdout.write(json.dumps(findings, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render_markdown(findings))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
