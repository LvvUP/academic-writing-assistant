# Examples

End-to-end worked examples. The point is not the specific text but the shape: where the deliverable goes, how the ledger reads, and what belongs in a query rather than an edit.

All content below is invented for illustration — no real papers, datasets, or results.

## Contents

- [Polishing with claim softening](#polishing-with-claim-softening)
- [CN→EN translation](#cnen-translation)
- [Abstract with no results yet](#abstract-with-no-results-yet)
- [Related work with no references](#related-work-with-no-references)
- [Conference rebuttal](#conference-rebuttal)
- [LaTeX editing](#latex-editing)
- [Redirecting a detection-evasion request](#redirecting-a-detection-evasion-request)
- [A short task that needs no ceremony](#a-short-task-that-needs-no-ceremony)

## Polishing with claim softening

**User:** 我做医学影像分割的，帮我润色成 SCI 风格：我们的方法能减少标注困难的问题，分割结果比较好，对小病灶也有帮助，明显优于现有方法。

**Response:**

```text
## 修改后文本

The proposed method reduces the annotation burden in medical image segmentation
and improves the delineation of small lesions compared with the evaluated
baselines. [请补充具体数据集、指标与数值]

## 改动台账

L1（语法/冠词/时态）：共 4 处，未逐条列出。

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | 分割结果比较好 | improves the delineation ... compared with the evaluated baselines | L3 | "比较好"无对照对象；英文论文需指明与谁比较，否则审稿人必然追问 |
| 2 | 明显优于现有方法 | compared with the evaluated baselines | L3 | "明显/significantly" 在英文中读作统计显著性主张。若已做显著性检验，告诉我检验方法与 p 值，可改回 significantly outperforms |

## 需确认

- 使用了哪些数据集、哪些评价指标（Dice / IoU / HD95）？没有这些数值，性能表述只能停留在定性层面。
- "现有方法"具体指哪些 baseline？写明方法名称能显著降低审稿人质疑对比公平性的概率。
- 标注负担的降低是否有量化（标注时长、标注像素量、所需标注样本数）？医学影像审稿人通常会追问这一口径。
```

Note that the response did not invent a Dice score to make the sentence complete, and the two L3 entries each tell the author how to reverse the change.

## CN→EN translation

**User:** 翻译成 SCI 英文，给术语表：针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法，具有重要的理论意义和应用价值。

**Response:**

```text
## English Translation

To address the large scale variation and complex backgrounds in remote sensing
images, this study proposes a multi-scale feature fusion method.

## 术语选择

| 中文 | English | 说明 |
|---|---|---|
| 遥感图像 | remote sensing images | 遥感领域标准表述 |
| 目标尺度变化 | scale variation | 比 "target scale change" 更符合领域惯例 |
| 多尺度特征融合 | multi-scale feature fusion | 视觉与遥感论文通用；不用 feature merging |

## 翻译说明

- 删除了"具有重要的理论意义和应用价值"（L3）。这类表述在中文论文中是惯例性收尾，
  但直译成 "has important theoretical significance and application value" 在英文中
  会被读作缺乏支撑的宏大主张，审稿人对此较敏感。如果希望保留这层意思，建议改为
  具体陈述，例如该方法可用于哪类实际任务——需要你补充。
- 保留了"针对……问题"的问题-方法逻辑结构，未改变主张强度。

## 需确认

- 尺度变化针对的目标类型（车辆、建筑、船舶等）？具体化能提升摘要与标题的检索性。
```

The dropped ceremonial phrase is disclosed as L3, with an explanation of why it does not transfer — most authors do not know this and it is the most useful thing in the response.

## Abstract with no results yet

**User:** 我方法部分写完了但实验还没跑完，能先写摘要吗？[方法描述]

**Response:** Write the abstract with the results sentence as a visible placeholder:

```text
## Abstract Draft

... Experiments on [请填写数据集名称] show that the proposed method achieves
[请填写主要指标与数值，例如 Dice 0.XX / mAP XX.X] compared with [请填写对比方法].
...

## 写作逻辑

- 背景与问题 → 现有方法不足 → 本文方法 → 实验验证 → 结论
- 结论句已按"待实验数据确定"处理，未预设结果方向

## 缺失信息

- 数据集名称与规模
- 主要评价指标与数值
- 对比方法
- 是否进行显著性检验（决定能否使用 significantly）

注意：以上占位符必须在投稿前替换。当前草稿中没有任何虚构数值。
```

The placeholders are in Chinese inside brackets so they cannot be mistaken for manuscript text, and the closing note tells the author explicitly what state the draft is in.

## Related work with no references

**User:** 帮我写医学影像分割的相关工作，两三段就行。

**Response:** Do not produce citations. Offer the structure and ask:

```text
相关工作部分需要真实文献支撑，我不能生成参考文献——虚构的文献格式上看起来完全正常，
很容易被带进投稿稿件。两个可行方式：

**方式一（推荐）**：把你的参考文献列表发给我，我按你的文献组织结构和逻辑。

**方式二**：先给出结构框架，你后续填入引用：

现有医学图像分割方法大致可分为三类。第一类基于编码器-解码器结构
[citation needed: 该类方法代表工作]，其核心是……；这类方法在 [具体场景] 下
表现良好，但在 [具体限制] 时受限 [citation needed: 指出该限制的工作]。

第二类引入注意力机制 [citation needed]……

需要我按方式二先搭框架吗？如果告诉我你的具体子方向（器官分割 / 病灶检测 /
多模态配准），框架可以更贴近你的论述路径。
```

## Conference rebuttal

**User:** ICLR 审稿人说 "The improvement over baselines is marginal and may be within noise." 我们跑了 5 个种子，均值提升 2.1 个点，标准差 0.3。怎么回？

**Response:**

```text
## Rebuttal 草稿

**Marginal improvement / noise (R2).** We report results over 5 seeds: the
proposed method improves by 2.1 points on average (std 0.3), while the baseline's
own seed variance is [请填写 baseline 的标准差]. The gap therefore exceeds the
run-to-run variation by a substantial margin. We will add per-seed results and
variance to Table 2 in the revision.

## 说明

- 直接用你给的数据回应，未添加任何未提供的数值。
- 建议补充 baseline 的种子方差——这是回应"是否在噪声范围内"最直接的证据，
  只给自己方法的方差无法完全回答审稿人的问题。
- 如果做了显著性检验（如配对 t 检验），加上检验方法与 p 值会更有力；
  没做的话不要用 "significantly"。

## 需填写

- baseline 在相同 5 个种子下的标准差
- 表格编号是否与正文一致
```

The response used the author's real numbers, flagged the one number that would make the argument complete, and did not manufacture it.

## LaTeX editing

**User:** [pastes a LaTeX paragraph with `\cite{}`, `\ref{}`, and inline math] 帮我润色一下

**Response:** Return LaTeX, preserving all markup, then:

```text
## 保真核对

已运行 fidelity_check：引用 6/6、交叉引用 3/3、行内公式 4/4、数值 5/5 全部保留。

## 改动台账

L1：共 9 处（冠词、时态、`Section~\ref{}` 补非断行空格、`3-7` 改为 `3--7`）。

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | [片段] | [片段] | L2 | 拆分长句，主谓提前 |

## 需确认

- 第 3 句的 $\lambda$ 在本段首次出现但未见定义，可能定义在前文；若无，建议补充。
```

## Redirecting a detection-evasion request

**User:** 帮我把这段改一下，AI 检测率太高了，要降到 10% 以下。

**Response:**

```text
我不按检测器的分数来改写——这类检测工具在两个方向上都不可靠，误判率很高，
针对它优化既不稳定也没有实际意义。

但你遇到的问题通常是真实的：被判为机器生成的文本，往往确实存在可识别的写作问题。
我可以按这些问题来改：

- 句长过于均匀 → 长短交替
- 每个论点权重相同 → 区分主次，次要信息降级为从句
- 空泛表述（"various approaches have been proposed"）→ 具体化
- 模糊语堆叠（"may potentially help to some extent"）→ 保留一个
- 连接词过密 → 靠信息顺序承担逻辑
- 不表态 → 明确作者倾向哪种解释

改完之后文本会更具体、更有判断，这本身就是更好的学术写作。要我按这个思路处理吗？

另外提醒：如果这篇稿件确实使用了 AI 辅助写作，多数出版商现在要求声明。
Elsevier 要求在参考文献前加一节专门声明，ICLR 把未声明的实质性使用视为
违反行为准则。语言润色通常豁免，但门槛各家不同，建议核对目标期刊的作者指南。
```

## A short task that needs no ceremony

**User:** "The experiments shows that our method are effective." 这句怎么改？

**Response:**

```text
The experiments show that the proposed method is effective.

主谓一致两处（shows → show，are → is）；"our method" 改为 "the proposed method"
更符合期刊惯例。另外 "effective" 偏空泛，如果有具体指标，改成
"improves [指标] by [数值]" 会更有说服力。
```

No table, no headings, no 需确认 section. Matching ceremony to task size is part of the skill — a one-line fix wrapped in a full template trains the author to skim the format when it actually matters.
