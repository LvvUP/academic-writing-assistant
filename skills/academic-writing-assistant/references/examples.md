# Examples

以下均为合成任务及预期输出，用于展示规则；不是实测模型结果或脚本运行记录。数字仅属于对应输入，不能迁移到真实稿件。

## 中文润色：不增加对照对象

输入：请润色中文：我们的方法可以减少标注困难的问题，而且分割结果比较好，对小病灶也有帮助。

输出：

```text
该方法可以缓解标注困难，分割表现较好，对小病灶分割也有帮助。

调整了冗余表达与衔接。需确认两项定性评价对应的实际结果；未增加比较对象或数值。
```

## CN→EN translation

输入：请译成英文：针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法。

输出：

```text
To address large variations in target scale and complex backgrounds in remote
sensing images, this study proposes a multi-scale feature fusion method.
```

术语按给定语境选择；不虚构 L1 语法修正数，不添加实验结果。

## Abstract with no results yet

输入：写英文摘要：小目标特征弱、背景干扰大；方法包含上下文增强和多尺度特征融合；实验尚未完成。

输出：

```text
Small object detection is challenging because small objects have weak features
and are easily affected by complex backgrounds. This study uses a context
enhancement module and a multi-scale feature fusion module.
[Results and conclusions remain to be supplied after the experiments are completed.]
```

没有假设模块机制、比较结果或数据集。“实验表明”不能先写成事实再只把数字留空。

## Related work with no references

输入：帮我写医学影像分割的相关工作，当前没有参考文献。

无检索能力时可给：

```text
当前无法检索核验文献。可先按你提供的研究问题组织：
[请确定比较的研究方向] → [各方向的真实代表来源和结论] → [与本文的具体关系]。
需要文献支持的具体分类与局限暂不写成事实。
```

有检索能力且任务授权时实际查证，记录读取范围和支持状态，而非按此例一概拒绝文献列表。

## Conference rebuttal

输入：The improvement over baselines is marginal and may be within noise. 作者说跑了 5 个种子，均值提升 2.1 个点，标准差 0.3；未提供编号、检验和计划。

输出：

```text
We evaluated 5 seeds and observed a mean improvement of 2.1 points.
[请确认 0.3 的统计对象：方法得分、baseline 得分，还是配对差值；
再补充对应分析以回应随机波动问题。]
```

不添加 R2、Table 2 或修改承诺，不把标准差称为 variance，不声称差距超出随机波动。

## LaTeX editing without execution tools

输入：仅润色，宿主不能运行程序：`The results shows that $x_i$ remains bounded under assumption A~\cite{synthetic-key}.`

输出：

```latex
The results show that $x_i$ remains bounded under assumption A~\cite{synthetic-key}.
```

说明：只修主谓一致；可见公式、条件和引用保持原样。无执行工具，机械保真检查未运行。引用键是合成示例，未验证真实文献支持。

## Stronger claim / only-body

输入：只给正文，把“可能在部分场景改善性能”写得更强，没有补充数据。

输出：

```text
该方法可能改善部分场景下的性能。
```

缺少新证据时保留原意；only-body 不允许悄悄删可能与部分。若原文语义冲突无法处理，最小必要说明或明显占位优先于无条件新主张。

## A short task

输入：The experiments shows that our method are effective. 只纠正语法。

输出：

```text
The experiments show that our method is effective.
```

只有两处可追踪主谓一致修正；不额外把 our method 改成“更符合期刊惯例”的其他表述。

## Detection-evasion request

有原文时简短说明不针对检测分数优化，再处理原文实际存在的重复、逻辑或引用问题。不承诺分数，不断言被标记文本必然质量低，不擅自添加作者偏好的解释。
