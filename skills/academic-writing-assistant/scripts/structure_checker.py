#!/usr/bin/env python3
"""Lightweight section completeness checker for academic paper drafts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Sequence


SECTION_RULES: Dict[str, Dict[str, Sequence[str]]] = {
    "abstract": {
        "Background": ["背景", "研究", "问题", "重要", "challenge", "background"],
        "Research problem": ["问题", "挑战", "不足", "limitation", "problem"],
        "Method": ["本文", "提出", "方法", "模型", "we propose", "method"],
        "Experimental evidence": ["实验", "结果", "验证", "dataset", "experiment", "results"],
        "Main conclusion": ["表明", "证明", "说明", "conclusion", "indicate", "suggest"],
    },
    "introduction": {
        "Research background": ["背景", "近年来", "研究", "重要", "background"],
        "Problem importance": ["重要", "关键", "意义", "important", "critical"],
        "Gap or limitation": ["不足", "局限", "挑战", "however", "limitation", "gap"],
        "Proposed method": ["提出", "本文", "we propose", "method"],
        "Contributions": ["贡献", "contribution", "主要工作"],
    },
    "method": {
        "Overview": ["总体", "框架", "overview", "framework"],
        "Problem formulation": ["定义", "符号", "公式", "formulation", "denote"],
        "Architecture or modules": ["模块", "网络", "结构", "architecture", "module"],
        "Objective or loss": ["损失", "目标", "优化", "loss", "objective"],
        "Training or inference": ["训练", "推理", "training", "inference"],
    },
    "experiment": {
        "Datasets": ["数据集", "dataset", "benchmark"],
        "Metrics": ["指标", "metric", "accuracy", "dice", "f1"],
        "Implementation details": ["实现", "参数", "训练", "implementation"],
        "Baselines": ["对比", "baseline", "comparison"],
        "Results": ["结果", "性能", "result", "performance"],
        "Ablation": ["消融", "ablation"],
    },
    "discussion": {
        "Interpretation": ["原因", "说明", "分析", "indicate", "suggest"],
        "Strengths": ["优势", "有效", "benefit", "advantage"],
        "Limitations": ["局限", "不足", "limitation"],
        "Future work": ["未来", "后续", "future"],
    },
}


SUGGESTIONS = {
    "Experimental evidence": "Consider adding a concise sentence summarizing validation results or use a placeholder if results are unavailable.",
    "Main conclusion": "Consider closing with an evidence-bounded conclusion.",
    "Gap or limitation": "Clarify the specific limitation that motivates the proposed work.",
    "Contributions": "Add 2-4 evidence-bounded contribution points.",
    "Datasets": "State the datasets or use a placeholder instead of inventing them.",
    "Metrics": "State the evaluation metrics or mark them as missing.",
}


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def contains_keyword(text: str, keywords: Sequence[str]) -> bool:
    lowered = text.lower()
    return any(re.search(re.escape(keyword.lower()), lowered) for keyword in keywords)


def audit(section: str, text: str) -> Dict[str, List[str]]:
    rules = SECTION_RULES[section]
    present: List[str] = []
    missing: List[str] = []
    for label, keywords in rules.items():
        if contains_keyword(text, keywords):
            present.append(label)
        else:
            missing.append(label)
    return {"present": present, "missing": missing}


def render_report(section: str, result: Dict[str, List[str]]) -> str:
    lines = ["# Section Audit Report", "", f"Section: {section}", ""]
    lines.append("## Present Elements")
    lines.append("")
    if result["present"]:
        lines.extend(f"- {item}: detected" for item in result["present"])
    else:
        lines.append("- None detected")
    lines.extend(["", "## Possibly Missing Elements", ""])
    if result["missing"]:
        lines.extend(f"- {item}" for item in result["missing"])
    else:
        lines.append("- None")
    lines.extend(["", "## Suggestions", ""])
    if result["missing"]:
        for item in result["missing"]:
            lines.append(f"- {SUGGESTIONS.get(item, 'Consider adding this element if it is relevant and supported by your study.')}")
    else:
        lines.append("- The configured structure elements are present. Still verify factual accuracy manually.")
    return "\n".join(lines) + "\n"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit academic paper section structure.")
    parser.add_argument(
        "--section",
        choices=sorted(SECTION_RULES),
        required=True,
        help="Section type to audit.",
    )
    parser.add_argument("file", nargs="?", help="Text or Markdown file. Reads stdin when omitted.")
    args = parser.parse_args(argv)

    text = read_text(args.file)
    result = audit(args.section, text)
    sys.stdout.write(render_report(args.section, result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
