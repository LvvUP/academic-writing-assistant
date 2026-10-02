<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass-dark.svg">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass：书页、修订线与核对标记" width="120">
</picture>

# Academic Writing Assistant

### 让 AI 帮你改论文，但不改你的数据和结论

面向中文科研作者的**通用学术写作 Skill**：论文润色 · 中英互译 · 章节起草 · 学位论文与基金申请 · 审稿回复 · 投稿材料<br>
适用于理工、医学、经管、社科、人文、法学等各学科，一份 Skill 可在 Claude Code、Codex、Cursor、Grok Build、OpenCode 中使用。

[![Version](https://img.shields.io/badge/version-0.4.0-2563EB)](CHANGELOG.md)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-2563EB)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-111827)](https://agentskills.io)
[![GitHub stars](https://img.shields.io/github/stars/LvvUP/academic-writing-assistant?style=social)](https://github.com/LvvUP/academic-writing-assistant/stargazers)

**中文** · [English](README_EN.md)

[快速安装](#-快速安装) · [效果示例](#-效果示例) · [功能一览](#-功能一览) · [适用学科](#-适用学科) · [常见问题](#-常见问题)

</div>

---

## 💡 为什么需要它

用 AI 改论文，语法和流畅度往往不是问题。真正危险的是那些**读起来更好、却悄悄改变了事实**的修改：

| 你写的 | AI 常见的“润色” | 问题 |
|---|---|---|
| 该方法**可能**在**部分场景**下改善性能 | 该方法显著提升了性能 | 删掉限定，主张被夸大 |
| A 与 B **相关** | A **导致** B | 相关变成因果 |
| 准确率 92.3% | 准确率 93.2% | 数字被改错 |
| （没有引用） | ……（Smith et al., 2021） | 编造参考文献 |
| 我们**拟**开展问卷调查 | 我们开展了问卷调查 | 计划写成成果 |

Academic Writing Assistant 给 AI 一份**保真契约**：语言可以大胆改，事实与证据边界不能动；涉及主张强度的修改必须单独列出，由你决定是否采用。

## 🚀 快速安装

支持 **Claude Code、Codex、Cursor、Grok Build、OpenCode**。

### 方式一：把下面这段话发给你的 AI Agent（推荐）

```text
请帮我安装（已安装则更新）学术写作 Skill「academic-writing-assistant」，全程只用仓库自带的安装脚本：
1. 判断你是哪个 Agent，确定 --host：Claude Code → claude，Codex → codex，Cursor → cursor，Grok Build → grok-build，OpenCode → opencode。不是这五个就告诉我并停止。
2. 把 https://github.com/LvvUP/academic-writing-assistant（main 分支）git clone --depth 1 到一个临时文件夹，在其中运行（需 Python 3.9+；Windows 可用 py -3 代替 python3）：
   python3 -B scripts/install_skill.py install --host <上面的值> --home-root "$HOME"
3. 如果提示已安装，把 install 换成 update 再运行；如果提示需要 --backup-existing，加上它再运行（旧副本会移到备份文件夹，不会删除）。遇到其他错误就原样告诉我并停止：不要手动复制或删除文件、不要绕过检查、不要用 sudo。
4. 完成后删除临时文件夹，把脚本输出的安装路径、版本和 note 提示告诉我，并说明调用方式、是否需要新开会话。
```

Agent 会下载仓库、运行自带的安装脚本，并告诉你结果。以后想更新，再发送一次同样的话即可。

<details>
<summary><strong>方式二：自己在终端运行同一个脚本</strong></summary>

需要 Git 和 Python 3.9+：

```sh
git clone --depth 1 https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

把 `claude` 换成你使用的 Agent：

| Agent | `--host` | 安装位置 |
|---|---|---|
| Claude Code | `claude` | `~/.claude/skills/academic-writing-assistant` |
| Codex | `codex` | `~/.agents/skills/academic-writing-assistant` |
| Cursor | `cursor` | `~/.cursor/skills/academic-writing-assistant` |
| Grok Build | `grok-build` | `~/.grok/skills/academic-writing-assistant` |
| OpenCode | `opencode` | `~/.config/opencode/skills/academic-writing-assistant` |

更新时把 `install` 换成 `update`，卸载用 `uninstall`。Windows 可用 `py -3` 代替 `python3`。两种方式用的是同一个脚本，装出来的副本可以互相更新。更多说明见 [安装指南](docs/installation.md)。

</details>

### 开始使用

安装后新开一个会话，直接用自然语言提出写作任务，Agent 会自动调用；也可以显式指定：

```text
/academic-writing-assistant 请润色下面这段摘要，保留数值、引用和结论范围，并说明重要改动。

[粘贴你的文本]
```

> Claude Code、Grok Build 使用 `/academic-writing-assistant`；Codex 使用 `$academic-writing-assistant`；Cursor 在 Agent 输入框输入 `/` 后选择；OpenCode 直接描述任务即可自动加载。

## ✨ 效果示例

> 以下均为合成示例，数据与引用仅用于演示。

### 论文润色：口语化表达 + 相关被写成因果（社会科学）

**原文**

> 我们对 412 名大学生做了问卷调查，结果发现每天刷短视频的时间越长，学习投入就越低（r = −0.29，p < 0.001）。这说明刷短视频会严重影响大学生的学习，学校应该采取措施进行干预。

**润色后**

> 本研究对 412 名大学生开展问卷调查，发现每日短视频使用时长与学习投入呈负相关（r = −0.29，p < 0.001）。[干预建议：请补充支持因果关系或干预效果的依据后再写入。]

**重要改动**

| 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|
| 刷短视频会严重影响大学生的学习 | 与学习投入呈负相关 | L3 主张 | 问卷相关分析支持“相关”，不足以支持“影响”和“严重”的判断 |
| 学校应该采取措施进行干预 | 改为待补充占位 | L3 主张 | 该建议依赖因果判断；有干预研究或文献依据时可恢复为条件化建议 |

<details>
<summary><strong>中译英：观察性研究不写成“降低风险”（医学）</strong></summary>

**中文原文**

> 在这项回顾性队列研究中，我们纳入了 2018—2022 年间在本院就诊的 1,236 名 2 型糖尿病患者。与未使用该药物的患者相比，使用该药物的患者心血管事件风险较低（HR = 0.78，95% CI 0.64–0.95），但这一关联在 65 岁及以上患者中不明显。

**英文译文**

> In this retrospective cohort study, we included 1,236 patients with type 2 diabetes who attended our hospital between 2018 and 2022. Compared with non-users, patients who used the drug had a lower risk of cardiovascular events (HR = 0.78, 95% CI 0.64–0.95), although this association was not evident in patients aged 65 years or older.

**译法说明：** “风险较低”译为 *had a lower risk*，而不是 *reduced the risk*，因为队列研究只支持关联；“不明显”译为 *not evident*，不写成 *no effect*。数值、置信区间和年龄界值逐一对应。

</details>

<details>
<summary><strong>审稿回复：只写作者确认已完成的修改（计算机）</strong></summary>

**审稿意见**

> The accuracy gain may come at the cost of higher inference latency.

**作者材料**

> 我们同意需要量化推理开销。已在同一张 GPU、batch size = 1、相同输入分辨率下测量推理延迟：baseline 为 18 ms/图像，我们的方法为 21 ms/图像；准确率分别为 84.2% 和 86.1%。已将这组结果补入修订稿表 4，并在第 5.2 节补充准确率与延迟的权衡。请写成英文期刊回复。

**回复草稿**

> Thank you for raising this point. We have quantified the accuracy–latency trade-off on the same GPU, with a batch size of 1 and the same input resolution. Our method achieves an accuracy of 86.1% at 21 ms per image, compared with 84.2% at 18 ms per image for the baseline. The gain in accuracy comes with higher latency. We have added these results to Table 4 and a discussion of the trade-off to Section 5.2 of the revised manuscript.

**组织方式：** 直接回应问题，给出可比较的结果，再指向已完成的修改。表号、章节和完成状态均来自作者材料，不替作者承诺新实验。

</details>

[查看更多示例 →](examples/)

## 📋 功能一览

| 你正在做什么 | 可以交给它的工作 |
|---|---|
| ✍️ 修改论文 | 中英文润色、扩写、合并段落、按字数压缩、优化标题与贡献表述 |
| 🌐 中英互译 | 中译英、英译中，术语对照与重要译法说明，保留 LaTeX 与引用 |
| 📄 起草章节 | 依据你提供的材料组织摘要、引言、相关工作、方法、结果、讨论与结论 |
| 🎓 学位论文与申请书 | 学位论文各章、中英文摘要对照、开题报告、基金/项目申请书 |
| 💬 回应审稿 | 期刊逐条回复信、会议 rebuttal，区分已完成修改与计划 |
| 📮 准备投稿 | Cover letter、Highlights、AI 使用声明、CRediT 贡献声明 |
| 📚 引用与格式 | 按 GB/T 7714、APA 等整理参考文献；保留 LaTeX 引用、公式与交叉引用 |
| 🔍 全文自查 | 跨章节检查术语、缩写、符号、数值与主张是否前后一致 |

## 🧭 适用学科

内置 12 个学科大类的写作提示，未列出的学科按通用流程处理，跟随你的学科惯例与论文结构。

| 领域 | 学科大类 |
|---|---|
| 📚 人文社科 | 人文学科 · 法学 · 经济学与管理学 · 社会科学 · 教育学与心理学 |
| 🩺 医学与生命科学 | 医学与公共卫生 · 生命科学与农学 |
| 🔬 理学 | 物理化学与材料 · 数学与统计 · 地球与环境科学 |
| ⚙️ 工程与计算机 | 工程技术 · 计算机与人工智能 |

**研究类型同样被区分对待：** 实验 · 调查与计量 · 定性研究 · 理论证明 · 综述 · 人文与法学阐释 · 案例研究 · 设计研究

> 不会要求人文论文写“实验设置”，也不会把访谈主题写成总体比例。

## 🛡️ 核心原则：保真契约

| 区域 | 包括什么 | 怎么处理 |
|---|---|---|
| 🔒 **锁定区** | 数值、单位、p 值、引用、公式、法条、直接引语、伦理批号…… | 原样保留；发现疑似错误只标出，不擅自“更正” |
| ⚖️ **承重语言** | 可能、部分、相关、导致、显著、首次、应当…… | 增强或削弱都要有依据，并单独列出 |
| ✏️ **自由表层** | 语法、拼写、标点、语序、冗余 | 直接改进 |

所有修改按 **L1 表层 / L2 结构 / L3 主张** 分级：短句纠错直接给结果，较长修订附上重要改动台账，涉及主张的修改永远不会静默发生。

学术诚信方面，它**不编造**参考文献、数据、实验结果或作者行动，缺失信息用 `[请补充……]` 明确占位；也不提供“降低 AI 检测率”或绕过查重的服务。完整规则见 [SKILL.md](skills/academic-writing-assistant/SKILL.md)。

## 🔧 本地核查工具（可选）

核心写作不需要 Python。如果 Agent 可以运行 Python，还可以用内置脚本做机械核查：

| 脚本 | 用途 |
|---|---|
| `fidelity_check.py` | 比对修改前后的数值、引用、公式、法条序号等是否被改动 |
| `manuscript_audit.py` | 检查缩写首次定义、缺少统计依据的“显著”、字数与字符限制 |
| `terminology_checker.py` | 发现同一概念的不同译法、易混淆的相关概念 |
| `structure_checker.py` | 提示摘要、引言等章节可能缺少的要素 |

脚本只使用 Python 标准库，在本地运行、不联网。用法见 [脚本说明](docs/scripts.md)。

## ❓ 常见问题

<details>
<summary><strong>会改动我的数据或结论吗？</strong></summary>

不会静默改动。数值、引用、公式属于锁定区；涉及结论强度的修改会在台账中列出并说明理由。发现正文与表格数值不一致时，它会指出冲突，而不是自行选一个。

</details>

<details>
<summary><strong>能帮我降低 AI 检测率或查重率吗？</strong></summary>

不针对检测分数优化，也不承诺任何分数。它可以改善确实存在的空泛、重复、逻辑和引用问题，让文本更具体、更清楚。

</details>

<details>
<summary><strong>我的稿件安全吗？</strong></summary>

本项目的脚本在本地运行、不联网、不收集数据。但你所用的 AI Agent 或云端模型会接收你提供的文本，请按平台和所在机构的数据政策决定提交哪些材料。

</details>

<details>
<summary><strong>没有提供参考文献，能写相关工作吗？</strong></summary>

Agent 有检索能力时，可以实际检索并注明读到了什么；没有检索能力时，会给出结构、检索词和明确的引用占位，不会凭记忆编造文献。

</details>

更多问题见 [FAQ](docs/faq.md)。

## 🤝 参与贡献

欢迎补充学科写作惯例、术语对照和合成示例，也欢迎修复脚本问题。请先阅读 [贡献指南](CONTRIBUTING.md)，后续计划见 [路线图](ROADMAP.md)，版本变化见 [更新记录](CHANGELOG.md)。

如果这个 Skill 对你的论文写作有帮助，欢迎点一个 ⭐ **Star**，让更多科研作者发现它。

[![Star History Chart](https://api.star-history.com/svg?repos=LvvUP/academic-writing-assistant&type=Date)](https://star-history.com/#LvvUP/academic-writing-assistant&Date)

## 📄 许可

本项目采用 **AGPL-3.0-only** 许可，见 [LICENSE](LICENSE) 与 [许可说明](docs/licensing.md)。
