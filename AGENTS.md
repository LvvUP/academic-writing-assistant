# AGENTS.md

## Repository purpose

An Academic Writing Assistant Skill for Chinese and English research
manuscripts: polishing, translation, section drafting, reviewer responses and
rebuttals, submission materials, and whole-draft consistency checking.

## What this Skill is actually for

Not "make the prose flow better" -- models do that easily, and that is the
danger: fluent prose quietly upgrades claims. The Skill exists to improve
writing *without moving the boundary between what the evidence supports and
what it does not*, and to make that boundary cheap for the author to audit.

Any change that weakens the fidelity contract or the integrity boundaries
defeats the purpose of the project.

## Working rules

- Preserve the fidelity contract in `SKILL.md`: the three zones (locked,
  load-bearing, free surface) and the L1/L2/L3 change tiers.
- Preserve citation safety and the fabrication prohibitions. These are not
  decoration; they are what makes the output usable in a real submission.
- Keep `SKILL.md` lean. Detailed rules belong in `references/`.
- Explain *why* an instruction matters rather than stacking imperatives. The
  model following these instructions has good judgment; give it the reasoning
  and it will handle cases the rules did not anticipate.
- Examples must not contain real citations, real unpublished results, or
  private user data. Invented illustrative content must be obviously
  illustrative.
- Do not add claims about venue policies without a verifiable source. Publisher
  and conference requirements change; where they differ by venue, say so and
  point the author to the venue's own guide.
- Run `python -m pytest tests/` after changing scripts or repository structure.
- Keep the Revision Compass logo in both READMEs. The lint script and tests
  enforce this.
- Preserve AGPL-3.0-only for the current project and retain the historical MIT
  notices and grants. Keep root and standalone package licenses in sync.
- Put raw development records and private material in `.internal/` or `.local/`.
  Keep useful public documentation, synthetic examples, tests, and evaluations.
- Distinguish unit tests, model evaluations, Skill discovery, and native host
  execution. Report failures, untested coverage, and unavailable checks honestly.

## Structure

- `skills/academic-writing-assistant/SKILL.md` — core contract and routing.
- `skills/academic-writing-assistant/references/` — detailed rules, loaded on demand.
- `skills/academic-writing-assistant/scripts/` — deterministic checks.
- `skills/academic-writing-assistant/assets/` — terminology maps.
- `examples/`, `evals/`, `docs/`, `tests/` — usage, evaluation, documentation, verification.

## Definition of done

1. The Skill remains coherent and usable end to end.
2. Both READMEs remain accurate and beginner-friendly, with the logo intact.
3. The fidelity contract and integrity boundaries are preserved.
4. `python -m pytest tests/` passes.
5. `python skills/academic-writing-assistant/scripts/skill_lint.py .` passes.
6. No fabricated citations, results, or venue policy claims anywhere in the repo.
