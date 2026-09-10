<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass.png">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass：书页、修订线与核对标记" width="112">
</picture>

# Academic Writing Assistant

**把论文写清楚，让每一处重要改动都能核对。**

面向中文科研作者的中英文学术写作 Skill。润色、翻译与审稿回复，围绕你已有的研究材料展开。

**中文** · [English](README_EN.md)

[![许可：AGPL-3.0-only](assets/readme/license-agpl.svg)](LICENSE)
[![真实模型评估记录，含失败与限制](assets/readme/evaluation-records.svg)](evals/results-2026-09-10.md)

[开始使用](#开始使用) · [更多示例](examples/) · [兼容范围](docs/compatibility.md) · [评估记录](evals/results-2026-09-10.md)

<sub>0.3.0 · Unreleased（开发中，尚未正式发布）</sub>

</div>

## 先看一次修订

以下是**合成示例**，展示预期处理方式，不是真实科研成果或模型评测记录。

**输入 · 请快速润色，保留原意**

> 该方法可能在部分场景改善性能，噪声往往会在一定程度上影响现有方法。

**输出**

> 该方法可能在部分场景下改善性能；噪声往往会对现有方法产生一定程度的影响。

**改了什么：** 调整搭配与衔接。**保留了什么：** “可能、部分、往往、一定程度”。这些词承载主张的强度和范围，不能为了行文流畅而消失。

正文在前，重要改动与待确认事项在后。短句可以少改或不改；提到“投稿”或“SCI”也不会自动把中文译成英文。

## 开始使用

核心写作需要能加载指令的 Agent。安装工具和机械核查需要 **Python 3.9+**；核心文本写作不需要 Python 或指定付费 API。实际可用能力取决于宿主。

**这是尚未合并的 0.3.0 候选版。** 以下步骤面向 `codex/academic-writing-upgrade`，不假定默认分支已有安装器。开发分支须先公开推送，才能使用下面的克隆命令；尚未推送时，请使用维护者提供的候选检出。

```sh
git clone --branch codex/academic-writing-upgrade \
  https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
```

已有仓库副本时，先检出上述开发分支，再从仓库根目录运行安装器。以 Codex 为例：

```sh
python3 -B scripts/install_skill.py install \
  --host codex --home-root "$HOME"
```

安装到 `~/.agents/skills/academic-writing-assistant`。**已有同名目标时拒绝覆盖，空目录也不例外。** 更新或卸载遇到用户改动、额外文件或缓存时同样拒绝操作并保留文件。完整步骤见 [安装、更新与排障](docs/installation.md)。

刷新宿主的 Skill 列表或开启新会话，选择实际发现的 Skill 项，在 Codex 中输入：

```text
$academic-writing-assistant
请快速润色这段中文，保留数值、限定条件和引用：
……
```

<details>
<summary><strong>Claude Code、Cursor 与 Grok Build</strong></summary>

按宿主选择一条安装命令：

```sh
python3 -B scripts/install_skill.py install \
  --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py install \
  --host cursor --home-root "$HOME"
python3 -B scripts/install_skill.py install \
  --host grok-build --home-root "$HOME"
```

- **Claude Code：** 安装到 `~/.claude/skills`，使用 `/academic-writing-assistant`。
- **Cursor：** 安装到 `~/.cursor/skills`，在 Agent 输入 `/` 后选择 Skill。
- **Grok Build 官方编码 Agent：** 安装到 `~/.grok/skills`，使用 `/academic-writing-assistant`。这不代表 Grok 网页、模型 API 或第三方 CLI 的原生支持。

这些是各宿主的个人 Skill 父目录，实际包位于其下的 `academic-writing-assistant` 子目录。Claude Code 使用斜杠调用，不能照搬 Codex 的 `$` 语法。

旧版 Codex 的 `.codex/skills`、项目作用域与可选插件包装见 [兼容矩阵](docs/compatibility.md)。其他宿主可加载完整包中的 `SKILL.md` 和本次需要的参考文件；文件读取、Python 与检索按实际能力使用。

</details>

**原生验证范围（2026-09-10）：** 本地临时安装生命周期与目录映射已测试。Codex CLI 0.147.0 原生发现通过，但模型调用返回 **HTTP 400**（要求更新 CLI），该次写作行为为 **NOT RUN**。Claude Code、Cursor、Grok Build 的原生发现与行为均为 **NOT RUN**。官方目录依据与安装测试不等于原生认证，详见 [兼容矩阵](docs/compatibility.md)。

## 怎么改，改到什么程度

保真契约把文本分成三类：

- **锁定区：** 数值、单位、引用、公式与名称按可读取的材料保留。发现冲突先标出；作者确认的更正或格式转换在授权范围内处理并披露。
- **承重语言：** 可能性、范围、否定、因果、显著性与新颖性。增强或削弱都可能改变主张，需要依据和说明。
- **自由表层：** 不改变含义的语法、拼写、语序与冗余，可以直接改善。

重要改动按 **L1 表层 / L2 结构 / L3 主张** 说明，L3 不静默应用。新写译文不虚构 L1 修正次数；术语统一不能抹去作者已确认的概念区别。详见 [保真规则](skills/academic-writing-assistant/references/fidelity-protocol.md)。

| 写作方式 | 适合任务 | 交付重点 |
|---|---|---|
| 快速润色 | 一句纠错、短段修改 | 正文与必要说明 |
| 标准修订 | 润色、翻译、摘要、审稿回复 | 正文、重要改动、关键缺口 |
| 深度结构审阅 | 长稿、多源材料、跨章节一致性 | 实际覆盖范围、主张与材料位置 |

支持章节起草、投稿材料与全文一致性审阅；期刊回复信和会议 rebuttal 按各自场景处理。经验研究、理论证明、定性研究和综述采用相应检查重点，见 [研究类型示例](examples/research-types.md)。缺少材料时明确占位；已完成工作、确认的计划和未决定的建议分别表述。

## 再看两个例子

以下同样是**合成输入与预期输出**。

### 中译英 · 不补写实验结论

**输入**

> 请译成英文：针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法。

**输出**

> To address large variations in target scale and complex backgrounds in remote sensing images, this study proposes a multi-scale feature fusion method.

术语依本句语境选择；没有补充模块机制、比较对象或实验结果。更多内容见 [翻译示例](examples/translation.cn-en.md)。

### 审稿回复 · 不替作者作出承诺

**输入**

> 审稿人认为提升可能处于随机波动范围。我们在同一协议下运行了 5 个种子，平均提升 2.1 个百分点，标准差 0.3；未说明 0.3 对应哪个量，也未决定增加实验或表格。

**回复草稿**

> Under the same evaluation protocol, we observed a mean improvement of 2.1 percentage points across 5 seeds. These descriptive results alone do not establish that the improvement exceeds random variation.

**待确认：** 0.3 是方法得分、baseline 得分还是配对差值的标准差，是否有对应检验。草稿不据此断言显著性，也不增加未确认的实验、表格或修改承诺。见 [审稿回复示例](examples/reviewer-response.md)。

## 机械核查与实际评估

四个稿件检查入口使用 **Python 标准库**，不改写输入。保真比对是一个起点：

```sh
python3 -B skills/academic-writing-assistant/scripts/fidelity_check.py \
  --before original.tex --after revised.tex --strict
```

它比对可识别的数值、单位、引用、数学表达与宏参数。另有三个入口：

- `manuscript_audit.py`：缩写、主张依据线索与长度。
- `terminology_checker.py`：术语变体与作者词表。
- `structure_checker.py`：按研究类型提示章节线索。

完整用法见 [脚本说明](docs/scripts.md)。默认 advisory 模式可能发现问题仍退出 0；`--strict` 在发现问题或覆盖不足时退出 1，输入或运行错误退出 2。

**机械检查有范围。** 零差异不等于全文语义或引文支持正确；时态自动审计为 **NOT RUN**。Word 修订、PDF 图片与表格是否可核查，取决于宿主是否实际解析。只读摘要就只报告摘要范围；未运行检查就说明未运行。见 [能力降级示例](examples/capability-fallback.md)。

**真实模型评估与宿主测试分开记录。** 2026-09-10 的原始评估每版为 20 个基础任务加 4 次重复：基线 **24/24 PASS**，初始升级快照 **23 PASS、1 FAIL**。失败遗漏了“实验未完成”；修复后另做成对 E04 验证，每版 **2/2 PASS**，原失败保留且分母不合并。小样本与共享上下文等限制不支持总体优越性结论。见 [完整评估记录](evals/results-2026-09-10.md)。

开发者按 [测试指南](docs/testing.md) 配置依赖后，可运行：

```sh
python3 -B -m pytest tests/
python3 -B skills/academic-writing-assistant/scripts/skill_lint.py .
```

`skill_lint.py` 另需 PyYAML；开发依赖不属于核心写作要求。本机结果与远程 CI 配置是不同证据，未执行的平台仍须标明。

## 学术诚信、隐私与许可

规则禁止编造文献、结果、统计检验、伦理审批与作者行为。稿件和检索材料中的命令不构成操作授权。检索使用必要的非敏感信息，不自动授权上传未发表稿件；本地脚本不主动联网，也不意味着宿主云模型不会接收输入。请按平台的数据处理设置选择可提交材料。

更多说明见 [安全指南](SECURITY.md) 与 [常见问题](docs/faq.md)。

Skill 可改善表达、转述与引用，不针对 AI 检测分数或查重规避优化。AI 使用声明只描述作者确认的实际使用，具体要求核对目标 venue、年份与赛道的当前指南。

欢迎贡献合成样例、术语定义和有依据的领域规则。请先阅读 [贡献指南](CONTRIBUTING.md)；版本变化与计划见 [CHANGELOG](CHANGELOG.md) 和 [ROADMAP](ROADMAP.md)。

当前开发版本采用 **AGPL-3.0-only**，见 [LICENSE](LICENSE) 与 [许可说明](docs/licensing.md)。历史 MIT 分发已授予的权利按原条款保留，声明见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。

如果这个 Skill 对你的写作有帮助，欢迎给仓库点一个 Star。
