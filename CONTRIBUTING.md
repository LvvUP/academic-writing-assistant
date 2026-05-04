# Contributing

Thank you for considering a contribution to Academic Writing Assistant.

This project welcomes careful, academically responsible improvements. The best contributions make the Skill more useful without weakening its evidence and integrity boundaries.

## Ways to Contribute

- Add or improve field adaptation rules.
- Add terminology pairs and inconsistency patterns.
- Improve output templates for common academic tasks.
- Add safe examples that do not include private or unpublished research content.
- Improve helper scripts and tests.
- Improve documentation for installation and usage.

## What We Do Not Accept

- Fake references, fake datasets, fake experiments, or invented metrics.
- Features that encourage unsupported claims or paper ghostwriting.
- Examples containing private, sensitive, or unpublished manuscript content.
- Claims of official certification, user counts, download counts, or star counts without proof.
- Wording that promises publication, review acceptance, or guaranteed academic outcomes.

## Pull Request Checklist

Before opening a PR:

- [ ] The change preserves academic integrity guardrails.
- [ ] New examples use safe sample text and placeholders where needed.
- [ ] New terminology entries include a short note.
- [ ] `SKILL.md` remains concise; detailed rules live in `references/`.
- [ ] `python -m pytest tests/` passes.
- [ ] README and docs are updated if behavior changes.

## Adding a New Field

Add a field section to `skills/academic-writing-assistant/references/field-adapter.md` with:

1. common tasks;
2. writing focus;
3. common terms;
4. expressions or claims to avoid.

If useful, add terminology entries to `assets/terminology-map.zh-en.json` and a safe example under `examples/`.

