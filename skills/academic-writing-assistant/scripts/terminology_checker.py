#!/usr/bin/env python3
"""Rule-based terminology consistency checker for academic drafts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


DEFAULT_MAP = Path(__file__).resolve().parents[1] / "assets" / "terminology-map.zh-en.json"


def load_terms(path: Path = DEFAULT_MAP) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    terms: List[Dict[str, Any]] = []
    for field, entries in data.items():
        for entry in entries:
            item = dict(entry)
            item["field"] = field
            terms.append(item)
    return terms


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def find_inconsistencies(text: str, terms: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for entry in terms:
        variants = entry.get("variants_zh", [])
        found = [variant for variant in variants if variant and variant in text]
        if len(found) > 1:
            findings.append(
                {
                    "field": entry.get("field", "general"),
                    "found": found,
                    "recommended": entry.get("recommended_zh", found[0]),
                    "english": entry.get("en", ""),
                    "note": entry.get("note", ""),
                }
            )
    return findings


def render_markdown(findings: List[Dict[str, Any]]) -> str:
    lines = ["# Terminology Consistency Report", ""]
    if not findings:
        lines.extend(
            [
                "## Potential Inconsistencies",
                "",
                "No configured terminology inconsistencies were detected.",
            ]
        )
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "## Potential Inconsistencies",
            "",
            "| Field | Variants Found | Recommended Term | English Term | Note |",
            "|---|---|---|---|---|",
        ]
    )
    for finding in findings:
        lines.append(
            "| {field} | {found} | {recommended} | {english} | {note} |".format(
                field=finding["field"],
                found=", ".join(finding["found"]),
                recommended=finding["recommended"],
                english=finding["english"],
                note=finding["note"],
            )
        )
    return "\n".join(lines) + "\n"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check academic terminology consistency.")
    parser.add_argument("file", nargs="?", help="Text or Markdown file. Reads stdin when omitted.")
    parser.add_argument(
        "--map",
        default=str(DEFAULT_MAP),
        help="Terminology map JSON path. Defaults to the bundled terminology map.",
    )
    args = parser.parse_args(argv)

    text = read_text(args.file)
    terms = load_terms(Path(args.map))
    findings = find_inconsistencies(text, terms)
    sys.stdout.write(render_markdown(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
