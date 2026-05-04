<div align="center">

<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">

# Academic Writing Assistant

A field-adaptive academic writing Skill for Chinese and English research papers.

[中文](README.md) | **English**

</div>

## Positioning

`academic-writing-assistant` is an academic writing Skill / Plugin for researchers who need structured support for paper polishing, translation, expansion, paragraph merging, section drafting, reviewer response, title optimization, and terminology consistency while preserving academic integrity and technical meaning.

It is designed for graduate students, PhD candidates, early-career researchers, faculty members, and AI Agent users who want a reusable academic writing workflow.

## Why This Skill

Academic authors often move between Chinese research ideas, English manuscript language, field-specific terminology, and reviewer communication. A single prompt can help once, but it rarely provides stable task routing, field adaptation, output structure, and evidence boundaries.

This project organizes common academic writing needs into routable tasks, modular references, reusable output templates, and lightweight checking scripts so scholarly writing support becomes clearer, more maintainable, and more trustworthy.

## Core Features

| Feature | What it does |
|---|---|
| Task routing | Detects polishing, translation, expansion, merging, section drafting, reviewer response, and related tasks |
| Field adaptation | Adjusts writing emphasis, terminology, and caution level by research field |
| Academic polishing | Improves clarity, logic, grammar, and academic tone while preserving technical meaning |
| CN/EN translation | Supports Chinese-to-English and English-to-Chinese academic translation with terminology notes |
| Paper section drafting | Supports abstract, introduction, related work, method, experiment, discussion, and future work |
| Reviewer response | Drafts polite, specific, non-defensive responses and revision statements |
| Title optimization | Generates accurate, restrained, submission-ready title candidates |
| Terminology consistency | Detects mixed terminology and recommends consistent expressions |
| Integrity guardrails | Explicitly forbids fabricated citations, datasets, results, and unsupported claims |

## Supported Writing Tasks

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
- Discussion, Limitation, and Future Work Writing
- Reviewer Response Drafting
- Title Optimization
- Terminology Consistency Checking
- Academic Naturalization
- Prompt Optimization

## Supported Research Fields

| Field | Writing emphasis |
|---|---|
| Computer Vision | model architecture, feature representation, robustness, generalization, ablation studies |
| Artificial Intelligence | reasoning, planning, representation learning, multimodality, evaluation boundaries |
| Machine Learning | objectives, generalization, training stability, model complexity |
| Medical Imaging | clinical relevance, data heterogeneity, interpretability, external validation |
| Remote Sensing | spatial resolution, scale variation, multi-source fusion, geographic generalization |
| Natural Language Processing | semantic representation, context modeling, pre-trained models, data bias |
| Robotics | perception, planning, control, real-time performance, sensor fusion |
| Data Mining | pattern discovery, scalability, noise robustness, evaluation metrics |
| Bioinformatics | sample heterogeneity, statistical significance, biological interpretation |
| Materials Science | experimental conditions, structure-property relationships, characterization, reproducibility |

## Repository Structure

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

`SKILL.md` keeps the core purpose, trigger conditions, task entry points, and quality requirements. Detailed rules live under `references/` so agents can load them only when needed.

## Installation

### Install for Codex

Send this prompt to Codex:

```text
Install the Academic Writing Assistant Skill from https://github.com/LvvUP/academic-writing-assistant into my local Codex skills directory, then verify that $academic-writing-assistant can be invoked.
```

After installation, start a new Codex session and invoke:

```text
Use $academic-writing-assistant to polish this academic paragraph.
```

<details>
<summary>Manual fallback</summary>

```bash
git clone https://github.com/LvvUP/academic-writing-assistant.git
mkdir -p ~/.codex/skills
cp -R academic-writing-assistant/skills/academic-writing-assistant ~/.codex/skills/
```

If your Codex environment supports local plugins, you can also use `.codex-plugin/plugin.json` as the plugin manifest.

</details>

### Install for Claude Code

You can also ask Claude Code to install it for you:

```text
Install the Academic Writing Assistant Skill from https://github.com/LvvUP/academic-writing-assistant into my local Claude Code skills directory, then verify that $academic-writing-assistant can be invoked.
```

<details>
<summary>Manual fallback</summary>

```bash
git clone https://github.com/LvvUP/academic-writing-assistant.git
mkdir -p ~/.claude/skills
cp -R academic-writing-assistant/skills/academic-writing-assistant ~/.claude/skills/
```

