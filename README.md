<div align="center">

![Revision Compass](assets/logo/revision-compass.svg)

# Academic Writing Assistant

面向中英文学术论文的领域自适应写作 Skill。

**中文** | [English](README_EN.md)

</div>

## 项目定位

`academic-writing-assistant` 是一个面向中文科研作者的学术写作 Skill / Plugin 项目，用于在保持学术诚信和技术含义准确的前提下，辅助完成论文润色、翻译、扩写、合并、章节写作、审稿回复、标题优化和术语一致性检查。

它适合研究生、博士生、青年教师和科研作者，也适合希望把学术写作工作流沉淀为可复用 Skill 的 AI Agent 用户。

## 为什么需要

中文科研作者经常需要在中文思路、英文投稿语言、领域术语和审稿沟通之间切换。普通提示词可以处理单次任务，但很难稳定地覆盖任务识别、领域适配、输出格式和学术诚信边界。

这个项目把常见学术写作需求拆成可路由的任务、可按需加载的参考文件、可复用的输出模板和轻量检查脚本，帮助作者更清楚、更规范、更可信地表达研究内容。

## 核心功能

| 功能 | 说明 |
|---|---|
| 任务路由 | 自动识别润色、翻译、扩写、合并、章节写作、审稿回复等任务 |
| 领域适配 | 根据研究领域调整写作重点、术语和谨慎程度 |
| 学术润色 | 提升清晰度、逻辑、语法和学术语气，同时保持技术含义 |
| 中英文学术翻译 | 支持中译英和英译中，并提供术语表和译法说明 |
| 论文各章节写作 | 支持摘要、引言、相关工作、方法、实验、讨论和未来工作 |
| 审稿回复 | 起草礼貌、具体、非防御性的审稿回复和修改说明 |
| 标题优化 | 生成多个克制、准确、适合投稿的标题候选 |
| 术语一致性 | 检查术语混用并建议统一表达 |
| 学术诚信护栏 | 明确禁止虚构文献、数据集、实验结果和不受支持的结论 |

## 支持的学术写作任务

- 学术润色
- 段落扩写
- 段落合并
- 中文到英文学术翻译
- 英文到中文学术翻译
- 摘要写作
- 引言写作
- 相关工作组织
- 方法部分写作
- 实验部分写作
- 讨论、局限与未来工作写作
- 审稿回复起草
- 标题优化
- 术语一致性检查
- 学术自然化表达
- 学术写作提示词优化

## 支持的研究领域

| 领域 | 写作重点 |
|---|---|
| 计算机视觉 | 模型结构、特征表示、鲁棒性、泛化能力、消融实验 |
| 人工智能 | 推理、规划、表征学习、多模态、评估边界 |
| 机器学习 | 优化目标、泛化能力、训练稳定性、模型复杂度 |
| 医学影像 | 临床相关性、数据异质性、可解释性、外部验证 |
| 遥感 | 空间分辨率、尺度变化、多源融合、地理泛化 |
| 自然语言处理 | 语义表征、上下文建模、预训练模型、数据偏差 |
| 机器人 | 感知、规划、控制、实时性、传感器融合 |
| 数据挖掘 | 模式发现、可扩展性、噪声鲁棒性、评估指标 |
| 生物信息学 | 样本异质性、统计显著性、生物学解释 |
| 材料科学 | 实验条件、结构-性能关系、表征方法、可重复性 |

## 目录结构

```text
academic-writing-assistant/
├── .codex-plugin/plugin.json
├── assets/logo/
├── skills/academic-writing-assistant/
│   ├── SKILL.md
│   ├── references/
│   ├── assets/terminology-map.zh-en.json
│   └── scripts/
├── examples/
├── tests/
├── docs/
├── evals/
├── README.md
├── README_EN.md
└── LICENSE
```

`SKILL.md` 保留核心说明、触发条件、任务入口和质量要求；详细规则放在 `references/` 中，便于 Agent 按需读取。

## 安装

### Codex 安装

克隆仓库：

```bash
git clone https://github.com/LvvUP/academic-writing-assistant.git
```

复制 Skill 到 Codex 本地 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R academic-writing-assistant/skills/academic-writing-assistant ~/.codex/skills/
```

开启新的 Codex 会话后，可以使用：

```text
Use $academic-writing-assistant to polish this academic paragraph.
```

也可以用自然语言触发，例如：

```text
我是做医学影像分割的，请帮我把下面这段话润色成 SCI 论文风格。
```

如果你的 Codex 环境支持本地插件，也可以使用仓库中的 `.codex-plugin/plugin.json` 作为插件 manifest。

### Claude Code 安装

克隆仓库：

```bash
git clone https://github.com/LvvUP/academic-writing-assistant.git
```

复制 Skill 到 Claude Code 本地 skills 目录：

```bash
mkdir -p ~/.claude/skills
cp -R academic-writing-assistant/skills/academic-writing-assistant ~/.claude/skills/
```

开启新的 Claude Code 会话后，可以使用：

```text
Use $academic-writing-assistant to translate this Chinese academic paragraph into English.
```

### 其他 Agent 安装

如果你的 Agent 支持 Skill 目录机制，请复制整个目录：

```text
skills/academic-writing-assistant/
```

如果你的 Agent 不支持 Skill 机制，可以将 `skills/academic-writing-assistant/SKILL.md` 作为主指令，并在需要时加载 `references/` 中的任务路由、领域适配、写作流程、输出模板和质量检查文件。

不要只复制 `scripts/`。脚本只能做辅助检查，真正的任务路由、领域适配和学术诚信规则都在 `SKILL.md` 与 `references/` 中。

## 使用示例

### 学术润色

输入：

```text
我是做医学影像分割的，请帮我把下面这段话润色成 SCI 论文风格：

