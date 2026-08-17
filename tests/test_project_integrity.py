import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "academic-writing-assistant"


def test_skill_frontmatter_has_name_and_description():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter = text.split("---", 2)[1]
    assert "name: academic-writing-assistant" in frontmatter
    assert "description:" in frontmatter
    assert "[TODO:" not in frontmatter


def test_skill_description_covers_the_main_trigger_surfaces():
    """The description is all an agent sees before deciding to load the Skill.

    If it stops naming a task the Skill supports, that task silently stops
    triggering -- which looks like the Skill being bad rather than unloaded.
    """
    frontmatter = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
    lowered = frontmatter.lower()
    for surface in [
        "polish",
        "translat",
        "abstract",
        "rebuttal",
        "cover letter",
        "latex",
        "terminology",
    ]:
        assert surface in lowered, f"description no longer mentions {surface}"


def test_skill_states_the_fidelity_contract():
    """The three zones and three tiers are the mechanism the whole Skill rests on."""
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for zone in ["Locked zone", "Load-bearing language", "Free surface"]:
        assert zone in text
    for tier in ["L1", "L2", "L3"]:
        assert tier in text


def test_skill_keeps_fabrication_guardrails():
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "Never fabricate" in text or "Never invent" in text
    for forbidden in ["references", "datasets", "metric values"]:
        assert forbidden in text


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
    required_phrases = [
        "# Academic Writing Assistant",
        '<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">',
        "**中文** | [English](README_EN.md)",
        "项目定位",
        "保真契约",
        "锁定区",
        "承重语言",
        "自由表层",
        "核心功能",
        "支持的学术写作任务",
        "支持的研究领域",
        "内置领域适配预设",
        "不是支持范围上限",
        "通用学术写作流程",
        "安装",
        "Codex 安装",
        "Claude Code 安装",
        "其他 Agent 安装",
        "把这句话发给 Codex",
        "手动安装备用",
        "使用示例",
        "输出示例",
        "学术诚信",
        "路线图",
        "贡献指南",
        "许可证",
    ]
    for phrase in required_phrases:
        assert phrase in text, f"README.md missing: {phrase}"


def test_english_readme_contains_key_sections_and_language_switch():
    text = (ROOT / "README_EN.md").read_text(encoding="utf-8")
    required_phrases = [
        "# Academic Writing Assistant",
        '<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">',
        "[中文](README.md) | **English**",
        "Positioning",
        "fidelity contract",
        "Locked",
        "Load-bearing",
        "Free surface",
        "Core features",
        "Supported Writing Tasks",
        "Supported Research Fields",
        "Built-in Field Adapters",
        "not a limit",
        "general academic writing workflow",
        "Installation",
        "Install for Codex",
        "Install for Claude Code",
        "Install for Other Agents",
        "Send this prompt to Codex",
        "Manual fallback",
        "Quick Examples",
        "Example output",
        "Academic Integrity",
        "Roadmap",
        "Contributing",
        "License",
    ]
    for phrase in required_phrases:
        assert phrase in text, f"README_EN.md missing: {phrase}"
    assert "项目定位" not in text


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
    required_phrases = [
        "# Contributing / 贡献指南",
        "[中文](#中文) | [English](#english)",
        "## 中文",
        "欢迎为 Academic Writing Assistant 做贡献",
        "不接受的内容",
        "虚构参考文献、数据集、实验结果或评价指标",
        "## English",
        "Thank you for considering a contribution",
        "What We Do Not Accept",
        "Fake references, datasets, experiments, or evaluation metrics",
    ]
    for phrase in required_phrases:
        assert phrase in text


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


def test_examples_do_not_contain_citation_shaped_strings():
    """Illustrative text must not read as a real citation.

    Examples are the strongest signal the Skill has about what good output looks
    like. A plausible-looking reference in one contradicts the rule the Skill
    states most emphatically. The two files that discuss citation formats as
    subject matter are exempt.
    """
    import re

    author_year = re.compile(
        r"\((?:Smith|Zhang|Wang|Li|Chen|Liu|Kim|Brown|Johnson)\s+(?:et al\.|and)[^)]*,\s*(?:19|20)\d{2}\)"
    )
    exempt = {"fidelity-protocol.md", "citation-safety.md", "latex-and-formats.md"}
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or path.name in exempt:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not author_year.search(text), (
            f"{path.relative_to(ROOT)} contains a citation-shaped string; use a "
            "placeholder instead"
        )