</details>

After installation, start a new Claude Code session and invoke:

```text
Use $academic-writing-assistant to translate this Chinese academic paragraph into English.
```

### Install for Other Agents

If your agent supports a Skill directory, copy the whole directory:

```text
skills/academic-writing-assistant/
```

If your agent can read GitHub repositories, you can also give it this link:

```text
https://github.com/LvvUP/academic-writing-assistant
```

If your agent does not support Skills directly, use `skills/academic-writing-assistant/SKILL.md` as the main instruction and load files from `references/` when needed.

Do not copy only `scripts/`. The scripts are helper checks; task routing, field adaptation, and academic integrity rules live in `SKILL.md` and `references/`.

## Quick Examples

### Academic polishing

Input:

```text
I work on medical image segmentation. Please polish the following paragraph in SCI paper style:

Our method can reduce the problem of difficult annotation, and the segmentation results are relatively good. It is also helpful for small lesions.
```

Expected output structure:

```text
## Revised Text

The proposed method helps reduce the annotation burden in medical image segmentation and shows potential for improving the delineation of small lesions under the evaluated setting.

## Key Revision Notes

1. Replaced informal phrasing with academic expression.
2. Rewrote "relatively good" as an evidence-bounded claim.
3. Preserved the small-lesion focus while avoiding unsupported clinical overclaiming.

## Needs Confirmation

- Dataset names, metrics, and quantitative results are needed for stronger performance claims.
```

### Chinese-to-English translation

Input:

```text
Please translate the following Chinese paragraph into academic English suitable for an SCI paper and provide a terminology table:

针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法。
```

Expected output structure:

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

### Reviewer response

Input:

```text
Please help me respond to this reviewer comment politely and professionally:
Reviewer: The novelty of this method is unclear.
```

Expected output structure:

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

The helper scripts use only the Python standard library:

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py examples/terminology-check.md
python skills/academic-writing-assistant/scripts/structure_checker.py --section abstract examples/abstract-writing.md
python skills/academic-writing-assistant/scripts/skill_lint.py .
```

Scripts:

- `terminology_checker.py`: scans configured terminology variants and reports possible mixed usage.
- `structure_checker.py`: checks whether abstract, introduction, method, experiment, or discussion drafts include expected structural elements.
- `skill_lint.py`: checks Skill files, references, README structure, and basic integrity guardrails.

## Design Principles

1. Academic integrity first: no fake citations, datasets, experiments, authors, years, or unsupported results.
2. Meaning preservation: improve expression without changing technical meaning.
3. Field adaptation: adjust terms, writing emphasis, and caution level by research field.
4. Progressive disclosure: keep `SKILL.md` concise and place detailed rules in `references/`.
5. Structured output: use task-specific templates.
6. Beginner-friendly: explain revision choices, terminology decisions, and missing information.

## Academic Integrity

This project is an academic expression assistant, not a paper-writing or result-generation tool.

It must avoid:

- fabricated references, authors, years, venues, or paper titles;
- fabricated datasets, experiments, metric values, or ablation findings;
- exaggerated contribution, novelty, clinical relevance, or deployment readiness;
- changes to the technical meaning of user-provided content;
- assistance with evading academic integrity checks.

When evidence is missing, the Skill should use placeholders or ask the user to provide the missing information.

## Roadmap

- `v0.1`: core Skill, task routing, field adaptation, integrity rules, README, examples, and helper scripts.
- `v0.2`: richer examples for abstracts, introductions, related work, methods, experiments, and title optimization.
- `v0.3`: stronger reviewer response, rebuttal, response letter, and submission-language templates.
- `v0.4`: deeper field packs for medical imaging, remote sensing, NLP, robotics, bioinformatics, and materials science.
- `v1.0`: stable Skill structure, expanded example library, manual evaluation set, and contributor workflow.

See [ROADMAP.md](ROADMAP.md) for details.

## Contributing

Contributions are welcome, especially:

- new field adaptation notes;
- terminology maps and inconsistency rules;
- safer output templates;
- non-sensitive academic writing examples;
- helper scripts and tests.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Contributions that fabricate citations, encourage unsupported claims, or weaken academic integrity guardrails will not be accepted.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

If this project helps you write clearer and more responsible academic papers, consider giving it a Star so more researchers can discover it.
