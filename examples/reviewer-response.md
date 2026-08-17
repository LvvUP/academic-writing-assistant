# 审稿回复示例：期刊 vs 会议

## Task

Reviewer Response Drafting

## 两种文体的区别

| | 期刊 response letter | 会议 rebuttal |
|---|---|---|
| 篇幅 | 基本不受限，详尽是优点 | 严格字符或页数上限 |
| 时机 | 修改**之后**写 | 修改**之前**写，先承诺后兑现 |
| 时态 | "We have revised Section 3.2…" | "We will add…" / "We ran this during the rebuttal period…" |
| 结构 | 逐条回应，完整覆盖 | 按影响评分的程度排序 |

弄错代价很高：把 6000 字逐条回复粘进会议 rebuttal 框会被截断，把会议式简短回复
发给期刊编辑会显得敷衍。

## 示例一：期刊，创新性质疑

### User Input

```text
Reviewer: The novelty of the proposed method is unclear.
我们已经在修订稿的 3.1 节加了一段说明，并新增了 Table 6。
```

### Expected Output

```markdown
**Comment R1.1:** The novelty of the proposed method is unclear.

**Response:** We thank the reviewer for this comment. We agree that the
distinction between our design and existing approaches was not stated
explicitly enough. The key difference is that [请填写与最接近的现有方法的具体技术差异],
which we have now made explicit. We have also added Table 6 reporting
[请填写该消融实验验证的内容], which isolates the contribution of this design choice.

**Revision:** Section 3.1, page [X], lines [X–X] now reads:

> "[请粘贴修订后的正文]"

## 需填写

- 与最接近的现有方法的具体技术差异
- Table 6 验证的内容
- 修订后的章节页码与行号
```

注意：回复中说"已修改"是因为**用户明确说明已经修改**。用户未确认时，
应写成 "we propose to revise"，并说明这一区别。

## 示例二：会议 rebuttal，提升幅度质疑

### User Input

```text
ICLR 审稿人：The improvement over baselines is marginal and may be within noise.
我们跑了 5 个种子，均值提升 2.1 个点，标准差 0.3。
```

### Expected Output

```markdown
**Marginal improvement / noise (R2).** We report results over 5 seeds: the
proposed method improves by 2.1 points on average (std 0.3), while the
baseline's own seed variance is [请填写 baseline 标准差]. The gap therefore
exceeds run-to-run variation by a substantial margin. We will add per-seed
results and variance to Table 2 in the revision.

## 说明

- 直接使用作者提供的数据，未添加任何未提供的数值。
- 建议补充 baseline 的种子方差——这是回应"是否在噪声范围内"最直接的证据；
  只报告自己方法的方差无法完整回答该质疑。
- 若做了配对显著性检验，加上检验方法与 p 值会更有力；没做则不要写
  significantly。
```
