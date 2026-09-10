import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "academic-writing-assistant" / "scripts"


def run_script(name, *args, input_text=None, check=True):
    return subprocess.run(
        [sys.executable, str(SCRIPT_DIR / name), *args],
        input=input_text,
        text=True, encoding='utf-8',
        capture_output=True,
        cwd=ROOT,
        check=check,
    )


# ---------------------------------------------------------------------------
# fidelity_check
# ---------------------------------------------------------------------------


def write_pair(tmp_path, before_text, after_text):
    before = tmp_path / "before.tex"
    after = tmp_path / "after.tex"
    before.write_text(before_text, encoding="utf-8")
    after.write_text(after_text, encoding="utf-8")
    return str(before), str(after)


def test_fidelity_check_passes_on_a_faithful_rewrite(tmp_path):
    """A rewrite that only touches free-surface wording must come back clean."""
    original = (
        "As shown in Section~\\ref{sec:m}, the \\ours{} model builds on prior "
        "work~\\cite{a2021,b2020} and improves accuracy by 3.2 points. "
        "The loss is $\\mathcal{L} = \\alpha \\mathcal{L}_1$ and Table~\\ref{tab:x} "
        "reports 92.3\\% Dice."
    )
    revised = (
        "As shown in Section~\\ref{sec:m}, the \\ours{} model builds on prior "
        "work~\\cite{a2021,b2020} and improves accuracy by 3.2 points. "
        "The loss is $\\mathcal{L} = \\alpha \\mathcal{L}_1$; Table~\\ref{tab:x} "
        "reports a Dice score of 92.3\\%."
    )
    before, after = write_pair(tmp_path, original, revised)
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "Status: PASS" in result.stdout


def test_fidelity_check_detects_a_dropped_citation(tmp_path):
    before, after = write_pair(
        tmp_path,
        "Prior work~\\cite{a2021,b2020} established this.",
        "Prior work~\\cite{a2021} established this.",
    )
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "REVIEW NEEDED" in result.stdout
    assert "b2020" in result.stdout


def test_fidelity_check_detects_a_changed_number(tmp_path):
    """The failure this script exists for: a silently altered result."""
    before, after = write_pair(
        tmp_path,
        "The method improves accuracy by 3.2 points.",
        "The method improves accuracy by 3.5 points.",
    )
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "REVIEW NEEDED" in result.stdout
    assert "3.2" in result.stdout
    assert "3.5" in result.stdout


def test_fidelity_check_detects_a_truncated_equation(tmp_path):
    before, after = write_pair(
        tmp_path,
        "The loss is $\\mathcal{L} = \\alpha \\mathcal{L}_1 + \\beta \\mathcal{L}_2$.",
        "The loss is $\\mathcal{L} = \\alpha \\mathcal{L}_1$.",
    )
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "REVIEW NEEDED" in result.stdout
    assert "Math blocks" in result.stdout


def test_fidelity_check_detects_a_dropped_custom_macro(tmp_path):
    """Author macros carry the method name; losing one renames it everywhere."""
    before, after = write_pair(
        tmp_path,
        "We evaluate \\ours{} against the baseline.",
        "We evaluate the model against the baseline.",
    )
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "REVIEW NEEDED" in result.stdout
    assert "ours" in result.stdout


def test_fidelity_check_detects_a_dropped_dataset_name(tmp_path):
    """Dataset names carry no digits, so the numeric check cannot see them."""
    before, after = write_pair(
        tmp_path,
        "We evaluate on LEVIR-CD, WHU-CD, and ImageNet.",
        "We evaluate on LEVIR-CD and ImageNet.",
    )
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "REVIEW NEEDED" in result.stdout
    assert "WHU-CD" in result.stdout


def test_fidelity_check_does_not_flag_ordinary_prose_as_a_name(tmp_path):
    """Ordinary capitals are not entities, and zero coverage is not proof."""
    before, after = write_pair(tmp_path, "The method works well. Experiments confirm this.",
                               "The method performs well. Experiments confirm this finding.")
    result = run_script("fidelity_check.py", "--before", before, "--after", after, "--json")
    payload = json.loads(result.stdout)
    assert payload["named_entities"]["before_count"] == 0
    assert payload["named_entities"]["after_count"] == 0
    assert payload["_meta"]["status"] == "INSUFFICIENT"


def test_fidelity_check_pass_message_states_its_limits(tmp_path):
    """A PASS must not be readable as 'the whole locked zone was verified'."""
    before, after = write_pair(tmp_path, "Accuracy was 90.1%.", "Accuracy reached 90.1%.")
    result = run_script("fidelity_check.py", "--before", before, "--after", after)
    assert "Status: PASS" in result.stdout
    assert "claim strength" in result.stdout


