# Design

## The problem

An author sends a rough paragraph and receives polished English. The English is
better than anything they would have written, so they accept all of it without
line-by-line comparison -- comparing is slow, and the output looks
authoritative.

That trust is the product, and it is also the risk. Every unflagged
strengthening rides along into a submitted manuscript, where it becomes the
author's word and the author's responsibility.

Fluent academic prose is not the hard part; models produce it easily. The hard
part is producing it without moving the boundary between what the evidence
supports and what it does not -- and making that boundary cheap for the author
to inspect.

## The mechanism

**Three zones.** Every sentence is read as locked content (numbers, citations,
equations, names), load-bearing language (hedges, quantifiers, scope
conditions, causal verbs, novelty claims), and free surface (everything else).
The zones determine what may be edited without permission.

**Three tiers.** Every edit is classified L1 (surface), L2 (structure), or L3
(claim). The tier determines how much explanation the author needs: L1
aggregated, L2 with one line each, L3 never silent.

**A ledger.** L2 and L3 changes are reported as a scannable table with
fragments rather than whole sentences. The design constraint is that it must be
readable in about a minute; a ledger too long to read is no ledger at all.

The reasoning behind tiering: an author facing 40 undifferentiated changes
accepts all of them without reading. An author facing "12 L1, 3 L2, 1 L3
needing confirmation" reads the four that matter. The goal is not to minimize
changes but to make the consequential ones easy to find.

## Architecture

- `SKILL.md` -- the fidelity contract, routing, output contract, integrity
  boundaries. Kept lean so it loads cheaply on every invocation.
- `references/` -- detailed rules, loaded on demand. Progressive disclosure
  keeps the always-loaded portion small while allowing depth where needed.
- `scripts/` -- deterministic checks. Anything mechanical and verifiable
  belongs here rather than in prose instructions, because "did the citation
  survive" should be answered with evidence rather than confidence.
- `assets/` -- terminology maps for rule-based scanning.
- `examples/`, `evals/`, `tests/`, `docs/` -- usage, evaluation, verification.

## Design choices

1. **Aggressive on the surface, rigorous about the boundary.** Timid edits that
   leave bad writing intact fail the author just as surely as unflagged
   overclaiming does.
2. **Flag, never fix, in the locked zone.** The Skill cannot see the data,
   tables, or bibliography. A silently harmonized number is the worst failure
   mode available, because it is invisible and it propagates.
3. **Field adaptation as reviewer perspective.** Knowing that remote sensing
   reviewers attack geographic generalization is more actionable than knowing
   remote sensing vocabulary.
4. **Placeholders over plausible invention.** A conspicuous
   `[请补充主要定量结果]` is a service; a plausible fabricated number is a
   landmine that survives into submission.
5. **Proportionate ceremony.** A one-sentence fix returns a fixed sentence.
   Ceremony scaled to a trivial task trains the author to skim the format when
   it actually matters.
6. **Redirect rather than refuse, where the underlying need is legitimate.**
   "Lower my AI detection score" is usually a real writing problem wearing the
   wrong clothes.

## Non-goals

- It does not promise acceptance or predict review outcomes.
- It does not replace domain expert review.
- It does not generate verified references without source material.
- It does not judge scientific validity. It can assess whether a claim is
  supported by the text in front of it; it cannot assess whether the science is
  correct, and polished prose must never imply an endorsement of the research.
