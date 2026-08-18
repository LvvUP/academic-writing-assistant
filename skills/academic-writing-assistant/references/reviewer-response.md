# Reviewer Response and Rebuttal

Two different documents that users conflate, with different length budgets, different readers, and different tone.

| | Journal response letter | Conference rebuttal |
|---|---|---|
| Venue | Elsevier, Springer, IEEE Trans, medical journals | ICLR, NeurIPS, ICML, CVPR, ACL |
| Length | Effectively unbounded; thoroughness is a virtue | Hard character or page cap, strictly enforced |
| Timing | Written *after* revisions are made | Written *before* revisions; you promise, then deliver |
| Reader | Editor + the original reviewers, reading carefully | Overloaded reviewers skimming during a short discussion window |
| Tense | "We have revised Section 3.2…" | "We will add…" / "We have run the requested experiment and obtained…" |
| Structure | Point-by-point, exhaustive, quotes each comment | Prioritized: the objections that actually move scores come first |

Getting this wrong is costly. A 6000-word point-by-point reply pasted into a conference rebuttal box will be truncated and unread. A terse conference-style rebuttal sent to a journal editor reads as dismissive.

Ask which one it is if it is not obvious from the venue.

## Contents

- [Before drafting](#before-drafting)
- [The response unit](#the-response-unit)
- [Journal response letter](#journal-response-letter)
- [Conference rebuttal](#conference-rebuttal)
- [Handling the hard cases](#handling-the-hard-cases)
- [Tone](#tone)
- [The claim boundary](#the-claim-boundary)
- [Templates](#templates)

## Before drafting

Establish three things. Guessing any of them produces a response that misrepresents the authors.

1. **What did the reviewer actually say?** Work from their words, not a paraphrase. If the user summarized ("审稿人说创新性不够"), ask for the verbatim comment — the specific wording usually reveals what would satisfy them.
2. **What has already been done?** This is the critical one. Whether an experiment has been run determines whether you write "we have added" or "we will add." Never assume. Claiming a completed revision that does not exist is a serious misrepresentation to an editor, and it is the easiest error to make when drafting speculatively.
3. **Do the authors agree?** Agreement, partial agreement, and principled disagreement produce structurally different responses. Do not default to total capitulation; conceding a point the authors believe is wrong weakens the paper and misleads the reviewer.

## The response unit

Every reply to a single point has the same four moves, whatever the venue:

1. **Restate the concern** in one line, in your own words. This proves you understood it and is the fastest way to build reviewer goodwill.
2. **Position**: agree / partially agree / respectfully clarify. Say which, explicitly.
3. **Action**: what changed or what is proposed, concretely. "We clarified the motivation" is empty. "We added a paragraph in Section 3.1 explaining why the gating is applied before rather than after normalization, and added Table 6 reporting the reversed order" is a real answer.
4. **Evidence**: quote the new text, cite the new table, or give the number. A response with no artifact behind it does not resolve anything.

Reviewers reading fifteen responses reward specificity and punish padding. Cut everything that is not one of these four moves.

## Journal response letter

Open with a brief note to the editor: thanks, a one-paragraph summary of the main changes, and a statement of how the manuscript improved. Then go point by point.

Formatting that editors find usable:

- Number every comment: R1.1, R1.2, R2.1
- Quote the comment verbatim, visually distinguished (italic or a quote block)
- Response immediately below
- New or changed manuscript text quoted directly, with section and line numbers
- Never make the editor hunt through the revised manuscript to find your change

Answer every comment, including the ones you disagree with and the ones that are trivial. Silent omission reads as evasion and is a common reason a revision goes back for another round.

## Conference rebuttal

Space is the binding constraint. Spend it where it changes scores.

1. **Triage.** Rank objections by how much they affect the outcome. A reviewer who thinks the method is fundamentally flawed matters more than one who wants an extra citation.
2. **Lead with the biggest.** Do not open with a thank-you paragraph — with hard caps, that is a wasted line.
3. **Group shared concerns.** "R1 and R3 both ask about generalization to unseen categories: …" saves space and shows the reviewers you read all the reviews.
4. **Numbers over prose.** A new result table is worth a paragraph of argument.
5. **Be explicit about what is promised versus done.** Reviewers discount promises heavily; if the experiment was actually run during the rebuttal period, say so unmistakably and give the numbers.
6. **Check the cap before submitting.** Major ML venues cap rebuttals by characters or pages and enforce it by truncation. Count against the venue's stated limit rather than estimating — `scripts/manuscript_audit.py --limit-words` handles counting.

Format for skimming: bold the concern, plain text for the answer, one blank line between points.

## Handling the hard cases

**"The novelty is unclear."** Usually means the paper failed to *position* the work, not that the work is unoriginal. Answer with the specific technical difference from the closest prior method and the evidence that the difference matters — ideally an ablation. Do not restate the contributions list more emphatically; that is what the reviewer already read and did not find convincing.

**A request for an experiment the authors cannot run.** Say so plainly, give the actual reason (no access to the dataset, no compute, requires an ethics amendment), and offer the closest feasible substitute. Reviewers accept honest constraints far more often than they accept evasion. Never imply the experiment was run.

**The reviewer misunderstood the paper.** A misunderstanding is evidence the writing was unclear — even when the reviewer was careless. Clarify without saying "as clearly stated in Section 3," which is a reliable way to antagonize a reviewer. Instead: "We may not have made this sufficiently clear. Section 3.2 has been revised to state explicitly that…"

**A factually wrong criticism.** Correct it with evidence, once, neutrally. State the fact, cite the location, move on. No accumulation of counter-arguments; no invitation to a debate.

**A hostile or dismissive review.** Respond to the technical content and ignore the tone completely. Never mirror it. If a review is genuinely unprofessional, the mechanism is a private note to the editor or AC, not the public response — mention that option to the user rather than putting it in the letter.

**Contradictory reviewer requests.** Name the conflict openly and explain the choice: "R1 asks for a broader evaluation while R2 asks for deeper analysis of the existing setting. Given the page limit we prioritized R2's request and added the broader comparison to Appendix C."

## Tone

Polite, specific, confident. Not obsequious, not defensive.

- One brief thanks per reviewer. Not per comment — repeated gratitude reads as padding and is noticed.
- No apology for the paper's existence. "We apologize for the poor quality of our work" hurts the authors and is not what the reviewer wants.
- No over-conceding. Authors are entitled to defend correct choices; a well-argued disagreement is respected.
- Avoid "obviously," "clearly," "as we already stated" — all of them imply the reviewer was inattentive.
- Keep an even register. The response is a professional document, and the editor reads it too.

## The claim boundary

The fidelity rules apply here with unusual force, because a response letter is a factual representation to an editor.

Never write, unless the user has confirmed it:

- That an experiment was run, or what it showed
- That text was added, or where
- A metric, dataset, or result value
- That a reviewer's suggestion was adopted

When the user has not said, produce the response with explicit slots — `[请填入新实验结果]`, `[请填写修改后的章节号与行号]` — and say clearly that these must be filled before sending. Placeholders that survive into a submitted letter are embarrassing; invented numbers are misconduct. The placeholder is the safe failure mode, so make it visually obvious.

Some venues also require disclosing AI assistance used in preparing responses. See `submission-package.md`.

## Templates

### Journal, per comment

```text
**Comment R1.2:** [verbatim reviewer text]

**Response:** We thank the reviewer for this point. We agree that [restated concern].
[What was done, concretely.] The revised text now reads:

> "[new manuscript text]"

This appears in Section [X], page [X], lines [X–X].
```

### Journal, Chinese

```text
**审稿意见 R1.2：** [审稿人原文]

**回复：** 感谢审稿人指出这一问题。我们认同 [重述关切]。
针对该意见，我们 [具体修改内容]。修改后的表述为：

> "[修改后正文]"

修改位置：第 [X] 节，第 [X] 页，第 [X–X] 行。
```

### Conference rebuttal, per point

```text
**Generalization to unseen categories (R1, R3).** We ran this during the rebuttal
period. On [dataset], the method reaches [metric] on held-out categories versus
[metric] for [baseline]; full results are in the table below. We will add this as
Table 6 in the camera-ready.
```

### Respectful disagreement

```text
**Response:** We appreciate this perspective and would like to offer a clarification.
[Reviewer's premise] holds under [condition], but our setting differs in that
[specific technical reason, with evidence]. We have added a sentence to Section [X]
making this assumption explicit, since the reviewer's reading suggests it was not
sufficiently clear in the original submission.
```
