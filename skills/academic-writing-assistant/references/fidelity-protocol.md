# Fidelity Protocol

Worked guidance for the hardest judgment in academic editing: how far you may move a sentence before you have changed what the author is claiming.

Read this when a revision touches claim strength, when you are unsure whether an edit is L2 or L3, or when a user pushes back on a change you made.

## Contents

- [Why fidelity is the whole game](#why-fidelity-is-the-whole-game)
- [Zone 1: locked](#zone-1-locked)
- [Derived numbers](#derived-numbers)
- [Bounding an overclaim](#bounding-an-overclaim-three-options-not-one)
- [Zone 2: load-bearing language](#zone-2-load-bearing-language)
- [Zone 3: free surface](#zone-3-free-surface)
- [Worked examples](#worked-examples)
- [Edge cases](#edge-cases)
- [Reporting](#reporting)

## Why fidelity is the whole game

An author sends a rough paragraph and gets back polished English. The English is better than anything they would have written. So they accept it — all of it, without line-by-line comparison, because comparing is slow and the output looks authoritative.

That trust is the product. It is also the risk. Every unflagged strengthening rides along on it into a submitted manuscript, where it becomes the author's word and the author's responsibility. A reviewer who spots "significantly outperforms" with no significance test does not blame the tool.

So the goal is not to be conservative for its own sake. Timid edits that leave bad writing intact fail the author just as surely. The goal is to be **aggressive on the surface and rigorous about the boundary** — and to make the boundary cheap for the author to inspect.

## Zone 1: locked

Reproduce character-for-character. Never paraphrase, reformat, round, convert, or "clean up."

- Numerals, percentages, units, tolerances, confidence intervals, p-values
- Dataset, benchmark, corpus, and cohort names — including capitalization (`ImageNet`, not `Imagenet`)
- Method, model, architecture, and software names, with versions
- Citation markers: `[12]`, `(Zhang et al., 2021)`, `\cite{zhang2021}`, `\citep{}`
- Equations, inline math, symbols, subscripts, superscripts
- Cross-references: `Section 3.2`, `Table 4`, `Fig. 5`, `\ref{}`, `\label{}`
- Hyperparameters, seeds, hardware, runtimes
- Ethics approval numbers, registration IDs, accession numbers, funding numbers

### When a locked item looks wrong

Flag; do not fix. Examples of things that must become queries rather than edits:

- The text says 92.3% but the referenced table says 93.2%
- A symbol appears before its definition
- "three datasets" is followed by four dataset names
- A citation year contradicts a claim about chronology

You do not have the data, the tables, or the bibliography. The author does. Write:

> **需确认**：正文第 2 段为 92.3%，与 Table 4 的 93.2% 不一致。已保留原文数值未作修改，请核对以哪个为准。

The cost of flagging a real error is thirty seconds of author attention. The cost of silently harmonizing two numbers to the wrong one is a corrected-in-proof or a retraction. These are not comparable.

### One exception: mechanical formatting the author asked for

If the user explicitly requests a formatting normalization — "统一成 Table 1 而不是 table 1", "把百分号统一" — apply it, and confirm what was normalized. The rule protects against *unrequested* alteration.

### Derived numbers

A number you calculate from two locked values — 91.2 − 89.8 = 1.4 — is neither supplied by the author nor invented. It comes up constantly: improvement margins, relative gains, parameter reductions, speedups.

The rule: **offer it, never insert it.** Put the derived value in the ledger or the queries as a suggestion, not in the manuscript-ready text.

The reason is that the arithmetic is trivially right and the *interpretation* is where it goes wrong. A 1.4-point difference is only "a 1.4-point improvement" if both numbers come from the same evaluation protocol, the same split, and the same metric definition — which you cannot verify. Relative percentages are worse: "a 1.6% relative gain" versus "1.4 points absolute" are both true and mean different things to a reader, and picking one for the author makes a rhetorical choice on their behalf.

> **需确认**：91.2% 与 89.8% 相差 1.4 个百分点。如果两者是同一评测协议下的结果，
> 建议写成 "a 1.4-point F1 gain over the baseline"，比"提高很多"有说服力得多。
> 请确认口径后再写入。

Once the author confirms, use it freely — it is then their number.

### Bounding an overclaim: three options, not one

"Soften toward accuracy" is underspecified. When a sentence claims more than the evidence supports, there are three legitimate moves, and they are not interchangeable:

**Add a scope condition.** "可广泛应用于各种遥感场景" → "may generalize to other change-detection scenarios, although this would require confirmation across sensors, regions, and acquisition periods." Right when the author plainly believes the claim and the limits are conventional for the field.

**Cut the sentence.** The same sentence, deleted. Right when it adds no information — and unbounded applicability claims usually do not. Removing one costs the paper nothing and removes an attack surface.

**Leave a placeholder.** "The method is expected to generalize to `[请补充你能支持的适用范围]`." Right when only the author knows the real boundary.

The trap in the first option: the limits you add come from your field knowledge, not the author's text. Writing "across sensors, regions, and acquisition periods" asserts a specific limitation profile the author never stated. It moves in the safe direction, but it is still content you introduced.

So when you soften by adding scope, mark it L3, say where the limitation came from, and **offer deletion as the alternative**. Let the author choose between conceding a specific limitation and simply not making the claim.

## Zone 2: load-bearing language

These words determine what the paper asserts. They look like style; they are not.

### Hedges and evidential strength

Ordered from weakest to strongest:

`may / might` < `can` < `suggests / indicates` < `shows / demonstrates` < `establishes / proves`

Chinese equivalents: `可能` < `能够` < `表明 / 说明` < `证明` < `充分证明`

**Never move rightward on your own.** Moving leftward (toward caution) is permitted and often correct, but still disclose it — an author who deliberately wrote "demonstrates" after checking their statistics deserves to know you softened it, and may want it back.

`prove` deserves special attention with Chinese-native authors, because 证明 covers both mathematical proof and empirical support. In English, "prove" claims deductive certainty. An experiment does not prove; it demonstrates, indicates, or provides evidence for. Flag every 证明 → prove translation.

### Quantifiers and coverage

`all` / `every` / `always` / `universally` are absolute claims. `most` / `many` / `several` / `some` are not. Never inflate; never quietly deflate a defensible absolute either (a mathematical result may legitimately hold for all inputs).

Watch the implicit universal in translation: 该方法能够提升检测性能 has no explicit scope and may become an unbounded "The method improves detection performance." Add the scope the evidence supports, and mark it L3.

### Scope conditions

Phrases like "on the evaluated datasets," "in this cohort," "under the stated assumptions," "for images above 512×512," "在所测试的场景下" are the difference between a defensible claim and an overclaim. They are also the first thing that gets cut when someone tightens a sentence for concision.

Treat every scope condition as load-bearing. If you must cut one for length, say so explicitly and offer the shorter form as an option rather than a default.

### Causal language

`causes` / `leads to` / `results in` assert causation. `is associated with` / `correlates with` / `is accompanied by` do not. Chinese 导致 is frequently used loosely where the evidence supports only correlation — this is one of the most common overclaims to reach English drafts from Chinese sources, and reviewers in medicine, epidemiology, and the social sciences attack it reliably.

Unless the design is experimental with controls, prefer associational language and flag the change.

### Novelty and comparison

`first` / `novel` / `state-of-the-art` / `outperforms` / `superior` are checkable claims that reviewers do check.

- "first" — nearly indefensible; a single missed 2019 paper sinks it. Suggest "to our knowledge, the first" at minimum, and flag it.
- "state-of-the-art" — means "as of a specific comparison set on a specific benchmark." Bind it to that set or drop it.
- "outperforms" — needs a named baseline and a named metric. Unqualified, it is an invitation to a reviewer question.
- "significantly" — in a paper, this reads as a statistical claim. If no test was run, it is wrong, not merely strong. This is worth flagging every single time; it is the single most common unearned word in Chinese-authored English manuscripts.

### Negation, conditionals, and comparatives

Easy to drop, and reversing in meaning when dropped: `not`, `unless`, `except`, `only`, `at most`, `no worse than`, `fails to`, `除非`, `仅`, `并非`. Re-read any sentence containing these after rewriting it.

## Zone 3: free surface

Edit confidently. This is where the value is, and hesitation here produces stilted, half-improved prose that helps nobody.

- Grammar, agreement, articles, prepositions, plurals
- Tense (subject to section conventions — see `style-guide-en.md`)
- Sentence splitting and combining, when the claim is untouched
- Connectives and transitions that make existing logic explicit
- Cutting redundancy, filler, and empty intensifiers with no evidential role
- Reordering within a sentence for end-weight and emphasis
- Replacing vague verbs with precise ones of the same strength: `get better features` → `learn more discriminative features`
- Terminology normalization toward the author's dominant usage

The last one is worth stressing. When a draft mixes 目标检测 and 对象检测, or "feature fusion" and "feature merging," pick the author's more frequent variant and normalize to it, rather than imposing your preference. Consistency is the goal; the specific choice is usually the author's to make. Note the normalization as L2.

## Worked examples

### Example 1 — the classic overclaim

**Original:** 实验表明我们的方法明显优于现有方法，证明了该模块的有效性。

**Bad revision (L3 applied silently):**
> Experiments demonstrate that our method significantly outperforms existing methods, proving the effectiveness of the proposed module.

Three unearned upgrades in one sentence: `significantly` implies a test that was never mentioned; `outperforms existing methods` is unbounded; `proving` claims deductive certainty from empirical results. All three look like faithful translation. None are.

**Good revision:**
> Experiments show that the proposed method outperforms the compared baselines on the evaluated datasets, supporting the effectiveness of the proposed module.

**Ledger entry:**

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | 明显优于现有方法 | outperforms the compared baselines on the evaluated datasets | L3 | "明显/significantly" 在英文论文中读作统计显著性主张；未见检验，故改为受限比较。若已做显著性检验，请告知检验方法与 p 值，可改回 significantly |
| 2 | 证明了 | supporting | L3 | prove 在英文中意味演绎证明；实验结果宜用 support/demonstrate |

**需确认**：`existing methods` 具体指哪些 baseline？写明对比方法名称会显著降低审稿人质疑"与谁比较"的概率。

Notice the ledger explains what the author gains from each change and how to reverse it. That is what makes it actionable instead of merely defensive.

### Example 2 — an edit that should not have been made

**Original:** The model achieves 89.2% Dice on the internal validation set, though performance drops to 81.4% on the external cohort.

**Bad revision:**
> The model achieves 89.2% Dice on the validation set, with strong performance maintained across cohorts.

The revision deleted a number, dropped the internal/external distinction, and inverted the author's honest concession into a positive claim. In medical imaging, external-cohort degradation is the most important sentence in the paragraph — it is precisely what reviewers look for as evidence of methodological honesty. "Improving" it destroys the paper's credibility.

**Correct handling:** the sentence is already well-formed. Leave it. If anything, `though` → `whereas` for register. L1, aggregate line, no ledger entry.

The lesson: not every sentence needs improvement, and the confidence to leave good writing alone is part of the skill.

### Example 3 — legitimate aggressive editing

**Original:** 由于在实际应用场景中往往存在着大量的噪声干扰的问题，因此使得现有的方法在进行处理的时候会不可避免地受到一定程度的影响，从而导致最终的性能表现有所下降。

**Revision:**
> Noise in real-world settings degrades the performance of existing methods.

This cut roughly 70% of the characters and is entirely faithful. Chinese academic drafts frequently carry 由于……因此……从而…… scaffolding, nominalizations (进行处理), and hedge stacking (往往、一定程度、有所) that add length without adding content. Stripping them is the highest-value edit available and requires no permission — the claim, its scope, and its strength are unchanged.

Report as L2 with a one-line reason: "压缩冗余虚词与名词化结构，语义未变."

Do not overcorrect into telegraphic prose, though. `有所下降` → `degrades` is right; deleting a genuine hedge like 在部分场景下 is not.

### Example 4 — a query instead of an edit

**Original:** Our approach reduces annotation cost by 60% compared to full supervision.

There is nothing to fix linguistically. But 60% invites a question: reduced relative to what annotation protocol, measured how — pixels, images, hours? If the paper does not say, a reviewer will ask.

This is not a fidelity issue; it is an anticipatory review comment. Put it under 需确认, not in the ledger:

> **需确认**：60% 的标注成本下降是按标注像素、图像数量还是标注时长计算？审稿人通常会追问该口径，建议在方法或实验部分说明。

Offering these is one of the most valuable things this Skill does — it catches the reviewer comment before the reviewer does. Keep them separate from the edits so they do not dilute the change ledger.

## Edge cases

**The author explicitly wants a stronger claim.** They may have evidence you cannot see. Comply, but state the dependency once: "已按要求改为 significantly outperforms — 请确认稿件中报告了对应的显著性检验." Then drop it. Repeating a warning after the author has made an informed decision is condescending, not careful.

**The source text is internally contradictory.** Do not pick a side. Present both readings and ask which is intended. Choosing silently means half the time you have written something the author did not mean, with no signal that it happened.

**Translating a claim that is idiomatic in one language and an overclaim in the other.** 具有重要的理论意义和应用价值 is standard Chinese framing and largely ceremonial; "has important theoretical significance and application value" reads in English as an unsupported grand claim. Translate the function, not the words: name the specific contribution, or cut it. Mark L3 and explain — the author usually did not realize the phrase does not transfer.

**A section that is entirely fabrication risk**, such as a related-work request with no references supplied. Do not produce a plausible-looking draft with invented citations. Give the structure with explicit `[citation needed]` slots, or ask for the reference list. See `citation-safety.md`.

**Very short input.** One sentence, obvious fix. Skip the ledger and the queries; return the fixed sentence and a clause of explanation. Ceremony scaled to a trivial task wastes the author's attention and trains them to ignore the format when it matters.

## Reporting

The ledger exists so the author can audit in one minute instead of ten. It fails if it is too long to read.

- Quote fragments, not sentences. The changed span plus minimal context.
- One line of reasoning per entry, written for the author's benefit — what problem the change avoids — not as a justification of your authority.
- L1 in a single aggregate count. Nobody reads "added article before 'proposed method'" forty times.
- In translation, the L1 count does not apply -- the target text is newly written, not corrected. Say so in one line rather than inventing a number.
- Every L3 needs either explicit reasoning or a query. No silent claim edits, ever.
- If nothing needed confirming, write 暂无. An empty section is information; a missing section looks like an oversight.

When `scripts/fidelity_check.py` has been run, cite its result rather than asserting preservation from memory: "fidelity_check 显示 14 处引用、9 个数值、3 个公式全部保留." Evidence beats reassurance, and the author can re-run it themselves.
