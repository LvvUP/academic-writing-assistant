<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass.png">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass: pages, revision lines and a check mark" width="112">
</picture>

# Academic Writing Assistant

**Clearer research writing, from draft to submission.**

A Chinese–English academic writing Skill for manuscript polishing, translation, section drafting, reviewer responses and submission materials.

[中文](README.md) · **English**

[Writing examples](#writing-examples) · [Supported tasks](#supported-tasks) · [Installation](#installation)

</div>

## Writing examples

These writing examples are synthetic; data and citation keys are for demonstration.

### Manuscript polishing: connect the setup, results and conclusion

**Original draft**

> To see the effect of the fusion module, we did an ablation experiment, the training settings were the same and the same test set was used. After taking out the fusion module, Dice went from 86.4% to 83.1%, and for small lesions (diameter < 10 mm), it went from 78.2% to 72.6%. These results support that the fusion module is helpful for segmentation on this test set, see Table 3.

**Polished text**

> We evaluated the contribution of the fusion module through an ablation study using the same training settings and test set. Removing the module reduced Dice from 86.4% to 83.1%; for small lesions (diameter < 10 mm), Dice decreased from 78.2% to 72.6% (Table 3). These results support the module's contribution to segmentation performance on this test set.

**Editorial note:** The revision establishes the setup, presents the two results in parallel, then states the conclusion. The values, small-lesion definition and table reference stay intact, and the conclusion remains specific to this test set.

<details>
<summary><strong>CN→EN: make the training setup, comparison and results easy to follow</strong></summary>

**Chinese source**

> 为减轻季节变化对土地覆盖分类的影响，我们把来自春季和秋季的影像拿来联合训练，并沿用已有的多尺度融合模块 `\cite{demo_fusion}`。联合训练模型的宏平均 F1 为 0.81，只用春季影像训练的模型是 0.76。两个模型都在北部研究区的同一批秋季测试影像上评估。

**English translation**

> To reduce the effect of seasonal variation on land cover classification, we jointly trained the model on spring and autumn imagery using the existing multi-scale fusion module `\cite{demo_fusion}`. Both models were evaluated on the same autumn test images from the northern study area. The model trained on both seasons achieved a macro-F1 score of 0.81, compared with 0.76 for the model trained only on spring imagery.

**Translation note:** Moving the evaluation setup before the results clarifies the comparison between training settings. The translation uses land cover classification and macro-F1 consistently, keeping the citation key, values and evaluation region aligned.

</details>

<details>
<summary><strong>Reviewer response: answer a latency concern with completed additional results</strong></summary>

**Reviewer comment**

> The accuracy gain may come at the cost of higher inference latency.

**Author material**

> We agree that inference overhead needs to be quantified. We have measured inference latency on the same GPU, with batch size = 1 and the same input resolution: 18 ms per image for the baseline and 21 ms per image for our method. Their accuracies are 84.2% and 86.1%, respectively. We have added these results to Table 4 of the revised manuscript and discussed the accuracy–latency trade-off in Section 5.2. Please draft an English journal response.

**Response draft**

> Thank you for raising this point. We have quantified the accuracy–latency trade-off on the same GPU, with a batch size of 1 and the same input resolution. Our method achieves an accuracy of 86.1% at 21 ms per image, compared with 84.2% at 18 ms per image for the baseline. The gain in accuracy comes with higher latency. We have added these results to Table 4 and a discussion of the trade-off to Section 5.2 of the revised manuscript.

**Structure:** Address the concern, present comparable results, then point to the completed changes. Each value stays attached to its method; the table, section and completion status all come from the author material.

</details>

[Explore more writing examples →](examples/)

## Supported tasks

| What you are working on | What the Skill can help with |
|---|---|
| Manuscript revision | Chinese and English polishing, expansion, paragraph merging, shortening and titles |
| Chinese–English translation | Both directions, terminology pairs and explanations of important translation choices |
| Section drafting | Abstract, introduction, related work, methods, results, discussion and conclusion from supplied material |
| Peer review | Journal response letters, conference rebuttals, evidence and revision locations |
| Submission materials | Cover letters, Highlights, AI-use disclosures and CRediT contribution statements |
| Long drafts and LaTeX | Terminology, abbreviations, symbols and claims across sections; citation, equation and cross-reference preservation |

### Fields and research types

Built-in field adapters cover computer vision, machine learning and AI, NLP and LLMs, medical imaging and clinical research, remote sensing, robotics, data mining and recommendation, bioinformatics, materials science and chemistry, and social sciences, education and management.

Writing priorities follow the research context: validation scope in medical imaging, regional and sensor conditions in remote sensing, and comparison settings and experimental variation in machine learning. Theoretical proofs, qualitative research and reviews have their own organizational guidance. For other fields, provide your research context, study type and key terminology so the Skill can follow your conventions.

## A repeatable academic writing workflow

Give your Agent reusable writing rules that it can apply to each task:

- **Follow field conventions.** Adapt terminology, information order and emphasis to the discipline, section and research type.
- **Preserve research facts.** Attend to values, citations, equations and claim scope while improving sentences, keeping the prose aligned with the supplied evidence.
- **Explain important changes.** Return usable text first, then explain structural edits and changes affecting claims so the author can decide what to adopt.
- **Match the depth to the task.** A one-line correction can return just the revised text; a standard revision includes essential notes; a long-draft review focuses on consistency and connections across sections and sources.

Read the complete [writing guidelines and academic integrity principles](skills/academic-writing-assistant/SKILL.md).

## Installation

### Codex

Run these commands in a terminal with **Python 3.9+**:

```sh
git clone --branch main https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host codex --home-root "$HOME"
```

The Skill installs to `~/.agents/skills/academic-writing-assistant`. Refresh the Skill list or start a new session, then enter this in Codex:

```text
$academic-writing-assistant
Polish the paragraph below for clearer organization. Preserve values, citations
and claim scope, and explain important changes.

[Paste your paragraph]
```

### Claude Code

After cloning the repository as above, run this from its directory:

```sh
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

The Skill installs to `~/.claude/skills/academic-writing-assistant`. Start a new session and use the slash command:

```text
/academic-writing-assistant
Translate the Chinese paragraph below into English. Preserve values, citations
and terminology meanings, and explain important translation choices.

[Paste your paragraph]
```

<details>
<summary><strong>Cursor, Grok Build and other Agents</strong></summary>

After cloning the repository, choose the installation command for your host:

```sh
# Cursor
python3 -B scripts/install_skill.py install --host cursor --home-root "$HOME"

# Official Grok Build coding agent
python3 -B scripts/install_skill.py install --host grok-build --home-root "$HOME"
```

- **Cursor:** installs to `~/.cursor/skills/academic-writing-assistant`; type `/` in Agent and select the Skill.
- **Grok Build:** installs to `~/.grok/skills/academic-writing-assistant`; invoke `/academic-writing-assistant`.
- **Other Agents:** load the complete `skills/academic-writing-assistant/` directory, using `SKILL.md` as the main instruction and reading files in `references/` for the current task.

Core text use requires a host that can load instructions. File parsing, retrieval and script execution use the capabilities supplied by the host. See [compatibility notes](docs/compatibility.md) for host directories, project installation and plugin options.

</details>

For an existing installation, see [installation, updates and troubleshooting](docs/installation.md).

## Documentation and contributions

- [More examples](examples/) · [FAQ](docs/faq.md) · [Research-type examples](examples/research-types.md)
- [Manuscript checks](docs/scripts.md): `fidelity_check.py` compares values, citations and equations; `manuscript_audit.py` checks abbreviations and length.
- [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Roadmap](ROADMAP.md)

Contributions of field terminology, writing guidance and synthetic examples are welcome. If this Skill helps with your manuscripts, give the repository a **Star** so more researchers can find it.

License: **AGPL-3.0-only**. See [LICENSE](LICENSE).
