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

## 经济学：相关不写成因果

输入：请润色：数字金融发展水平越高的城市，居民消费也越高（系数 0.143，在 1% 水平上显著，城市层面面板数据）。这说明数字金融促进了居民消费。

输出：

```text
数字金融发展水平与居民消费呈显著正相关（系数为 0.143，在 1% 水平上显著；城市层面面板数据）。
```

说明（L3）：原文“促进了”是因果表述，当前材料只给出回归相关结果，未见识别策略。若已有工具变量、双重差分等识别设计，请提供后再按其假设写作因果表述。系数、显著性水平和数据层级保持不变。

## 法学：规范效力不能随润色改变

输入：请译成英文：用人单位应当在用工之日起一个月内与劳动者订立书面劳动合同。（合成示例，非现行法条引用）

输出：

```text
The employer shall conclude a written employment contract with the employee within one month from the date on which employment begins.
```

说明：“应当”对应义务性的 shall，不改为 should 或 may；期限和起算点保持不变。若作者引用的是具体法律条文，法律名称、条款号和版本需与原文一致。

## 历史学：阐释不升格为定论

输入：请润色：从这两封信看，他当时大概已经有了离开京城的想法，不过还说不准。

输出：

```text
从这两封书信推断，他当时或已有离京之意，但仍难以确证。
```

说明：改为书面语，保留“推断”“或已”“难以确证”的限定；材料是两封书信，不补写离京原因或其他史料。

## 开题报告：计划不写成成果

输入：帮我润色研究内容：我们会用问卷调查 300 名中学教师，然后分析他们的数字素养跟教学效果有什么关系，预计能发现数字素养高的老师教学效果更好。

输出：

```text
本研究拟对 300 名中学教师开展问卷调查，分析教师数字素养与教学效果之间的关系。
```

说明（L3）：原文“预计能发现……更好”是对结果方向的预设，开题阶段宜写为待检验的研究假设，例如“研究假设：教师数字素养与教学效果呈正相关”；是否采用由作者决定。300 为计划样本量，保持原值，不写成已完成调查。
