# Output Templates

Shapes, not scripts. The purpose is that an author can find the deliverable instantly and audit the changes in about a minute. Adapt freely — a template that fights the task should lose.

Two rules hold across all of them: **manuscript-ready text comes first**, and **L3 changes are never silent**.

## Contents

- [Revision](#revision)
- [Translation](#translation)
- [Section draft](#section-draft)
- [Compression](#compression)
- [Reviewer response](#reviewer-response)
- [Title candidates](#title-candidates)
- [Consistency report](#consistency-report)
- [Terminology check](#terminology-check)
- [Cover letter and submission materials](#cover-letter-and-submission-materials)
- [Prompt optimization](#prompt-optimization)
- [Scaling down](#scaling-down)

## Revision

For polishing, expansion, merging, and general editing.

```text
## 修改后文本

[clean, paste-ready text — no inline markup, no commentary]

## 改动台账

L1（语法/冠词/时态/拼写）：共 N 处，未逐条列出。

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | [fragment] | [fragment] | L2 | [one line] |
| 2 | [fragment] | [fragment] | L3 | [one line, and how to revert] |

## 需确认

- [what only the author can resolve]
- （无则写"暂无"）
```

If every change is L1 and the text is short, collapse to the revised text plus one line: "仅作语法与冠词修正（7 处），未改动任何主张。"

## Translation

```text
## English Translation

[translation]

## 术语选择

| 中文 | English | 说明 |
|---|---|---|
| [term] | [term] | [why this rendering] |

## 翻译说明

- [L3 decisions: dropped ceremonial framing, adjusted hedging, restructured order]

## 需确认

- [ambiguity in the source, or terms the author should confirm against their field]
```

Reverse the language of the headings for EN→CN.

### The compound case: Chinese in, polished English out

The most frequent request, and it sits between the Revision and Translation shapes. Use the Translation shape as the base and add the change ledger for claim-level decisions, since those are what the author most needs to check:

```text
## English Translation

[translation]

## 改动台账

（中译英，原文为中文，不计 L1 语法修正）

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | [中文片段] | [English fragment] | L3 | [why] |

## 术语选择

| 中文 | English | 说明 |
|---|---|---|

## 需确认

- ...
```

## Section draft

For abstract, introduction, method, experiment, discussion.

```text
## [Section] Draft

[draft, with placeholders visible: [请补充主要定量结果]]

## 写作逻辑

- [how the draft is organized and why — helps the author adapt it]

## 缺失信息

- [每个占位符对应什么，以及为什么需要]
```

Placeholders must be impossible to miss. Bracketed Chinese instructions work well because they cannot be mistaken for manuscript text.

## Compression

```text
## 压缩后文本（[N] 词 / 限制 [M] 词）

[text]

## 删减内容

- [what was cut, grouped by type]

## 保留说明

- [scope conditions and hedges kept, and why they were not candidates for cutting]
```

Always state the count. If the limit could not be met without cutting load-bearing language, say so and let the author choose.

## Reviewer response

Follows `reviewer-response.md`. Journal:

```text
## 回复信

[editor paragraph]

### R1.1
**Comment:** [verbatim]
**Response:** [answer]
**Revision:** [quoted new text, Section X, lines X–X]

### R1.2
...

## 需填写

- [every slot the user must complete before sending]
```

Conference rebuttal is denser and ordered by impact — no per-comment ceremony.

## Title candidates

```text
## 标题候选

1. **[descriptive]** — [strategy, one line]
2. **[method-forward]** — [...]
3. **[problem-forward]** — [...]
4. **[concise]** — [...]

## 推荐

[choice] — [reason tied to venue and searchability]

## 说明

- [any claim-strength note, e.g. why "first" was avoided]
```

## Consistency report

Grouped by category, claim inconsistencies first. Format in `consistency-pass.md`.

## Terminology check

```text
## 建议统一

| 出现的变体 | 建议统一为 | 出现位置 | 说明 |
|---|---|---|---|
| A（7 次）/ B（2 次） | A | 3.2 节、4.1 节 | [why] |

## 需作者决定

- [cases where both variants are defensible and it is the author's call]
```

## Cover letter and submission materials

Return the document ready to send, with clearly marked slots for anything only the author knows (editor name, ethics numbers, prior submission history). Follow with a short list of what must be filled and what to verify against the venue's guide. See `submission-package.md`.

## Prompt optimization

```text
## 优化后 Prompt

[the improved prompt]

## 补充了什么

- [what was missing and why it changed the output]
```

## Scaling down

Ceremony should match the size of the task. A one-sentence fix returns the fixed sentence and a clause of explanation — not a table with one row and an empty "需确认" section.

When the user asks for just the text, give just the text. The contract exists to serve the author's ability to check the work; when they have explicitly said they do not need to check it, honoring that is the correct response.
