# Script Usage

The scripts are intentionally lightweight and use only the Python standard library.

## Terminology Checker

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py examples/terminology-check.md
```

Reads a file or stdin and reports configured terminology variants that appear together.

```bash
echo "目标检测和对象检测不应混用。" | python skills/academic-writing-assistant/scripts/terminology_checker.py
```

## Structure Checker

```bash
python skills/academic-writing-assistant/scripts/structure_checker.py --section abstract examples/abstract-writing.md
```

Supported sections:

- `abstract`
- `introduction`
- `method`
- `experiment`
- `discussion`

The checker reports possibly missing structural elements. It does not validate facts.

## Skill Lint

```bash
python skills/academic-writing-assistant/scripts/skill_lint.py .
```

Checks core repository files, required references, README sections, plugin JSON, and a small set of forbidden overclaiming patterns.

