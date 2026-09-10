# 审稿回复示例：事实与行动状态

以下输入、审稿意见和数字均为合成示例。回复长度与允许提交的内容取决于具体 venue。

## 示例一：已完成的修改

### User Input

```text
Reviewer: The novelty of the proposed method is unclear.
我们已经在修订稿的 3.1 节加了一段说明，并新增了 Table 6。
```

### Expected Output

```text
Comment: The novelty of the proposed method is unclear.

Response: We have added a paragraph in Section 3.1 and added Table 6.
[请提供具体技术区别、修订段落和 Table 6 的内容，以便说明其如何回应创新性质疑。]
```

可以陈述作者确认的新增位置。不能进一步猜测 Table 6 是消融实验或已隔离某组件的贡献，也不替作者默认承认原文表达不清。

## 示例二：标准差归属未知

### User Input

```text
ICLR 审稿人：The improvement over baselines is marginal and may be within noise.
我们跑了 5 个种子，均值提升 2.1 个点，标准差 0.3。
```

### Expected Output

```text
We evaluated 5 seeds and observed a mean improvement of 2.1 points.
[请确认 0.3 是方法得分、baseline 得分，还是逐种子配对差值的标准差，
并补充对应统计分析后再回应波动问题。]
```

均值差不能单独排除随机波动。没有输入的 R2、Table 2、显著性结论与新增实验/表格计划不应出现。标准差不是方差。

## 示例三：作者已确认统计量和计划

### User Input

```text
同一评测协议下，5 对种子结果的平均差值为 2.1 个百分点；0.3 个百分点是这5个
配对差值的样本标准差。我们已决定在修订稿的补充材料中提供逐种子结果，尚未添加。
暂未提供显著性检验。
```

### Expected Output

```text
Across 5 paired seeds under the same evaluation protocol, the mean difference
was 2.1 percentage points, with a sample standard deviation of 0.3 percentage
points for the paired differences. We will provide the per-seed results in the
supplementary material of the revision.
```

不再追问已经确认的标准差定义或计划；仍不据此推断统计显著性或声明材料已经添加。
