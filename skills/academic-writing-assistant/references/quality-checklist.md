# Quality Checklist

Run before sending. The ordering is deliberate — integrity failures are unrecoverable once they reach a submission, style problems are merely annoying.

## 1. Fabrication — the blocking check

Scan your own output for anything you supplied that the user did not:

- [ ] No reference, author, year, venue, title, DOI, or arXiv ID that the user did not provide
- [ ] No dataset name, cohort size, or sample count
- [ ] No metric value, ablation result, p-value, or statistical test
- [ ] No equation, hyperparameter, or architectural detail
- [ ] No ethics approval, funding number, or institutional detail
- [ ] No claim that an experiment was run or a revision was made

Every gap is a visible placeholder instead. If you cannot tell whether a specific detail came from the user, it did not — remove it.

This check comes first because it is the only category where being wrong is not merely unhelpful but harmful.

## 2. Claim strength

- [ ] No hedge weakened or removed without disclosure
- [ ] No scope condition dropped ("on the evaluated datasets," "in this cohort")
- [ ] No quantifier inflated (some → most → all)
- [ ] No correlation rewritten as causation
- [ ] "significantly" appears only where a statistical test was reported
- [ ] "prove" not used for empirical results
- [ ] "first," "novel," "state-of-the-art" verified or flagged
- [ ] Negations, conditionals, and comparatives intact after rewriting

Compare against the original sentence by sentence. Drift accumulates quietly; a paragraph can end up stronger than its source without any single edit looking wrong.

## 3. Locked zone

- [ ] Every number identical, including decimal places
- [ ] Dataset, method, and model names spelled and capitalized as in the source
- [ ] Citation markers and keys unchanged
- [ ] Equations and inline math untouched
- [ ] Symbols and subscripts unchanged
- [ ] Cross-references (`Section 3.2`, `Table 4`, `\ref{}`) intact
- [ ] LaTeX commands and custom macros preserved

For anything longer than a paragraph, run `scripts/fidelity_check.py --before X --after Y` rather than trusting a read-through. Small tokens are exactly what attention skips.

## 4. Task fit

- [ ] The requested task is what was performed
- [ ] Target language correct
- [ ] Venue register appropriate, or the assumption stated
- [ ] Length limit respected and counted, if one exists
- [ ] Source format preserved (LaTeX in → LaTeX out)

## 5. Writing quality

- [ ] Grammar, articles, agreement, prepositions
- [ ] Tense consistent with section conventions
- [ ] Terminology consistent throughout
- [ ] Abbreviations defined at first use, then used consistently
- [ ] No ceremonial openers ("With the rapid development of…", 众所周知)
- [ ] No hedge stacking
- [ ] Sentence length varied
- [ ] Connectives carry real logic rather than decorating
- [ ] Nominalizations reduced

## 6. Reporting

- [ ] Deliverable comes first, clean and paste-ready
- [ ] L1 aggregated, not enumerated
- [ ] Every L2 has a one-line reason
- [ ] Every L3 is flagged with reasoning, or left as a query
- [ ] Queries are things only the author can resolve
- [ ] "暂无" written when there is nothing to confirm
- [ ] Ledger short enough to actually read
- [ ] Script results cited as evidence where a script was run

## 7. Proportion

- [ ] Ceremony matches task size — no ledger for a one-line fix
- [ ] Blocking questions avoided; assumptions labeled instead
- [ ] The response answers what was asked before offering anything extra

## Last look

Two questions, both worth asking honestly:

**If the author pasted this straight into their manuscript without reading my notes, would anything be wrong?** Placeholders will be caught. A silently strengthened claim will not.

**Did I leave good writing alone?** Manufactured changes teach the author that your edits are noise, and then they stop reading the ones that matter.
