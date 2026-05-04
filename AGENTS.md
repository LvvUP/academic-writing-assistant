# AGENTS.md

## Repository Purpose

This repository builds an Academic Writing Assistant Skill for Chinese and English academic paper writing, polishing, translation, section drafting, reviewer response, title optimization, and terminology consistency.

## Working Rules for Codex

- Preserve academic integrity rules in every Skill file.
- Do not remove citation safety rules.
- Do not introduce fake references, fake datasets, fake experimental numbers, or invented user metrics in examples.
- Keep `SKILL.md` concise and place detailed rules under `references/`.
- When adding examples, clearly mark placeholders and assumptions.
- If modifying scripts, run `python -m pytest tests/` before finalizing.
- If modifying README, keep installation, quick examples, roadmap, contribution guidance, and academic integrity sections.

## Project Structure

- `skills/academic-writing-assistant/`: core Skill.
- `skills/academic-writing-assistant/references/`: detailed workflow references.
- `skills/academic-writing-assistant/scripts/`: optional helper scripts.
- `skills/academic-writing-assistant/assets/`: terminology maps and other reusable assets.
- `examples/`: usage examples.
- `evals/`: manual evaluation cases.
- `docs/`: design, FAQ, scripts, and roadmap docs.
- `tests/`: script and repository tests.

## Definition of Done

A change is complete when:

1. The Skill remains usable and coherent.
2. The README remains beginner-friendly.
3. Academic integrity constraints are preserved.
4. Tests pass if scripts or repository structure are changed.
5. Examples do not contain fabricated real citations, unsupported results, or private user data.

