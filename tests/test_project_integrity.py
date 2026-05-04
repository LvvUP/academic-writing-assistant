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


def test_readme_contains_key_sections():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    required_phrases = [
        "# Academic Writing Assistant",
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
    for phrase in required_phrases:
        assert phrase in text