def test_fidelity_check_strict_mode_exits_non_zero(tmp_path):
    before, after = write_pair(
        tmp_path, "Accuracy reached 92.3%.", "Accuracy reached 93.2%."
    )
    result = run_script(
        "fidelity_check.py", "--before", before, "--after", after, "--strict", check=False
    )
    assert result.returncode == 1


def test_fidelity_check_json_output_is_parseable(tmp_path):
    before, after = write_pair(tmp_path, "Result: 5 points.", "Result: 5 points.")
    result = run_script("fidelity_check.py", "--before", before, "--after", after, "--json")
    payload = json.loads(result.stdout)
    assert "numbers" in payload
    assert payload["numbers"]["missing"] == []


# ---------------------------------------------------------------------------
# manuscript_audit
# ---------------------------------------------------------------------------


def test_manuscript_audit_flags_significance_without_a_test(tmp_path):
    sample = tmp_path / "draft.md"
    sample.write_text(
        "Our method significantly outperforms the baseline on all datasets.",
        encoding="utf-8",
    )
    result = run_script("manuscript_audit.py", str(sample), "--checks", "claims")
    assert "significance" in result.stdout.lower()


def test_manuscript_audit_stays_quiet_when_a_test_is_reported(tmp_path):
    """Significance language is correct when a test backs it -- no false alarm."""
    sample = tmp_path / "draft.md"
    sample.write_text(
        "The method improves Dice by 2.1 points, significantly better than the "
        "baseline (paired t-test, p = 0.01).",
        encoding="utf-8",
    )
    result = run_script("manuscript_audit.py", str(sample), "--checks", "claims")
    assert "significance_without_test" not in result.stdout
    assert "no statistical test appears" not in result.stdout


def test_manuscript_audit_flags_abbreviation_used_before_definition(tmp_path):
    sample = tmp_path / "draft.md"
    sample.write_text(
        "We use MSFF throughout the pipeline. The multi-scale feature fusion "
        "(MSFF) module is described later.",
        encoding="utf-8",
    )
    result = run_script("manuscript_audit.py", str(sample), "--checks", "abbreviations")
    assert "MSFF" in result.stdout


def test_manuscript_audit_flags_ceremonial_openers(tmp_path):
    sample = tmp_path / "draft.md"
    sample.write_text(
        "With the rapid development of deep learning, detection has advanced.",
        encoding="utf-8",
    )
    result = run_script("manuscript_audit.py", str(sample), "--checks", "style")
    assert "Ceremonial opener" in result.stdout


def test_manuscript_audit_counts_characters_per_line_for_highlights(tmp_path):
    """Elsevier highlights cap at 85 characters including spaces."""
    sample = tmp_path / "highlights.txt"
    sample.write_text(
        "- A short highlight\n"
        "- " + "x" * 200 + "\n",
        encoding="utf-8",
    )
    result = run_script(
        "manuscript_audit.py", str(sample), "--limit-chars", "85", "--per-line"
    )
    assert "Over by" in result.stdout


def test_manuscript_audit_reports_word_limit_overrun(tmp_path):
    sample = tmp_path / "abstract.txt"
    sample.write_text(" ".join(["word"] * 300), encoding="utf-8")
    result = run_script(
        "manuscript_audit.py", str(sample), "--limit-words", "250", "--checks", "claims"
    )
    assert "300 / 250" in result.stdout


def test_manuscript_audit_is_clean_on_careful_writing(tmp_path):
    """Well-hedged, evidence-bounded prose must not generate noise."""
    sample = tmp_path / "clean.md"
    sample.write_text(
        "We propose a segmentation framework for CT imaging. The encoder "
        "extracts multi-scale features, which the fusion module combines.\n\n"
        "On the external cohort the method reached a mean Dice of 0.83 "
        "(SD 0.04), compared with 0.79 for the baseline (paired t-test, "
        "p = 0.01).\n\n"
        "Performance degrades on scans below 1 mm slice thickness, and "
        "prospective validation is still required.",
        encoding="utf-8",
    )
    result = run_script("manuscript_audit.py", str(sample))
    assert "No configured issues detected" in result.stdout


def test_manuscript_audit_rejects_an_unknown_check(tmp_path):
    sample = tmp_path / "draft.md"
    sample.write_text("text", encoding="utf-8")
    result = run_script("manuscript_audit.py", str(sample), "--checks", "nonsense", check=False)
    assert result.returncode == 2
    assert "Unknown check" in result.stderr


def test_manuscript_audit_accepts_stdin():
    result = run_script(
        "manuscript_audit.py",
        "--checks",
        "style",
        input_text="众所周知，该问题非常重要。",
    )
    assert "Manuscript Audit" in result.stdout


