# Detailed Roadmap

Implementation detail behind the root `ROADMAP.md`.

## v0.1

- Core Skill with modular references.
- Field adapter for ten fields.
- Terminology and structure checker scripts.
- README, examples, tests, open-source governance files.

## v0.2 (current)

- Fidelity contract in `SKILL.md`: three zones, three change tiers, ledger format.
- `fidelity-protocol.md` with worked examples, including edits that should not be made.
- `reviewer-response.md` split by venue type, with hard-case handling.
- `submission-package.md`: cover letter, highlights with the 85-character limit,
  generative-AI disclosure templates in both languages, CRediT roles.
- `latex-and-formats.md`: protected markup inventory, math handling, common
  LaTeX errors, Word and Markdown notes.
- `consistency-pass.md`: terminology, abbreviations, symbols, tense, numbers,
  method naming, cross-references, and claim consistency across sections.
- `fidelity_check.py`: multiset comparison of citations, cross-references,
  numbers, math blocks, and custom macros between two versions.
- `manuscript_audit.py`: abbreviation first-use, claim-strength scanning,
  filler and hedge stacking, tense mixing, terminology drift, length limits.
- `structure_checker.py`: added related_work and conclusion, placeholder
  counting, JSON output.
- `terminology_checker.py`: occurrence counts, dominant-variant reporting,
  `_meta` key support in the map.

## v0.3

- Discipline-specific reviewer attack patterns beyond the current ten fields.
- Caption and float conventions.
- Degree-thesis structure per common Chinese university templates.
- Appeal and major-revision response examples.

## v0.4

- Terminology map expansion with per-field notes and contributor guidance.
- Additional keyword rules per section and field.
- Larger example library.

## v1.0

- Freeze structure, publish contributor guide for field packs.
- Full evaluation documentation and release notes.
