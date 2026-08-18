# Consistency Pass

Paragraph-level editing cannot catch the errors that live across a whole manuscript. These are the ones reviewers notice immediately — they read as carelessness and prime a reviewer to look for other carelessness.

Run this pass when a user shares a full section, a full paper, or asks for a "全文检查."

## Contents

- [Terminology](#terminology)
- [Abbreviations](#abbreviations)
- [Symbols and notation](#symbols-and-notation)
- [Tense](#tense)
- [Numbers and units](#numbers-and-units)
- [Naming the work](#naming-the-work)
- [Cross-references and structure](#cross-references-and-structure)
- [Claim consistency](#claim-consistency)
- [Reporting](#reporting)

## Terminology

One concept, one term, throughout. A paper that alternates between "feature fusion" and "feature aggregation" for the same module makes the reader wonder whether they are two things.

Method:

1. Identify each technical concept that appears more than once.
2. Find every surface form used for it.
3. Normalize to the author's **dominant** variant, not your preferred one — unless the dominant one is wrong for the field, in which case say why.
4. Watch for the reverse error too: the same word used for two different things. That one is more damaging and harder to spot.

Chinese drafts: `scripts/terminology_checker.py` covers common variant pairs (目标检测/对象检测, 鲁棒性/稳健性, 遥感图像/遥感影像). See `terminology.md` for CN↔EN selection.

Note the legitimate exception: some papers deliberately distinguish two nearby terms. Check whether the draft defines them separately before normalizing.

## Abbreviations

Rules that hold nearly everywhere:

- Define at first use in the main text: "convolutional neural network (CNN)." Then use the abbreviation consistently — do not alternate.
- The abstract is a separate scope. An abbreviation defined there must be defined again at first use in the body.
- Do not define an abbreviation used only once. Spell it out; the abbreviation costs the reader more than it saves.
- Extremely standard field abbreviations (CNN in a vision paper, DNA in biology) may not need expansion — venue-dependent.
- Never define the same abbreviation twice, and never use one abbreviation for two expansions.

`scripts/manuscript_audit.py` flags abbreviations used before their definition and definitions that never get used — both common in drafts assembled from multiple sections.

## Symbols and notation

Especially important in method-heavy papers.

- Every symbol defined once, at first use
- One symbol, one meaning, for the whole paper
- Consistent typographic convention: vectors bold, matrices capitalized, scalars italic — whatever the author chose, applied uniformly
- Subscript conventions consistent (`x_i` for sample index throughout, not sometimes for feature index)
- Symbols in figures and tables match the text

Report inconsistencies; do not silently rename. Renaming a symbol requires editing every equation, and equations are locked-zone content.

## Tense

The conventional pattern in English scientific writing:

| Where | Tense | Example |
|---|---|---|
| Established knowledge | Present | "Attention mechanisms improve long-range modeling." |
| Prior specific work | Past or present perfect | "Zhang et al. proposed…" / "Recent work has shown…" |
| Describing your method | Present | "The encoder extracts multi-scale features." |
| What you did experimentally | Past | "We trained the model for 100 epochs." |
| What you found | Past | "The method achieved 89.2% Dice." |
| What tables and figures show | Present | "Table 2 reports…" / "As shown in Fig. 3…" |
| Interpretation | Present | "These results suggest…" |
| Limitations and future work | Present / future | "The method does not handle… We plan to…" |

Mixed tense inside a single paragraph is the most frequent tense error, and it is genuinely disorienting — the reader cannot tell whether a sentence describes the method or one experimental run.

Chinese has no tense inflection, so this is a systematic difficulty for Chinese-native authors rather than carelessness. Fix it as L1 and, if the pattern repeats, name it once so the author can apply the rule themselves.

## Numbers and units

- Decimal places consistent per metric: 89.2 and 91.47 in the same column is a formatting error
- Same rounding convention in text and tables, and matching values across both
- Space between number and unit (`10 ms`), except for percent and degree per most style guides
- One unit system throughout
- Consistent thousands separators
- Number-at-sentence-start spelled out, or the sentence rewritten

Text-versus-table mismatches are locked-zone: flag, never harmonize. You cannot know which one is right.

## Naming the work

Pick one and hold it: "the proposed method," "our method," or the method's actual name. Drifting between all three within a section reads as sloppiness, and in double-blind submissions "our" versus a named method can carry anonymity implications.

If the method has a name, use the name — it is more memorable and gets cited more.

Check venue conventions on first person. "We propose" is standard in most CS and many science venues; some journals still prefer impersonal constructions. Do not impose a preference the venue does not have.

## Cross-references and structure

- Every `\ref` has a `\label`, and vice versa
- Tables and figures are referenced in the text, in order
- Section numbering claims in the text match reality ("as described in Section 3.2")
- Promised content exists: "we discuss this in Section 5" must have a Section 5 that discusses it
- Appendix references resolve

The forward-promise failure is common in papers restructured late. Worth checking specifically.

## Claim consistency

The subtlest category, and the one reviewers punish hardest: the same result described with different strength in different places.

Typical pattern — the abstract says "significantly outperforms existing methods," the experiment section says "achieves comparable performance to X while improving on Y," and the conclusion says "consistently improves." These are three different claims about one result.

The abstract and conclusion drift upward because they are written last, compressed, and under pressure to sound conclusive. Check that:

- The abstract's claim strength matches the results section
- The conclusion does not exceed the discussion
- Contributions in the introduction correspond to actual content
- Limitations acknowledged in the discussion are not contradicted by an unhedged abstract

Flag every mismatch with all locations quoted, and recommend aligning to the **weakest** version that the evidence supports — that is the one the results section can defend.

## Reporting

Group findings by category, not by line number. An author fixing terminology wants all terminology issues together.

```text
## 全文一致性检查

### 术语（3 处）
- "feature fusion"（7 次）/ "feature aggregation"（2 次）指同一模块 → 建议统一为 feature fusion
  位置：3.2 节第 2 段、4.1 节第 1 段

### 缩写（2 处）
- MSFF 在 4.1 节首次出现时未定义，定义出现在 4.3 节 → 建议移至首次出现处
- SOTA 全文仅出现 1 次 → 建议展开为完整表述

### 时态（1 类模式）
- 3.3 节存在方法描述（现在时）与实验操作（过去时）混用，共 6 处

### 主张一致性（1 处，建议优先处理）
- 摘要："significantly outperforms existing methods"
- 4.2 节："achieves comparable performance on DatasetA and improves on DatasetB"
- 建议：摘要向 4.2 节的表述对齐；当前摘要强度高于实验部分可支持的范围，
  且未见显著性检验
```

Lead with claim inconsistencies. Terminology is cosmetic; a claim mismatch between the abstract and the results is what gets a paper rejected.