# ---------------------------------------------------------------------------
# terminology_checker
# ---------------------------------------------------------------------------


def test_terminology_checker_detects_mixed_terms_from_file(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text(
        "本文关注目标检测任务，同时也将对象检测作为核心问题，并讨论鲁棒性与稳健性。",
        encoding="utf-8",
    )
    result = run_script("terminology_checker.py", str(sample))
    assert "Terminology Consistency Report" in result.stdout
    assert "目标检测" in result.stdout and "对象检测" in result.stdout
    assert "鲁棒性" in result.stdout and "稳健性" in result.stdout


def test_terminology_checker_reports_the_dominant_variant(tmp_path):
    """Normalizing to the author's dominant form means fewer edits."""
    sample = tmp_path / "sample.md"
    sample.write_text(
        "目标检测很重要。目标检测的方法很多。目标检测的评估。此处写作对象检测。",
        encoding="utf-8",
    )
    result = run_script("terminology_checker.py", str(sample))
    assert "目标检测（3 次）" in result.stdout


def test_terminology_checker_is_quiet_on_consistent_text(tmp_path):
    sample = tmp_path / "sample.md"
    sample.write_text("本文关注目标检测任务，并讨论其鲁棒性。", encoding="utf-8")
    result = run_script("terminology_checker.py", str(sample))
    assert "No configured variant groups co-occur" in result.stdout


def test_terminology_checker_accepts_stdin():
    result = run_script(
        "terminology_checker.py",
        input_text="该方法用于语义分割，也可被描述为语义划分。",
    )
    assert "语义分割" in result.stdout and "语义划分" in result.stdout


def test_terminology_checker_json_output_is_parseable():
    result = run_script(
        "terminology_checker.py", "--json", input_text="目标检测与对象检测。"
    )
    payload = json.loads(result.stdout)
    assert payload and payload[0]["recommended"] == "目标检测"


# ---------------------------------------------------------------------------
# structure_checker
# ---------------------------------------------------------------------------


def test_structure_checker_reports_missing_abstract_elements(tmp_path):
    sample = tmp_path / "abstract.md"
    sample.write_text(
        "医学影像分割在临床辅助分析中具有价值。本文提出一种轻量化网络。",
        encoding="utf-8",
    )
    result = run_script("structure_checker.py", "--section", "abstract", str(sample))
    assert "Section Structure Check" in result.stdout
    assert "Possibly missing" in result.stdout
    assert "Evidence" in result.stdout


def test_structure_checker_supports_every_configured_section(tmp_path):
    sample = tmp_path / "draft.md"
    sample.write_text("本文提出一种方法并进行了实验验证。", encoding="utf-8")
    for section in [
        "abstract",
        "introduction",
        "related_work",
        "method",
        "experiment",
        "discussion",
        "conclusion",
    ]:
        result = run_script("structure_checker.py", "--section", section, str(sample))
        assert f"Section: {section}" in result.stdout


def test_structure_checker_counts_placeholders(tmp_path):
    """Placeholders must never survive into a submission."""
    sample = tmp_path / "abstract.md"
    sample.write_text(
        "本文提出一种方法。实验在 [请填写数据集名称] 上进行，取得 "
        "[请填写主要指标] 的结果，表明该方法有效。",
        encoding="utf-8",
    )
    result = run_script("structure_checker.py", "--section", "abstract", str(sample))
    assert "2 placeholder(s)" in result.stdout


def test_structure_checker_json_output_is_parseable(tmp_path):
    sample = tmp_path / "abstract.md"
    sample.write_text("本文提出一种方法。", encoding="utf-8")
    result = run_script(
        "structure_checker.py", "--section", "abstract", str(sample), "--json"
    )
    payload = json.loads(result.stdout)
    assert payload["section"] == "abstract"
    assert "missing" in payload


def test_structure_checker_rejects_empty_input():
    result = run_script(
        "structure_checker.py", "--section", "abstract", input_text="   ", check=False
    )
    assert result.returncode == 2


# ---------------------------------------------------------------------------
# Backward compatibility and repository lint
# ---------------------------------------------------------------------------


def test_legacy_wrappers_still_work():
    """Anyone with existing scripts pointing at the old names keeps working."""
    terminology = run_script(
        "term_consistency_check.py", input_text="目标检测与对象检测混用。"
    )
    assert "Terminology Consistency Report" in terminology.stdout

    structure = run_script(
        "section_audit.py", "--section", "abstract", input_text="本文提出一种方法。"
    )
    assert "Section Structure Check" in structure.stdout


def test_skill_lint_passes_on_the_repository():
    result = run_script("skill_lint.py", str(ROOT))
    assert "Skill Lint Report" in result.stdout
    assert "PASS" in result.stdout