我们的方法可以减少标注困难的问题，而且分割结果比较好，对小病灶也有帮助。
```

输出结构：

```text
## 润色后文本

The proposed method helps reduce the annotation burden in medical image segmentation and shows potential for improving the delineation of small lesions under the evaluated setting.

## 主要修改说明

1. 将口语化表达改为更正式的论文表达。
2. 将“比较好”改为更克制的证据边界表述。
3. 保留“小病灶”这一医学影像重点，但避免夸大临床效果。

## 需确认内容

- 需要补充具体数据集、指标和实验结果，才能写出更强的性能结论。
```

### 中译英

输入：

```text
请将以下中文段落翻译成适合 SCI 论文的英文表达，并给出术语表：

针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法。
```

输出结构：

```text
## English Translation

To address the large scale variations and complex backgrounds in remote sensing images, this study proposes a multi-scale feature fusion method.

## Terminology Choices

| 中文术语 | English Term | Note |
|---|---|---|
| 遥感图像 | remote sensing images | Standard term in remote sensing papers |
| 目标尺度变化 | scale variations | Keeps the technical meaning concise |
| 多尺度特征融合 | multi-scale feature fusion | Common expression in vision-related papers |

## Translation Notes

- The translation preserves the problem-method logic.
- No dataset, metric, or performance claim was added.
```

### 审稿回复

输入：

```text
请帮我回复审稿人意见，语气礼貌、专业、不要过度辩解：
Reviewer: The novelty of this method is unclear.
```

输出结构：

```text
## Reviewer Comment Summary

The reviewer asks for a clearer explanation of the method's novelty.

## Response Draft

Thank you for this constructive comment. We agree that the novelty of the proposed method should be described more explicitly. To address this concern, we propose revising the Introduction and Method sections to clarify the key design differences from existing approaches.

## Manuscript Revision Statement

We will revise Section X to better explain the motivation and technical contribution of the proposed design.

## Suggested Revised Text

[Please insert the method-specific novelty statement here.]
```

## 脚本使用

辅助脚本不依赖第三方库：

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py examples/terminology-check.md
python skills/academic-writing-assistant/scripts/structure_checker.py --section abstract examples/abstract-writing.md
python skills/academic-writing-assistant/scripts/skill_lint.py .
```

脚本说明：

- `terminology_checker.py`：扫描配置中的术语变体，报告可能的混用问题。
- `structure_checker.py`：检查摘要、引言、方法、实验、讨论等章节是否包含基本结构要素。
- `skill_lint.py`：检查仓库中的 Skill 文件、参考文件、README 结构和基本诚信护栏。

## 设计原则

1. 学术诚信优先：不编造文献、数据集、实验结果、作者、年份或不受支持的结论。
2. 技术含义保真：改善表达，但不改变用户原文的技术含义。
3. 领域自适应：根据研究领域调整术语、写作重点和谨慎程度。
4. 渐进披露：让 `SKILL.md` 保持简洁，把复杂规则放入 `references/`。
5. 结构化输出：不同任务使用不同输出模板。
6. 新手友好：说明修改理由、术语选择和需补充信息。

## 学术诚信

这个项目是学术表达辅助工具，不是论文代写或结果生成工具。

它必须避免：

- 虚构参考文献、作者、年份、期刊、会议或论文题目；
- 虚构数据集、实验、指标数值或消融结论；
- 夸大贡献、创新性、临床价值或部署能力；
- 改变用户提供内容的技术含义；
- 帮助规避学术诚信检查。

当证据不足时，Skill 应使用占位符或提示用户补充信息。

## 路线图

- `v0.1`：核心 Skill、任务路由、领域适配、诚信规则、README、示例和辅助脚本。
- `v0.2`：增强摘要、引言、相关工作、方法、实验和标题优化示例。
- `v0.3`：增强审稿回复、rebuttal、response letter 和投稿表达模板。
- `v0.4`：扩展医学影像、遥感、自然语言处理、机器人、生物信息学和材料科学领域包。
- `v1.0`：稳定 Skill 结构、完整示例库、人工评估集和贡献流程。

详见 [ROADMAP.md](ROADMAP.md)。

## 贡献指南

欢迎贡献：

- 新领域适配说明；
- 术语表和术语混用规则；
- 更安全的输出模板；
- 不含敏感信息的学术写作示例；
- 辅助脚本和测试。

提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。包含虚构文献、鼓励不受支持结论或削弱学术诚信护栏的贡献不会被接受。

## 许可证

本项目使用 MIT License。详见 [LICENSE](LICENSE)。

如果这个项目帮助你写出更清晰、更负责的学术论文，欢迎给它一个 Star，让更多科研作者发现它。
