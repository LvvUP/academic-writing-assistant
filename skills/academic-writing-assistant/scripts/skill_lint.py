#!/usr/bin/env python3
"""Repository-level lint checks for the Academic Writing Assistant Skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List


REQUIRED_REFERENCES = [
    "task-router.md",
    "field-adapter.md",
    "writing-workflows.md",
    "style-guide-zh.md",
    "style-guide-en.md",
    "output-templates.md",
    "quality-checklist.md",
    "examples.md",
]

REQUIRED_README_SECTIONS = [
    "项目定位",
    "为什么需要",
    "核心功能",
    "支持的学术写作任务",
    "支持的研究领域",
    "安装",
    "Quick Examples",
    "Academic Integrity",
    "Roadmap",
    "Contributing",
    "License",
]

FORBIDDEN_MARKERS = [
    "guaranteed acceptance",
    "保证录用",
    "绕过检测",
    "规避检测",
    "guaranteed publication",
]


def check(root: Path) -> List[str]:
    failures: List[str] = []
    skill_dir = root / "skills" / "academic-writing-assistant"
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        failures.append("Missing skills/academic-writing-assistant/SKILL.md")
    else:
        text = skill_md.read_text(encoding="utf-8")
        if "name: academic-writing-assistant" not in text:
            failures.append("SKILL.md is missing the expected name.")
        if "description:" not in text:
            failures.append("SKILL.md is missing description.")
        if "Never invent" not in text and "Never fabricate" not in text:
            failures.append("SKILL.md should include explicit fabrication guardrails.")

    for ref in REQUIRED_REFERENCES:
        if not (skill_dir / "references" / ref).exists():
            failures.append(f"Missing reference: {ref}")

    readme = root / "README.md"
    if not readme.exists():
        failures.append("Missing README.md")
    else:
        readme_text = readme.read_text(encoding="utf-8")
        for section in REQUIRED_README_SECTIONS:
            if section not in readme_text:
                failures.append(f"README.md missing section phrase: {section}")

    plugin_json = root / ".codex-plugin" / "plugin.json"
    if not plugin_json.exists():
        failures.append("Missing .codex-plugin/plugin.json")
    else:
        try:
            data = json.loads(plugin_json.read_text(encoding="utf-8"))
            if data.get("name") != "academic-writing-assistant":
                failures.append("plugin.json name should be academic-writing-assistant.")
        except json.JSONDecodeError as exc:
            failures.append(f"plugin.json is invalid JSON: {exc}")

    combined_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in root.rglob("*.md")
        if ".git" not in path.parts
    )
    lowered = combined_text.lower()
    for marker in FORBIDDEN_MARKERS:
        if marker.lower() in lowered:
            failures.append(f"Forbidden claim detected: {marker}")

    return failures


def render(failures: List[str]) -> str:
    lines = ["# Skill Lint Report", ""]
    if failures:
        lines.append("Status: FAIL")
        lines.append("")
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All configured repository checks passed.")
    return "\n".join(lines) + "\n"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint the Academic Writing Assistant repository.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root.")
    args = parser.parse_args(argv)

    failures = check(Path(args.root).resolve())
    sys.stdout.write(render(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
