#!/usr/bin/env python3
"""Check whether a draft section contains the elements reviewers expect.

This is a keyword scan, and it should be read as one: it detects whether a
draft *mentions* something, not whether it does so well. A section can pass
every check and still be poorly argued, and a good section can fail a check
because the author phrased something unusually. Treat findings as a list of
things to look at.

The value is catching outright omissions -- an abstract with no results
sentence, an experiment section that never names a baseline -- which are easy
to miss when re-reading your own draft.

Usage::

    python structure_checker.py --section abstract draft.md
    python structure_checker.py --section experiment draft.tex --json
    cat draft.md | python structure_checker.py --section introduction
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Sequence


SECTION_RULES: "OrderedDict[str, OrderedDict[str, Sequence[str]]]" = OrderedDict(
    (
        (
            "abstract",
            OrderedDict(
                (
                    ("Context and problem", ("背景", "问题", "挑战", "难以", "challenge", "problem", "remains", "difficult")),
                    ("Gap in existing work", ("不足", "局限", "现有方法", "however", "limitation", "existing", "prior")),
                    ("Proposed approach", ("本文", "提出", "我们", "we propose", "we present", "this paper", "this study", "method")),
                    ("Evidence", ("实验", "数据集", "验证", "结果", "experiment", "dataset", "evaluat", "results", "achiev")),
                    ("Conclusion", ("表明", "说明", "结果显示", "suggest", "indicate", "demonstrate", "show that")),
                )
            ),
        ),
        (
            "introduction",
            OrderedDict(
                (
                    ("Research background", ("背景", "近年来", "研究", "background", "recent", "widely")),
                    ("Specific problem", ("问题", "挑战", "难点", "problem", "challenge", "difficult")),
                    ("Prior work and its limits", ("现有", "已有方法", "然而", "不足", "existing", "however", "limitation", "prior work")),
                    ("Proposed response", ("提出", "本文", "为此", "we propose", "to address", "this paper")),
                    ("Contributions", ("贡献", "主要工作", "contribution", "summarized as", "as follows")),
                )
            ),
        ),
        (
            "related_work",
            OrderedDict(
                (
                    ("Organizing principle", ("可分为", "分为", "两类", "三类", "categor", "grouped", "broadly")),
                    ("Prior approaches", ("方法", "研究", "工作", "method", "approach", "studies", "work")),
                    ("Stated limitation", ("局限", "不足", "难以", "limitation", "however", "fail", "struggle")),
                    ("Transition to this work", ("与之不同", "本文", "相比之下", "in contrast", "unlike", "differ", "this work")),
                )
            ),
        ),
        (
            "method",
            OrderedDict(
                (
                    ("Overview", ("总体", "整体", "框架", "概述", "overview", "framework", "overall", "pipeline")),
                    ("Problem formulation", ("定义", "记为", "设", "符号", "formulation", "denote", "let ", "given")),
                    ("Architecture or components", ("模块", "网络", "结构", "分支", "architecture", "module", "block", "layer", "branch")),
                    ("Objective or loss", ("损失", "目标函数", "优化", "loss", "objective", "minimiz", "maximiz")),
                    ("Training or inference", ("训练", "推理", "优化器", "training", "inference", "optimiz", "learning rate")),
                )
            ),
        ),
        (
            "experiment",
            OrderedDict(
                (
                    ("Datasets", ("数据集", "样本", "dataset", "benchmark", "corpus", "cohort", "samples")),
                    ("Metrics", ("指标", "评价", "metric", "accuracy", "dice", "iou", "map", "f1", "auc", "precision", "recall")),
                    ("Implementation details", ("实现", "参数", "训练设置", "implementation", "epoch", "batch", "learning rate", "gpu")),
                    ("Baselines", ("对比", "基线", "baseline", "compared with", "comparison", "state-of-the-art")),
                    ("Results", ("结果", "性能", "result", "performance", "achiev", "obtain")),
                    ("Ablation", ("消融", "ablation", "component analysis", "without the")),
                    ("Variance or statistics", ("标准差", "方差", "显著性", "std", "standard deviation", "±", "p =", "p<", "p <", "seed", "confidence interval")),
                )
            ),
        ),
        (
            "discussion",
            OrderedDict(
                (
                    ("Interpretation", ("原因", "解释", "分析", "这表明", "suggest", "indicate", "explain", "attribute")),
                    ("Where it works", ("优势", "有效", "改善", "benefit", "advantage", "improve")),
                    ("Where it fails", ("失败", "不足", "受限", "fail", "degrade", "struggle", "worse")),
                    ("Limitations", ("局限", "限制", "limitation", "constrain")),
                    ("Future work", ("未来", "后续", "下一步", "future", "further work", "plan to")),
                )
            ),
        ),
        (
            "conclusion",
            OrderedDict(
                (
                    ("What was done", ("本文", "提出", "we propose", "this paper", "presented")),
                    ("What was found", ("实验", "结果", "表明", "results", "show", "demonstrate")),
                    ("Bounded scope", ("在所", "数据集上", "evaluated", "on the", "under")),
                    ("Outlook", ("未来", "后续", "future", "further")),
                )
            ),
        ),
    )
)


SUGGESTIONS: Dict[str, str] = {
    "Context and problem": "Open with the specific problem rather than a general field statement.",
    "Gap in existing work": "State what existing approaches cannot do — this is what motivates the paper.",
    "Evidence": "Summarize validation. If results are not ready, use an explicit placeholder rather than omitting the sentence.",
    "Conclusion": "Close with an evidence-bounded takeaway.",
    "Contributions": "Add 2-4 contributions, each naming something you did rather than a property you claim.",
    "Prior work and its limits": "Name the gap the paper addresses; a reviewer looks for this first.",
    "Organizing principle": "State how prior work is grouped, so the section reads as an argument rather than a list.",
    "Transition to this work": "End by connecting the surveyed limitation to your approach.",
    "Problem formulation": "Define notation and the task formally, so the method can be reimplemented.",
    "Objective or loss": "State what is being optimized.",
    "Training or inference": "Give the training procedure; reviewers treat this as a reproducibility requirement.",
    "Datasets": "Name the datasets, or mark them as missing. Never invent one.",
    "Metrics": "State the evaluation metrics explicitly.",
    "Baselines": "Name the methods compared against; 'existing methods' invites a reviewer question.",
    "Ablation": "Ablations isolating each component are expected in most venues.",
    "Variance or statistics": "Report seed variance or a statistical test. Without one, avoid the word 'significant'.",
    "Where it fails": "Describing failure cases strengthens credibility rather than weakening it.",
    "Limitations": "State real limitations; decorative ones read as evasion.",
    "Future work": "Connect future work to a stated limitation.",
    "Bounded scope": "Bound the conclusion to what was evaluated.",
}


def read_text(path: Optional[str]) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def contains_keyword(text: str, keywords: Sequence[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def audit(section: str, text: str) -> Dict[str, List[str]]:
    rules = SECTION_RULES[section]
    present: List[str] = []
    missing: List[str] = []
    for label, keywords in rules.items():
        (present if contains_keyword(text, keywords) else missing).append(label)
    return {"present": present, "missing": missing}


def count_placeholders(text: str) -> int:
    return len(
        re.findall(r"\[(?:请|please|TODO|citation needed|待)[^\]]*\]", text, re.IGNORECASE)
    )


def render(section: str, result: Dict[str, List[str]], placeholders: int) -> str:
    lines = ["# Section Structure Check", "", f"Section: {section}", ""]

    lines.extend(["## Detected", ""])
    if result["present"]:
        lines.extend(f"- {item}" for item in result["present"])
    else:
        lines.append("- None of the configured elements were detected.")

    lines.extend(["", "## Possibly missing", ""])
    if result["missing"]:
        for item in result["missing"]:
            suggestion = SUGGESTIONS.get(
                item, "Add if relevant and supported by your study."
            )
            lines.append(f"- **{item}** — {suggestion}")
    else:
        lines.append("- None. All configured elements appear present.")

    if placeholders:
        lines.extend(
            [
                "",
                "## Placeholders",
                "",
                f"- {placeholders} placeholder(s) found. These must be replaced with "
                "real content before submission.",
            ]
        )

    lines.extend(
        [
            "",
            "## Note",
            "",
            "This is a keyword scan. It detects whether an element is mentioned, not "
            "whether it is argued well, and it cannot verify that any number, dataset, "
            "or citation in the draft is real.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check a paper section for the elements reviewers expect."
    )
    parser.add_argument(
        "--section",
        choices=sorted(SECTION_RULES),
        required=True,
        help="Section type to check.",
    )
    parser.add_argument("file", nargs="?", help="Text file. Reads stdin when omitted.")
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

    result = audit(args.section, text)
    placeholders = count_placeholders(text)

    if args.json:
        payload = dict(result, section=args.section, placeholders=placeholders)
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render(args.section, result, placeholders))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
