<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass.png">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass：书页、修订线与核对标记" width="112">
</picture>

# Academic Writing Assistant

**让研究表达更清晰，让论文写作更高效。**

面向科研作者的中英文学术写作 Skill，覆盖论文润色、中英互译、章节起草、审稿回复与投稿材料。

**中文** · [English](README_EN.md)

[写作示例](#写作示例) · [支持的任务](#支持的任务) · [安装使用](#安装使用)

</div>

## 写作示例

以下为合成写作示例，数据与引用键仅供演示。

### 论文润色：把实验设置、结果与结论讲清楚

**原文**

> 为了看融合模块的作用，我们做了消融实验，训练设置都一样，测试用的是同一个测试集。去掉融合模块以后，Dice 从 86.4% 变成 83.1%，小病灶（直径 < 10 mm）这一组则从 78.2% 变成 72.6%。这些结果支持融合模块对本测试集上的分割有帮助，见表 3。

**润色后**

> 在相同训练设置和测试集上，我们通过消融实验评估融合模块的作用。移除该模块后，Dice 从 86.4% 降至 83.1%；在小病灶（直径 < 10 mm）组中，Dice 从 78.2% 降至 72.6%（表 3）。这些结果支持融合模块有助于改善本测试集上的分割表现。

**修改说明：** 先交代实验设置，再并列报告两组结果，最后给出结论。数值、小病灶定义和表号保持一致，结论仍限定在本测试集。

<details>
<summary><strong>中译英：让训练设置、比较对象与结果一目了然</strong></summary>

**中文原文**

> 为减轻季节变化对土地覆盖分类的影响，我们把来自春季和秋季的影像拿来联合训练，并沿用已有的多尺度融合模块 `\cite{demo_fusion}`。联合训练模型的宏平均 F1 为 0.81，只用春季影像训练的模型是 0.76。两个模型都在北部研究区的同一批秋季测试影像上评估。

**英文译文**

> To reduce the effect of seasonal variation on land cover classification, we jointly trained the model on spring and autumn imagery using the existing multi-scale fusion module `\cite{demo_fusion}`. Both models were evaluated on the same autumn test images from the northern study area. The model trained on both seasons achieved a macro-F1 score of 0.81, compared with 0.76 for the model trained only on spring imagery.

**译法说明：** 将评估设置移到结果之前，让两种训练方式的比较更清楚。术语统一为 land cover classification 和 macro-F1，引用键、数值与评估区域一一对应。

</details>

<details>
<summary><strong>审稿回复：用已完成的补充结果回应推理开销问题</strong></summary>

**审稿意见**

> The accuracy gain may come at the cost of higher inference latency.

**作者材料**

> 我们同意需要量化推理开销。已在同一张 GPU、batch size = 1、相同输入分辨率下测量推理延迟：baseline 为 18 ms/图像，我们的方法为 21 ms/图像；准确率分别为 84.2% 和 86.1%。已将这组结果补入修订稿表 4，并在第 5.2 节补充准确率与延迟的权衡。请写成英文期刊回复。

**回复草稿**

> Thank you for raising this point. We have quantified the accuracy–latency trade-off on the same GPU, with a batch size of 1 and the same input resolution. Our method achieves an accuracy of 86.1% at 21 ms per image, compared with 84.2% at 18 ms per image for the baseline. The gain in accuracy comes with higher latency. We have added these results to Table 4 and a discussion of the trade-off to Section 5.2 of the revised manuscript.

**组织方式：** 直接回应问题，给出可比较的结果，再指向已完成的修改。数值与方法逐一对应，表号、章节和完成状态均来自作者材料。

</details>

[浏览更多写作示例 →](examples/)

## 支持的任务

| 你正在做什么 | 可以交给 Skill 的工作 |
|---|---|
| 修改论文 | 中英文润色、扩写、合并段落、压缩篇幅、优化标题 |
| 中英互译 | 中译英、英译中、术语对照与重要译法说明 |
| 起草章节 | 根据已有材料组织摘要、引言、相关工作、方法、结果、讨论与结论 |
| 回应审稿 | 期刊逐条回复信、会议 rebuttal、证据与修订位置整理 |
| 准备投稿 | Cover letter、Highlights、AI 使用声明、CRediT 贡献声明 |
| 整理长稿与 LaTeX | 跨章节术语、缩写、符号与主张一致性；保留引用、公式和交叉引用 |

### 学科与研究类型

内置领域适配涵盖计算机视觉、机器学习与人工智能、自然语言处理与大模型、医学影像与临床研究、遥感、机器人、数据挖掘与推荐、生物信息学、材料科学与化学、社会科学与教育管理。

写作重点随研究语境调整：医学影像关注验证范围，遥感关注区域与传感器条件，机器学习关注比较设置与实验波动。理论证明、定性研究和综述也有相应的组织方式。未列出的学科，可以提供领域背景、研究类型和核心术语，按你的约定处理。

## 为学术写作准备的工作方式

把可复用的写作规则交给 Agent，每次按具体任务使用：

- **遵循领域写作习惯。** 结合学科、章节和研究类型，调整术语、信息顺序与叙述重点。
- **保留研究事实。** 改善句子时同时关注数值、引用、公式和结论范围，让表达与已有证据相符。
- **解释重要改动。** 先给可用正文，再说明结构调整与涉及主张的改动，方便作者决定采用哪些修改。
- **按任务调节深度。** 一句纠错可以直接给改文；标准修订附必要说明；长稿审阅关注跨章节一致性与材料之间的对应。

了解完整的[写作规范与学术诚信原则](skills/academic-writing-assistant/SKILL.md)。

## 安装使用

### Codex

在装有 **Python 3.9+** 的终端运行：

```sh
git clone --branch main https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host codex --home-root "$HOME"
```

Skill 安装到 `~/.agents/skills/academic-writing-assistant`。刷新 Skill 列表或开启新会话后，在 Codex 中输入：

```text
$academic-writing-assistant
请润色下面这段中文，让逻辑更紧凑，保留数值、引用和结论范围，并说明重要改动。

[粘贴原文]
```

### Claude Code

完成上面的克隆步骤后，在仓库目录运行：

```sh
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

Skill 安装到 `~/.claude/skills/academic-writing-assistant`。开启新会话后，使用斜杠命令：

```text
/academic-writing-assistant
请将下面这段中文译成英文，保留数值、引用与术语含义，并说明重要译法。

[粘贴原文]
```

<details>
<summary><strong>Cursor、Grok Build 与其他 Agent</strong></summary>

克隆仓库后，按宿主选择一条安装命令：

```sh
# Cursor
python3 -B scripts/install_skill.py install --host cursor --home-root "$HOME"

# Grok Build 官方编码 Agent
python3 -B scripts/install_skill.py install --host grok-build --home-root "$HOME"
```

- **Cursor：** 安装到 `~/.cursor/skills/academic-writing-assistant`，在 Agent 输入 `/` 并选择该 Skill。
- **Grok Build：** 安装到 `~/.grok/skills/academic-writing-assistant`，使用 `/academic-writing-assistant`。
- **其他 Agent：** 加载完整的 `skills/academic-writing-assistant/` 目录，以 `SKILL.md` 为主指令，按任务读取 `references/` 中的文件。

核心文本写作只需要宿主能加载指令；文件解析、检索与脚本执行使用宿主提供的能力。宿主目录、项目安装和插件方式见[兼容说明](docs/compatibility.md)。

</details>

已有安装需要更新时，见[安装、更新与常见问题](docs/installation.md)。

## 文档与参与

- [更多示例](examples/) · [常见问题](docs/faq.md) · [不同研究类型示例](examples/research-types.md)
- [稿件核查工具](docs/scripts.md)：`fidelity_check.py` 比对数值、引用与公式；`manuscript_audit.py` 检查缩写与篇幅。
- [贡献指南](CONTRIBUTING.md) · [更新记录](CHANGELOG.md) · [路线图](ROADMAP.md)

欢迎补充学科术语、写作规则和合成示例。如果这个 Skill 对你的论文写作有帮助，欢迎点一个 **Star**，让更多科研作者发现它。

许可：**AGPL-3.0-only**，见 [LICENSE](LICENSE)。
