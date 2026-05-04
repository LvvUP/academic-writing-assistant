import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "academic-writing-assistant" / "scripts"


def run_script(name, *args, input_text=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT_DIR / name), *args],
        input=input_text,
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=True,
    )


def test_terminology_checker_detects_mixed_terms_from_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text(
        "本文关注目标检测任务，同时也将对象检测作为核心问题，并讨论鲁棒性与稳健性。",
        encoding="utf-8",
    )
    result = run_script("terminology_checker.py", str(sample))
    assert "Terminology Consistency Report" in result.stdout
    assert "目标检测, 对象检测" in result.stdout
    assert "鲁棒性, 稳健性" in result.stdout


def test_terminology_checker_accepts_stdin():
    result = run_script(
        "terminology_checker.py",
        input_text="该方法用于语义分割，也可被描述为语义划分。",
    )
    assert "语义分割, 语义划分" in result.stdout


def test_structure_checker_reports_missing_abstract_elements(tmp_path):
    sample = tmp_path / "abstract.md"
    sample.write_text(
        "医学影像分割在临床辅助分析中具有重要价值。本文提出一种轻量化网络。",
        encoding="utf-8",
    )
    result = run_script("structure_checker.py", "--section", "abstract", str(sample))
    assert "Section Audit Report" in result.stdout
    assert "Possibly Missing Elements" in result.stdout
    assert "Experimental evidence" in result.stdout


def test_skill_lint_runs_on_repository():
    result = run_script("skill_lint.py", str(ROOT))
    assert "Skill Lint Report" in result.stdout
    assert "PASS" in result.stdout

