import json
import sys
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "academic-writing-assistant"
sys.path.insert(0, str(SKILL_DIR / "scripts"))
import skill_lint as lint



def test_skill_frontmatter_has_name_and_description():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert lint.validate_frontmatter(text, SKILL_DIR.name) == []


def test_skill_description_is_specific_and_excludes_unrelated_requests():
    # Behavioral trigger evaluation lives in evals; this only checks packaging.
    import yaml
    data = yaml.safe_load((SKILL_DIR / "SKILL.md").read_text().split("---", 2)[1])
    assert isinstance(data["description"], str)
    assert 1 <= len(data["description"]) <= 1024
    assert "academic" in data["description"].lower()


def test_skill_states_the_fidelity_contract():
    """The three zones and three tiers are the mechanism the whole Skill rests on."""
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for zone in ["Locked zone", "Load-bearing language", "Free surface"]:
        assert zone in text
    for tier in ["L1", "L2", "L3"]:
        assert tier in text


def test_skill_keeps_fabrication_guardrails():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert any(word in text for word in ("Never fabricate", "Never invent", "不编造"))
    for alternatives in [("references", "参考文献"), ("datasets", "数据集"), ("metric values", "实验结果")]:
        assert any(word in text for word in alternatives)


def test_reference_files_are_complete():
    required = {
        "task-router.md",
        "field-adapter.md",
        "writing-workflows.md",
        "style-guide-zh.md",
        "style-guide-en.md",
        "output-templates.md",
        "quality-checklist.md",
        "examples.md",
        "fidelity-protocol.md",
        "citation-safety.md",
        "reviewer-response.md",
        "terminology.md",
        "submission-package.md",
        "latex-and-formats.md",
        "consistency-pass.md",
    }
    existing = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    assert required.issubset(existing)


def test_every_reference_named_in_skill_md_exists():
    """A dangling pointer sends the agent looking for a file that is not there."""
    import re

    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for name in set(re.findall(r"references/([a-z0-9-]+\.md)", text)):
        assert (SKILL_DIR / "references" / name).exists(), (
            f"SKILL.md points at missing reference: {name}"
        )


def test_scripts_are_present():
    required = {
        "fidelity_check.py",
        "manuscript_audit.py",
        "terminology_checker.py",
        "structure_checker.py",
        "skill_lint.py",
    }
    existing = {path.name for path in (SKILL_DIR / "scripts").glob("*.py")}
    assert required.issubset(existing)


def test_terminology_map_is_valid_and_well_formed():
    data = json.loads(
        (SKILL_DIR / "assets" / "terminology-map.zh-en.json").read_text(encoding="utf-8")
    )
    fields = {key: value for key, value in data.items() if not key.startswith("_")}
    assert fields, "terminology map has no field groups"
    for field, entries in fields.items():
        for entry in entries:
            label = entry.get("recommended_zh", "?")
            assert len(entry.get("variants_zh", [])) >= 2, (
                f"{field}/{label}: a variant group needs at least two forms to "
                "detect a mix"
            )
            assert entry["recommended_zh"] in entry["variants_zh"], (
                f"{field}/{label}: recommended form is not among the variants"
            )
            assert entry.get("note"), f"{field}/{label}: missing an explanatory note"


def test_chinese_readme_contains_key_sections_and_language_switch():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert lint.validate_logo(text, ROOT) == []
    assert re.search(r"\[English\]\(README_EN.md\)", text)
    for term in ["安装", "示例", "诚信", "许可"]:
        assert term in text
    assert "路线图" in text or "ROADMAP.md" in text
    assert "贡献" in text or "CONTRIBUTING.md" in text


def test_english_readme_contains_key_sections_and_language_switch():
    text = (ROOT / "README_EN.md").read_text(encoding="utf-8")
    assert lint.validate_logo(text, ROOT) == []
    assert re.search(r"\[中文\]\(README.md\)", text)
    for term in ["install", "example", "integrity", "license", "roadmap", "contribut"]:
        assert term in text.lower()


def test_readmes_document_the_new_scripts():
    """A script nobody knows about does not get run."""
    for name in ["README.md", "README_EN.md"]:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "fidelity_check.py" in text, f"{name} does not mention fidelity_check.py"
        assert "manuscript_audit.py" in text, (
            f"{name} does not mention manuscript_audit.py"
        )


def test_contributing_is_bilingual_and_integrity_focused():
    text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "中文" in text and "English" in text
    assert "贡献" in text and "contribut" in text.lower()
    assert "虚构" in text or "编造" in text
    assert "references" in text.lower()


def test_logo_assets_and_plugin_manifest_are_configured():
    assert (ROOT / "assets" / "logo" / "revision-compass.svg").exists()
    assert (ROOT / "assets" / "logo" / "revision-compass.png").exists()
    manifest = json.loads(
        (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    interface = manifest["interface"]
    assert interface["logo"] == "./assets/logo/revision-compass.png"
    assert interface["composerIcon"] == "./assets/logo/revision-compass.png"
    assert "YOUR_GITHUB_USERNAME" not in json.dumps(manifest)


def test_public_examples_are_explicitly_synthetic():
    # A surname regex cannot establish citation truth. Every worked example
    # instead declares its fixture provenance; support is graded in evals.
    for path in [*(ROOT / "examples").glob("*.md"), SKILL_DIR / "references/examples.md"]:
        text = path.read_text(encoding="utf-8")
        assert re.search(r"合成|虚构示例|synthetic|illustrative", text, re.I), str(path)


def test_documentation_inventory_does_not_read_private_records():
    paths = lint.public_files(ROOT)
    assert ROOT / "docs/design.md" in paths
    assert all(".internal" not in path.relative_to(ROOT).parts for path in paths)
