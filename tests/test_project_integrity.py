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
    }
    existing = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    assert required.issubset(existing)


def test_chinese_readme_contains_key_sections_and_language_switch():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    required_phrases = [
        "# Academic Writing Assistant",
        '<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">',
        "**中文** | [English](README_EN.md)",
        "项目定位",
        "为什么需要",
        "核心功能",
        "支持的学术写作任务",
        "支持的研究领域",
        "安装",
        "Codex 安装",
        "Claude Code 安装",
        "其他 Agent 安装",
        "把这句话发给 Codex",
        "手动安装备用",
        "使用示例",
        "学术诚信",
        "路线图",
        "贡献指南",
        "许可证",
    ]
    for phrase in required_phrases:
        assert phrase in text
    assert "不是一组零散 Prompt，而是" not in text


def test_english_readme_contains_key_sections_and_language_switch():
    text = (ROOT / "README_EN.md").read_text(encoding="utf-8")
    required_phrases = [
        "# Academic Writing Assistant",
        '<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">',
        "[中文](README.md) | **English**",
        "Positioning",
        "Why This Skill",
        "Core Features",
        "Supported Writing Tasks",
        "Supported Research Fields",
        "Installation",
        "Install for Codex",
        "Install for Claude Code",
        "Install for Other Agents",
        "Send this prompt to Codex",
        "Manual fallback",
        "Quick Examples",
        "Academic Integrity",
        "Roadmap",
        "Contributing",
        "License",
    ]
    for phrase in required_phrases:
        assert phrase in text
    assert "项目定位" not in text


def test_logo_assets_and_plugin_manifest_are_configured():
    assert (ROOT / "assets" / "logo" / "revision-compass.svg").exists()
    assert (ROOT / "assets" / "logo" / "revision-compass.png").exists()
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    interface = manifest["interface"]
    assert interface["logo"] == "./assets/logo/revision-compass.png"
    assert interface["composerIcon"] == "./assets/logo/revision-compass.png"
    assert "YOUR_GITHUB_USERNAME" not in json.dumps(manifest)
