# Academic Writing Assistant

> A field-adaptive academic writing Skill for researchers who need clearer, more rigorous, and more trustworthy scholarly writing support.

面向中文科研作者的学术写作 Skill，支持中文与英文论文的润色、翻译、扩写、合并、摘要/引言/相关工作/方法/实验部分撰写、审稿回复、标题优化与术语一致性检查。

## 项目定位

`academic-writing-assistant` 不是一组零散 Prompt，而是一个可复用、可维护、可扩展的 Codex Skill / Plugin 项目。

它的目标是帮助中文科研作者在不牺牲学术诚信的前提下，更高效地完成论文表达层面的工作：让句子更清楚，让逻辑更连贯，让术语更一致，让中英文表达更符合学术语境。

适合：

- 研究生、博士生、青年教师和科研作者；
- 正在撰写中文论文、英文论文、SCI 论文或会议论文的作者；
- 需要将中文研究内容翻译成英文论文表达的作者；
- 需要组织摘要、引言、相关工作、方法、实验或审稿回复的作者；
- 希望把学术写作支持做成结构化 Skill 的 AI agent 用户。

## 为什么需要

很多学术写作提示词能处理单次任务，但很难稳定复用：

- 用户需要自己判断该用哪个 Prompt；
- 不同任务的输出格式不一致；
- 缺少跨学科领域适配；
- 容易把推测写成事实；
- 容易编造文献、数据集、实验结果或贡献；
- 难以覆盖从初稿、翻译、结构组织到审稿回复的完整流程。

这个项目把常见学术写作需求拆成可路由的任务、可按需加载的参考文件、可检查的输出模板和轻量脚本，让 Skill 更像一个可维护的开源工具。

## 核心功能

| Capability | What it does |
|---|---|
| Task routing | 自动识别润色、翻译、扩写、合并、章节写作、审稿回复等任务 |
| Field adaptation | 根据领域调整写作重点、术语和谨慎程度 |
| Academic polishing | 提升清晰度、逻辑、语法和学术语气，同时保持技术含义 |
| CN/EN translation | 支持中英文学术翻译，附术语表和译法说明 |
| Paper section drafting | 支持 Abstract、Introduction、Related Work、Method、Experiment、Discussion 等章节 |
| Reviewer response | 起草礼貌、具体、非防御性的审稿回复 |
| Title optimization | 生成多个克制、准确、可投稿的标题候选 |
| Terminology consistency | 检查术语混用并建议统一表达 |
| Integrity guardrails | 明确禁止虚构文献、数据集、实验结果和不受支持的结论 |

## 支持的学术写作任务

- Academic Polishing
- Academic Expansion
- Paragraph Merging
- Chinese-to-English Academic Translation
- English-to-Chinese Academic Translation
- Abstract Writing
- Introduction Writing
- Related Work Organization
- Method Section Writing
- Experiment Section Writing
- Discussion / Limitation / Future Work Writing
- Reviewer Response Drafting
- Title Optimization
- Terminology Consistency Checking
- Academic Naturalization
- Prompt Optimization

## 支持的研究领域

| Field | Writing emphasis |
|---|---|
| Computer Vision | 模型结构、特征表示、鲁棒性、泛化、消融实验 |
| Artificial Intelligence | 推理、规划、表征学习、多模态、评估边界 |
| Machine Learning | 优化目标、泛化能力、训练稳定性、模型复杂度 |
| Medical Imaging | 临床相关性、数据异质性、可解释性、外部验证 |
| Remote Sensing | 空间分辨率、尺度变化、多源融合、地理泛化 |
| Natural Language Processing | 语义表征、上下文建模、预训练模型、数据偏差 |
| Robotics | 感知、规划、控制、实时性、传感器融合 |
| Data Mining | 模式发现、可扩展性、噪声鲁棒性、评估指标 |
| Bioinformatics | 样本异质性、统计显著性、生物学解释 |
| Materials Science | 实验条件、结构-性能关系、表征方法、可重复性 |

