# Changelog

## 0.2.0

Reframes the Skill around fidelity: how far a revision may move a sentence
before it changes what the author is claiming, and how the author audits that.

### Added

- **Fidelity contract** in `SKILL.md`: locked zone / load-bearing language /
  free surface, with L1–L3 change tiers and a change ledger.
- `references/fidelity-protocol.md` — worked examples of the zones and tiers,
  including cases where an edit should not be made.
- `references/submission-package.md` — cover letters, highlights (85-character
  limit), generative-AI disclosure statements, CRediT contribution statements.
- `references/latex-and-formats.md` — editing `.tex` source without breaking
  `\cite{}`, `\ref{}`, math, or custom macros; Word and Markdown handling.
- `references/consistency-pass.md` — whole-draft terminology, abbreviation,
  symbol, tense, number, and claim-strength consistency.
- `scripts/fidelity_check.py` — verifies that citations, cross-references,
  numbers, math blocks, and macros survived a rewrite.
- `scripts/manuscript_audit.py` — abbreviation first-use, terminology drift,
  significance language without a test, unbounded claims, causal overreach,
  hedge stacking, tense mixing, and word/character limits.

### Changed

- `references/reviewer-response.md` now separates journal response letters from
  conference rebuttals, which differ in length budget, tense, and structure.
- `references/field-adapter.md` records what each field's reviewers attack
  rather than listing vocabulary; adds NLP/LLM and social sciences.
- `references/writing-workflows.md` rewritten around technique; adds
  compression to a limit.
- `references/style-guide-en.md` adds systematic Chinese-interference patterns.
- `references/style-guide-zh.md` adds thesis-versus-journal conventions.
- `references/task-router.md` covers bare-text input and requests to redirect.
- `scripts/structure_checker.py` adds related_work and conclusion sections,
  placeholder detection, and JSON output.
- `scripts/terminology_checker.py` reports occurrence counts and the dominant
  variant; the terminology map roughly doubles in coverage.
- READMEs rewritten in both languages, with the Revision Compass logo retained.

## 0.1.0

- Initial release.
- Academic Writing Assistant Skill with task routing, field adaptation, writing
  workflows, output templates, quality checklist, citation safety rules, and
  style guides.
- Terminology, section-structure, and repository lint helper scripts.
- Examples, tests, docs, and open-source governance files.
