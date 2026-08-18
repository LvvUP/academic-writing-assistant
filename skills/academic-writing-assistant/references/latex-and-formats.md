# LaTeX and Manuscript Formats

Most real manuscripts do not arrive as clean prose. They arrive as LaTeX source, Word text with tracked changes, or a Markdown draft, and the formatting carries meaning that must survive the edit.

## Contents

- [Editing LaTeX source](#editing-latex-source)
- [What must survive verbatim](#what-must-survive-verbatim)
- [Math](#math)
- [Common LaTeX-specific errors](#common-latex-specific-errors)
- [Word and tracked changes](#word-and-tracked-changes)
- [Markdown drafts](#markdown-drafts)
- [Verifying the edit](#verifying-the-edit)

## Editing LaTeX source

When a user pastes LaTeX, return LaTeX. Stripping the markup to "clean up the text" destroys the author's compiled document and forces them to re-integrate by hand — which defeats the purpose of the edit and is where citation losses happen.

Working rules:

1. **Edit prose between the commands, not the commands.** Text inside `\textit{}` or `\caption{}` is prose and can be edited; the command itself is structure.
2. **Preserve line-break structure** where the author has one sentence per line. Many people write LaTeX this way deliberately for clean version-control diffs, and reflowing paragraphs into single long lines produces an unreviewable diff.
3. **Keep comments** (`%`). They frequently contain notes to co-authors.
4. **Do not renumber, reorder, or relabel** sections, equations, or figures. Numbering is generated at compile time; the labels are the real identifiers.
5. **Do not "fix" the preamble** unless asked. Package conflicts are their own problem and usually venue-specific.

## What must survive verbatim

Everything in this list is locked-zone content from `fidelity-protocol.md`, expressed in markup:

| Category | Examples |
|---|---|
| Citations | `\cite{}`, `\citep{}`, `\citet{}`, `\autocite{}`, `\footcite{}` |
| Cross-references | `\ref{}`, `\eqref{}`, `\autoref{}`, `\cref{}`, `\pageref{}`, `\label{}` |
| Math | `$…$`, `\(…\)`, `\[…\]`, `equation`, `align`, `gather`, `split` |
| Floats | `figure`, `table`, `tabular`, `\includegraphics{}` |
| Custom macros | `\newcommand` definitions and every use of them |
| Structure | `\section{}`, `\subsection{}`, `\paragraph{}` |
| Symbols and units | `\alpha`, `\sigma`, `\SI{}{}`, `\num{}` |

A dropped `\cite{}` compiles without error and produces an uncited claim — which is a plagiarism-adjacent problem, not a typo. A dropped `\ref{}` produces a `??` in the PDF. Neither raises an alarm during editing, which is exactly why they need mechanical verification rather than a careful read.

Macro uses deserve special attention: an author may define `\ours{}` or `\method{}` in the preamble. These look like arbitrary commands but carry the paper's method name throughout. Never expand them to plain text.

## Math

Treat every math environment as an opaque, immutable block. Do not:

- Reformat spacing inside math
- Convert `$…$` to `\(…\)` or vice versa
- Change `\times` to `×`, or any symbol to a Unicode equivalent
- Alter subscripts, superscripts, or delimiter sizing
- Rewrite an equation you believe is wrong

The last one matters most. If an equation looks incorrect — a mismatched dimension, an undefined symbol, an index that does not bind — raise it as a query with your reasoning. You cannot verify the derivation, and a "corrected" equation that reaches a reviewer is far worse than an author's own error, because the author will not think to re-check it.

Text *around* math is editable, and often needs it. `Fig.~\ref{fig:arch}` shows... — the `~` is a non-breaking space and should stay.

## Common LaTeX-specific errors

Worth checking in any manuscript you touch:

- **Quotes.** LaTeX needs `` `` `` and `''` for curly quotes. A straight `"` renders wrong.
- **Non-breaking spaces.** `Section~\ref{}`, `Figure~\ref{}`, `Table~\ref{}` — the tilde prevents an orphaned label at a line break. Add it where missing; never remove it.
- **Escaped characters.** `%` `&` `_` `#` `$` need backslashes in text mode. An unescaped `%` silently comments out the rest of the line — a real content-loss bug.
- **Dashes.** `-` hyphen, `--` numeric range (`pages 3--7`), `---` em dash. Ranges written with a single hyphen are extremely common in drafts.
- **`\eqref` vs `\ref`** for equations, which controls whether the parentheses appear.
- **Abbreviation spacing.** `e.g.\ ` and `i.e.\ ` need the escaped space, or LaTeX applies sentence-ending spacing after the period.

Fixing these is L1 work — report them in the aggregate line.

## Word and tracked changes

When a user pastes text from Word:

- Ask whether they want plain revised text or a change list they can apply as tracked changes themselves. The second is more work for them but preserves their review workflow with co-authors.
- Text pasted from Word often carries smart quotes, non-breaking spaces, and stray formatting artifacts. Normalize silently; it is L1.
- If they paste text that already contains tracked-change markup or comment text, ask what to do with it before touching it — those are usually co-author comments, and deleting a co-author's question is a social problem, not just an editing one.

When a user needs the change ledger to be applicable in Word, format it as find/replace pairs rather than prose descriptions.

## Markdown drafts

Straightforward, but preserve:

- Heading levels, since they usually map onto the paper's section structure
- Reference-style link definitions
- Code blocks and their language tags, verbatim
- Footnote markers
- Table alignment rows

Markdown drafts are frequently converted to LaTeX or Word later, so structural consistency matters more than it appears.

## Verifying the edit

Do not rely on reading to confirm that protected items survived. Citations and numbers are exactly the kind of small tokens that human and model attention skips, and the failure is silent.

```bash
python scripts/fidelity_check.py --before original.tex --after revised.tex
```

It reports citation keys, cross-references, numeric values, math blocks, and macro uses that were added, dropped, or altered. Run it on any edit longer than a paragraph and report the result to the author as evidence:

> fidelity_check：引用 14/14、交叉引用 6/6、公式 3/3、数值 9/9 全部保留，未发现丢失。

If it reports a difference you intended — you split one sentence containing a number into two, and the number now appears once — explain that. If it reports a difference you did not intend, fix it before responding. That is the entire point of the script: it catches what re-reading does not.
