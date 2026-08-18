# Acceptance Checklist

## Skill structure

- [ ] `SKILL.md` exists with valid frontmatter (`name`, `description`).
- [ ] The description names the main trigger surfaces, including rebuttals,
      cover letters, LaTeX, and terminology.
- [ ] All 15 reference files exist under `references/`.
- [ ] Every `references/*.md` path named in `SKILL.md` resolves.
- [ ] All five scripts exist under `scripts/`.

## Fidelity contract

- [ ] `SKILL.md` states the three zones: locked, load-bearing, free surface.
- [ ] The L1/L2/L3 change tiers are defined, with reporting rules for each.
- [ ] The ledger format is specified.
- [ ] "Flag, never fix" applies to locked-zone content.
- [ ] `fidelity-protocol.md` includes worked examples, including at least one
      case where an edit should *not* be made.

## Academic integrity

- [ ] Fabrication prohibitions cover citations, datasets, metric values,
      statistical tests, ethics approvals, and claims about completed revisions.
- [ ] Placeholder usage is specified and visually unmistakable.
- [ ] Detection-evasion requests are redirected with genuine help, not lectures.
- [ ] AI disclosure guidance exists, and points authors to their venue's guide
      rather than asserting one universal rule.
- [ ] No file in the repository contains a citation-shaped string outside the
      files that discuss citation formats as subject matter.

## Coverage

- [ ] Journal response letters and conference rebuttals are handled separately.
- [ ] Submission materials: cover letter, highlights, AI disclosure, CRediT.
- [ ] LaTeX, Word, and Markdown handling documented.
- [ ] Whole-draft consistency: terminology, abbreviations, symbols, tense,
      numbers, claim strength.
- [ ] Field adapters record what reviewers attack, not only vocabulary.
- [ ] Unlisted fields are explicitly supported via the general workflow.

## Scripts

- [ ] `fidelity_check.py` detects dropped citations, changed numbers, truncated
      equations, and lost macros.
- [ ] `manuscript_audit.py` flags significance language without a test, and stays
      quiet when a test is reported.
- [ ] Neither script fires on careful, well-hedged writing.
- [ ] Legacy wrappers still work.
- [ ] `python -m pytest tests/` passes.
- [ ] `python skills/academic-writing-assistant/scripts/skill_lint.py .` passes.

## Documentation

- [ ] Both READMEs retain the Revision Compass logo and the language switch.
- [ ] Both READMEs document `fidelity_check.py` and `manuscript_audit.py`.
- [ ] Installation instructions cover Codex, Claude Code, and other agents.
- [ ] Examples show the change ledger rather than only revised text.
- [ ] CHANGELOG records what changed and why.
