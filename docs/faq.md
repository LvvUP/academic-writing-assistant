# FAQ

## Is this a paper-writing tool?

No. It is an academic expression and structure assistant. It helps revise,
translate, organize, and respond -- it does not replace the author's research,
evidence, or responsibility for what gets submitted.

## What is the "fidelity contract"?

Every sentence is read as three zones: locked content (numbers, citations,
equations) that is reproduced exactly, load-bearing language (hedges,
quantifiers, scope conditions) that may only change toward accuracy and always
with disclosure, and free surface (grammar, structure, phrasing) that is edited
freely.

Every edit is then tiered L1/L2/L3, so you can see at a glance which changes
touched your claims and which were just grammar.

## Why does it refuse to fix an obviously wrong number?

Because it cannot see your data. If the text says 92.3% and a table says 93.2%,
the Skill flags the discrepancy rather than picking one. The cost of flagging a
real error is thirty seconds of your attention; the cost of silently
harmonizing to the wrong value is a correction in proof.

## Can it write related work without references?

It can produce a structural draft with explicit `[citation needed]` slots, or
ask for your reference list. It will not generate citations. A fabricated
reference looks completely normal and survives into submissions.

## Will it help me lower my AI detection score?

It will not rewrite against a detector's score -- those tools are unreliable in
both directions, and optimizing against them is futile.

It will fix what usually causes the flag: uniform sentence length, evenly
weighted points, vague universals, stacked hedges, and connective overuse.
Fixing those produces text that is both better and less formulaic.

## Do I need to disclose that I used this?

Probably, if the assistance was substantive. Most publishers now require
disclosure of generative-AI use in writing, while exempting basic grammar and
spell checking. Elsevier asks for a dedicated section before the references;
ICLR treats undisclosed substantive LLM use as an ethics violation. Thresholds
differ by venue -- check your target journal's author guide.
`references/submission-package.md` has templates in both languages.

## Does it handle LaTeX?

Yes. Paste `.tex` source and you get `.tex` back, with `\cite{}`, `\ref{}`,
math, and custom macros preserved. Run `fidelity_check.py` afterward to verify
mechanically rather than by re-reading.

## Can it handle my field?

Built-in adapters cover ten fields, recording what reviewers in each actually
attack. Unlisted fields use the general workflow -- supply your field, target
venue, and key terminology when asking. Where information is missing, it uses
placeholders rather than inventing field facts.

## Journal response letter or conference rebuttal?

They are different documents. Journal letters are exhaustive, point-by-point,
and written after revisions are made. Conference rebuttals face hard character
caps, are prioritized by what moves scores, and are written before revisions
exist. The Skill handles them separately; tell it which venue you are
responding to.

## Does it require external services?

No. All Skill files and scripts are local, and the scripts use only the Python
standard library.