## 目录结构

```text
academic-writing-assistant/
├── .codex-plugin/plugin.json
├── skills/academic-writing-assistant/
│   ├── SKILL.md
│   ├── references/
│   ├── assets/terminology-map.zh-en.json
│   └── scripts/
├── examples/
├── tests/
├── docs/
├── evals/
├── AGENTS.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── CHANGELOG.md
└── LICENSE
```

`SKILL.md` 只保留核心触发条件、原则和任务入口；复杂说明放在 `references/` 下，便于 agent 按需读取。

## 安装

### 方式一：作为 Skill 使用

将 `skills/academic-writing-assistant` 复制到你的 agent 环境支持的本地 skills 目录中，然后用 `$academic-writing-assistant` 或自然语言触发。

### 方式二：作为 Codex Plugin 使用

本仓库包含 `.codex-plugin/plugin.json`，可在支持 Codex plugin 的环境中作为本地插件使用。插件 manifest 已指向 `LvvUP/academic-writing-assistant`。

## Quick Examples

### 1. Academic polishing

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
2. 将“比较好”改为更克制的 evidence-bounded 表述。
3. 保留“小病灶”这一医学影像重点，但避免夸大临床效果。

## 需确认内容

- 需要补充具体数据集、指标和实验结果，才能写出更强的性能结论。
```

### 2. Chinese to English academic translation

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

### 3. Reviewer response

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

## Script Usage

The helper scripts are optional and dependency-free.

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py examples/terminology-check.md
python skills/academic-writing-assistant/scripts/structure_checker.py --section abstract examples/abstract-writing.md
python skills/academic-writing-assistant/scripts/skill_lint.py .
```

What they do:

- `terminology_checker.py`: scans configured terminology variants and reports possible mixed usage.
- `structure_checker.py`: checks whether a draft section contains expected structural elements.
- `skill_lint.py`: checks repository-level Skill files, references, README sections, and basic integrity guardrails.

## 设计原则

1. **Academic integrity first**: no fake citations, datasets, experiments, authors, years, or unsupported results.
2. **Meaning preservation**: improve expression without changing technical meaning.
3. **Field adaptation**: adapt terms and writing emphasis to the research field.
4. **Progressive disclosure**: keep `SKILL.md` concise and move detailed rules into references.
5. **Structured output**: use task-specific templates instead of unstructured rewrites.
6. **Beginner-friendly**: explain changes, terminology choices, and missing information.

## Academic Integrity

This project is designed as an academic expression assistant, not a paper-writing shortcut.

It must not:

- fabricate references, authors, years, venues, or paper titles;
- fabricate datasets, experiments, metric values, or ablation findings;
- exaggerate contribution, novelty, clinical relevance, or deployment readiness;
- change the technical meaning of user-provided content;
- provide rewriting whose purpose is to escape academic responsibility.

When evidence is missing, the Skill should use placeholders or ask the user to provide the missing information.

## Roadmap

- **v0.1**: core Skill, task routing, field adaptation, integrity rules, README, examples, helper scripts.
- **v0.2**: richer paper-section workflows, more title and prompt optimization examples.
- **v0.3**: reviewer response, rebuttal, cover letter, and submission-style templates.
- **v0.4**: deeper field packs for medical imaging, remote sensing, NLP, robotics, bioinformatics, and materials science.
- **v1.0**: stable Skill schema, broader examples, manual evaluation set, and contributor workflow.

See [ROADMAP.md](ROADMAP.md) for the detailed plan.

## Contributing

Contributions are welcome, especially:

- new field adaptation notes;
- terminology map improvements;
- safer output templates;
- examples for real academic workflows using non-sensitive sample text;
- tests for helper scripts and repository checks.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Contributions that fabricate references, encourage unsupported claims, or weaken academic integrity guardrails will not be accepted.

## License

MIT License. See [LICENSE](LICENSE).

If this project helps you write clearer and more responsible academic papers, consider giving it a star. It helps more researchers discover the project.
