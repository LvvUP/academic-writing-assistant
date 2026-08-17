# Script Usage

All scripts use only the Python standard library. They handle the checks that
are mechanical and that language models perform unreliably -- exact-match
survival of citations and numbers, abbreviation first-use, counting against a
hard limit.

Findings are prompts to look, not verdicts. No script here can detect the
failures that matter most: fabricated content, and claims that outrun their
evidence.

## fidelity_check.py

The one to run by default after any substantial rewrite.

```bash
python skills/academic-writing-assistant/scripts/fidelity_check.py \
    --before original.tex --after revised.tex
```

Compares locked-zone content between two versions and reports what changed:

| Category | Covers |
|---|---|
| LaTeX citation keys | `\cite{}`, `\citep{}`, `\citet{}`, `\autocite{}`, multi-key groups split individually |
| Bracket citations | `[12]`, `[3, 5-7]` |
| Author-year citations | `(Author et al., 2021)` |
| Cross-references | `\ref{}`, `\eqref{}`, `\cref{}`, `\label{}` |
| Structural references | `Section 3.2`, `Table 4`, `Fig. 5`, `第 3 节` |
| Math blocks | `$...$`, `\(...\)`, `\[...\]`, `equation`, `align`, `gather`, `split` |
| Numeric values | Including percentages, thousands separators, scientific notation |
| Custom macros | Author-defined commands such as `\ours{}` or `\method{}` |

Comparison is by multiset, so an item appearing three times must still appear
three times. Numbers inside citation markers are excluded, since those are
tracked as citations.

Options:

- `--json` for machine-readable output
- `--strict` to exit non-zero when anything differs

Why it exists: a dropped `\cite{}` compiles without error and reads normally,
but it produces an uncited claim. A changed decimal is invisible on re-reading.
These are exactly the failures that attention skips.

Not every difference is a bug -- splitting a sentence can duplicate a reference,
and author-requested rounding changes a number. Report the reason rather than
dismissing the finding.

## manuscript_audit.py

Whole-draft hygiene.

```bash
python skills/academic-writing-assistant/scripts/manuscript_audit.py draft.md
python skills/academic-writing-assistant/scripts/manuscript_audit.py abstract.txt \
    --section abstract --limit-words 250
python skills/academic-writing-assistant/scripts/manuscript_audit.py highlights.txt \
    --limit-chars 85 --per-line
```

Checks:

- `abbreviations` — used before definition, defined but used once, used repeatedly without definition
- `claims` — significance language with no test anywhere in the text, unbounded superlatives, causal verbs where the evidence may be associational
- `style` — ceremonial openers, stacked hedges
- `tense` — paragraphs mixing method-present with experiment-past
- `terminology` — English variant pairs that may denote one concept

Select a subset with `--checks abbreviations,claims`. Add `--section` for
targeted guidance. `--json` for machine-readable output.

Length checking counts English words and CJK characters separately, and
characters including spaces. Use `--per-line` for highlights and key points,
where each bullet has its own limit -- Elsevier allows 85 characters including
spaces, and the limit is tighter than it looks.

## terminology_checker.py

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py draft.md
python skills/academic-writing-assistant/scripts/terminology_checker.py draft.md \
    --map custom-terms.json
```

Reports configured Chinese variant groups that co-occur, with occurrence counts
and which form dominates. Normalizing to the dominant variant is usually right:
fewer edits, and it preserves the author's own preference.

It does not decide anything. Some drafts distinguish nearby terms deliberately,
and where both variants are standard the choice belongs to the author.

Extend coverage by editing `assets/terminology-map.zh-en.json`. Keys beginning
with `_` hold documentation rather than terms.

## structure_checker.py

```bash
python skills/academic-writing-assistant/scripts/structure_checker.py \
    --section abstract draft.md
```

Sections: `abstract`, `introduction`, `related_work`, `method`, `experiment`,
`discussion`, `conclusion`.

A keyword scan. It detects whether an element is mentioned, not whether it is
argued well. Its value is catching outright omissions -- an abstract with no
results sentence, an experiment section that never names a baseline -- which are
easy to miss when re-reading your own draft. It also counts placeholders so
none reach submission.

## skill_lint.py

```bash
python skills/academic-writing-assistant/scripts/skill_lint.py .
```

Repository-level checks: required Skill files and references, README structure
in both languages, logo assets, plugin manifest, and a small set of forbidden
overclaiming patterns. Used in CI and before releases.

## Backward compatibility

`section_audit.py` and `term_consistency_check.py` remain as thin wrappers
around `structure_checker.py` and `terminology_checker.py` for anyone with
existing scripts.
