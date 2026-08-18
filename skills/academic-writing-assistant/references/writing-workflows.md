# Writing Workflows

How to actually execute each task. Every workflow assumes the fidelity contract in `SKILL.md` is already in force — these add task-specific technique on top of it.

## Contents

- [Polishing](#polishing)
- [Expansion](#expansion)
- [Merging](#merging)
- [Compression to a limit](#compression-to-a-limit)
- [Translation CN→EN](#translation-cnen)
- [Translation EN→CN](#translation-encn)
- [Abstract](#abstract)
- [Introduction](#introduction)
- [Related work](#related-work)
- [Method](#method)
- [Experiment](#experiment)
- [Discussion, limitations, future work](#discussion-limitations-future-work)
- [Title and contributions](#title-and-contributions)
- [Naturalization](#naturalization)
- [Prompt optimization](#prompt-optimization)

## Polishing

The most requested task and the easiest to do badly, because "polish" invites uniform smoothing that flattens a paper's argument into pleasant mush.

1. **Read the whole passage before editing anything.** Find the claim it is making. Local sentence fixes that fight the paragraph's argument are worse than no edit.
2. **Diagnose before rewriting.** Most drafts fail for one identifiable reason, not forty: buried topic sentence, missing logical connective, hedge stacking, nominalization, or a claim that outruns its evidence. Naming the pattern produces a better fix than sentence-by-sentence grinding, and gives the author something they can apply themselves next time.
3. **Fix structure first, surface second.** Reordering for a clear topic sentence often dissolves problems that looked like grammar problems.
4. **Apply the fidelity zones.** Free surface aggressively; load-bearing language only toward accuracy, disclosed; locked zone untouched.
5. **Re-read for meaning drift.** After rewriting, compare claim strength sentence by sentence against the original. This catch step matters more than any other, because drift accumulates silently across a paragraph.
6. **Report** per the output contract.

Chinese-authored English drafts concentrate on a handful of patterns — `style-guide-en.md` has the interference list. Recognizing them is usually faster than diagnosing from scratch.

A note on restraint: passages that are already good need little. Returning a lightly-touched draft with "这段结构清晰，仅做了 3 处冠词与时态修正" is a real service. Manufacturing changes to look busy erodes the author's ability to tell which of your edits matter.

## Expansion

Users ask to expand for two very different reasons, and confusing them produces useless output.

**Reason A — the logic has a gap.** A step is missing between claim and evidence, or motivation is unexplained. This is legitimately fixable: make the implicit reasoning explicit using only what the author already supplied.

**Reason B — they need to hit a length requirement.** Padding is not a service. Say so, and redirect: the honest ways to add length are more detail about the method, explicit limitations, added analysis of existing results, or clarified reasoning. Offer those. Adding empty subordinate clauses makes a paper worse and reviewers notice.

Execution:

1. Identify which gap type is present: background, motivation, mechanism ("why does this work"), implication, or transition.
2. Expand using only user-supplied content plus generic academic scaffolding.
3. Mark every added claim that needs evidence with a placeholder — `[请补充支持该结论的实验或引用]`.
4. Show clearly which sentences are new, so the author can check each one is true. Added sentences are all L3 by definition: they assert something the author did not write.

Never invent a motivation the author did not state. If you cannot tell why they made a design choice, ask — the real reason is almost always more specific and more persuasive than anything you would guess.

## Merging

1. Identify the shared claim; if there isn't one, merging is the wrong operation — say so.
2. Choose the strongest topic sentence and build around it.
3. Remove genuine repetition. Keep every distinct technical condition, even when it looks repetitive; conditions that seem redundant to a language model are often load-bearing to a specialist.
4. Preserve logical order: problem → approach → evidence → implication.
5. Report what was cut, so the author can veto. Cuts are the highest-risk part of merging, since deleted content leaves no trace to review.

## Compression to a limit

Abstract word limits, rebuttal character caps, highlight limits.

1. **Count first, against the venue's actual unit** — words, characters including spaces, or characters excluding spaces. Elsevier highlights are 85 characters *including spaces*; ICML rebuttal rounds are capped in characters. Getting the unit wrong wastes the whole exercise. `scripts/manuscript_audit.py --limit-words N` counts for you.
2. **Cut in this order**: empty intensifiers → nominalizations → redundant scaffolding (由于……因此) → repeated content → detail that appears elsewhere in the paper.
3. **Stop before scope conditions and hedges.** When only load-bearing language remains to cut, you have hit the floor. Report the shortfall and let the author decide what claim to drop; do not silently trade accuracy for length.
4. State the final count so the author can verify without recounting.

## Translation CN→EN

Translate the argument, not the string.

1. **Parse the logical structure first.** Chinese academic prose leans on 由于/因此/从而/进而 chains that map onto far fewer English connectives. A four-clause Chinese sentence is often two clean English sentences.
2. **Choose terminology deliberately.** Use the field's conventional English term, not a literal rendering. `terminology.md` has common pairs. When a term is ambiguous or the author's field uses a non-obvious convention, put it in the terminology table and let them override.
3. **Drop ceremonial framing.** 具有重要的理论意义和应用价值, 众所周知, 随着……的快速发展 are conventional in Chinese and read as padding or overclaim in English. Replace with the specific content, or cut. Flag as L3 — this surprises authors.
4. **Rebuild hedges to English norms.** Chinese hedging can be lighter; English academic writing hedges empirical claims more explicitly. Getting this right is the difference between a native-sounding paper and one that reads as overclaiming.
5. **Fix information order.** Chinese frequently front-loads conditions; English prefers subject-verb early with conditions following. Mechanical order-preservation is the main cause of "translationese."
6. Deliver: translation, terminology table, notes on any L3 decision.

**When the request is "润色成英文"** — Chinese source, English wanted — this workflow is the spine, but run Polishing's diagnostic step first. A structurally weak Chinese paragraph translated faithfully becomes a structurally weak English one; fixing the argument before translating is cheaper than fixing it after.

Report it as a translation. Skip the L1 aggregate line: the English is newly written rather than corrected, so a count of "article fixes" is meaningless. One line saying so is clearer than a fabricated number.

## Translation EN→CN

1. Preserve technical terms; use the established Chinese rendering rather than inventing one.
2. Match Chinese academic register — formal, no colloquial explanation unless asked.
3. Preserve hedges and scope conditions exactly. English hedging that gets dropped in Chinese translation produces an overclaim in the target text.
4. Keep symbols, equations, and citation markers in original form.
5. Provide a key-terminology table when the vocabulary is non-obvious.

## Abstract

The most-read and most-rejected part of a paper. Space is brutally scarce, so every sentence must earn its place.

Structure — roughly one to two sentences each:

1. Context and the problem, stated concretely
2. The gap: what existing approaches cannot do
3. What was done: the approach, named
4. Evidence: datasets, key results
5. What it means, scope-bounded

Rules:

- **No invented numbers, ever.** Missing results become `[请补充主要定量结果，如 Dice/mAP/准确率]`, and say plainly that this is a placeholder.
- No citations, unless the venue allows them.
- Define an abbreviation only if it is used again in the abstract; otherwise spell it out.
- Tense: past for what you did and found, present for what is generally true and what the paper reports.
- Check the venue's word limit and count against it.
- Cut every 众所周知 / "With the rapid development of…" opener. It costs 15 words and says nothing.

Verify with `scripts/structure_checker.py --section abstract`.

## Introduction

The logic chain that reviewers expect:

1. Broad importance — brief, one or two sentences, not a textbook review
2. The specific problem
3. What has been tried, and what remains unsolved — a gap, not a hit list
4. Your response to that gap
5. What you did, in summary
6. Contributions

Rules:

- The gap must connect to the contribution. If it does not, the introduction motivates a different paper than the one that follows — this is the single most common structural failure.
- Criticize prior work on specific technical grounds or not at all. Dismissive framing reads badly and reviewers are often the authors of the work being dismissed.
- 2–4 contributions. Each one a thing you *did*, not a property you claim.
- Avoid "first" / "novel" / "state-of-the-art" unless verified; see the fidelity protocol.

## Related work

The highest fabrication risk in the entire Skill. Load `citation-safety.md`.

Pick an organizing principle and hold it: by method family, by sub-problem, or by limitation addressed. Chronological order is right only when the history itself is the argument.

Without a reference list from the user, do **not** produce a draft with plausible-looking citations. Instead:

- Ask for the references, or
- Give the structure with explicit `[citation needed: 该类方法的代表工作]` slots

Both are useful. An invented bibliography is not merely useless — it is actively dangerous, because fabricated references survive into submissions when authors trust the output.

End with a transition to the gap, without attacking prior work.

## Method

1. Overview — the pipeline in a few sentences, so the reader has a map
2. Problem formulation, with notation defined at first use
3. Architecture or procedure
4. Components, in the order data flows through them
5. Objective function or optimization
6. Training and inference procedure
7. Complexity or implementation notes, if available

Rules:

- **Never invent equations, hyperparameters, or architectural details.** If the author writes "使用注意力机制" without specifics, the draft says that and flags the gap. Inventing "8-head self-attention with 64-dim keys" is fabrication that reads as competence.
- Reproducibility is the standard: could a competent reader reimplement this? Flag concretely what is missing.
- Symbols: introduce each once, use consistently, never reuse one symbol for two things. `scripts/manuscript_audit.py` flags first-use problems.
- Present tense for describing the method; past tense for what was done in experiments.

## Experiment

Structure: datasets → metrics → implementation details → baselines → main results → ablations → qualitative analysis → failure cases.

Rules:

- **No invented metric values, dataset sizes, or baseline numbers.** This is the most consequential fabrication risk after citations.
- Analyze only the numbers the author supplied. If they gave a table, describe what it shows; do not extrapolate a trend across cells you cannot see.
- "significant" means a statistical test was run. Without one, use "consistent," "notable," or just report the difference.
- Ablations should isolate one variable each; if the author's ablation confounds two, flag it — a reviewer will.
- Failure cases and limitations strengthen a paper. Authors under-report them; encourage the opposite.

## Discussion, limitations, future work

Where papers earn credibility. Hedging here is correct, not weak.

Cover: why the method behaves as observed; where it works, bounded by evidence; where it fails; limitations; what follows.

- Ground interpretation in the reported results, not in general plausibility.
- Limitations must be real. "Our method requires more computation" when computation was never measured is decoration, and reviewers read decoration as evasion.
- Future work should follow from a stated limitation.
- Distinguish what the evidence supports from what the authors believe. Both belong; conflating them does not.

## Title and contributions

**Titles** — produce 4–6 candidates across distinct strategies rather than six paraphrases:

- Descriptive: what the thing is
- Method-forward: names the technique
- Problem-forward: names what it solves
- Finding-forward: states the result, where venue norms allow
- Short and memorable

Then recommend one, with a reason tied to the venue. Note searchability: the terms someone would use to find this work should appear. Avoid unverifiable superlatives and question-form titles outside venues where they are common.

**Contribution statements** — each should name a thing done, be independently checkable, and be distinct from the others. Rewrite "we propose a novel and effective module" into what the module does and what evidence supports it. Three specific contributions beat five vague ones.

## Naturalization

Users ask for text that "reads less like a machine." Take the request seriously and reframe it accurately: you are improving writing quality, not targeting a detector. Detector scores are unreliable in both directions and optimizing against them is both futile and a bad use of the author's time.

What actually makes text read as machine-generated, and what to do:

- **Uniform sentence length.** Vary it. Short sentences after long ones create emphasis.
- **Even weighting.** Machine text treats every point as equally important. Real authors subordinate, foreground, and skip.
- **Vague universals.** "Various approaches have been proposed" says nothing. Name them or cut.
- **Hedge stacking.** "may potentially help to some extent" — pick one hedge.
- **Connective overuse.** Moreover/Furthermore/Additionally opening consecutive paragraphs.
- **No commitment.** Real papers argue for a position. Say which interpretation the authors favor.

Fixing these produces text that is both better and less formulaic — the goal the user actually has.

## Prompt optimization

Rewrite the user's academic-writing prompt so it specifies: task, field, target venue and register, language direction, section, what must be preserved verbatim, evidence available versus missing, desired output format, and integrity constraints.

Return the improved prompt plus a short note on what was missing and why it mattered — the point is to teach the pattern, not to hand over one better prompt.
