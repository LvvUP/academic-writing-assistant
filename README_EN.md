<div align="center">

<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">

# Academic Writing Assistant

A field-adaptive academic writing Skill for Chinese and English research papers.

[中文](README.md) | **English**

</div>

## Positioning

`academic-writing-assistant` is an academic writing Skill / Plugin for researchers: polishing, Chinese-English translation, section drafting, reviewer responses and rebuttals, submission materials, and whole-draft consistency checking.

The problem it solves is not "make the prose flow better." Models already do that easily — and that is precisely the danger, because fluent prose quietly upgrades claims. "在部分数据集上有所改善" becomes "significantly outperforms existing methods," the author reads English better than anything they would have written, and ships it. By the time a reviewer catches it, the cost is already incurred.

So this Skill is built around being **aggressive on the surface and rigorous about the boundary**: which content may never be touched, which words change the science when you change them, and how an author can audit every edit in about a minute.

Built for graduate students, PhD candidates, early-career researchers, faculty, and AI Agent users who want a reusable academic writing workflow.

## The core mechanism: the fidelity contract

Read every sentence as three zones before editing. This is the single most useful habit in the Skill.

| Zone | Contents | Handling |
|---|---|---|
| **Locked** | Numbers, units, p-values, dataset and method names, citation markers, equations, symbols, cross-references, ethics approval numbers | Reproduce exactly. If something looks wrong, **flag it — never fix it**. You cannot see the data; the author can |
| **Load-bearing** | Hedges (may / suggests / demonstrates), quantifiers (all / some), scope conditions ("on the evaluated datasets"), causal verbs (causes vs. is associated with), novelty claims (first / SOTA / significantly) | Change only toward accuracy, and always disclose |
| **Free surface** | Grammar, articles, tense, sentence splitting, connectives, redundancy, word order, equal-strength synonyms | Edit confidently. This is where the value lives |

Every edit is tiered:

- **L1 surface** — grammar, articles, tense, spelling → reported as one aggregate line, not enumerated
- **L2 structure** — splitting, reordering, terminology normalization → one line of reasoning each
- **L3 claim** — touches load-bearing language → **never applied silently**; flagged with reasoning or left as a query

The reason for tiering is practical: an author who receives 40 undifferentiated changes accepts all of them without reading, because checking is too expensive. An author who receives "12 L1 + 3 L2 + 1 L3 needing your confirmation" actually reads the four that matter. Making the important changes cheap to find is the job.

## Core features

| Feature | What it does |
|---|---|
| Fidelity-preserving revision | Three zones, three change tiers, and a ledger the author can audit line by line |
| Task routing | Detects polishing, translation, expansion, merging, compression, section drafting, reviewer response |
| Field adaptation | Adjusts emphasis by field — specifically, **what that field's reviewers attack** |
| CN/EN translation | Both directions, with a terminology table and notes on non-obvious decisions |
| Section drafting | Abstract, introduction, related work, method, experiment, discussion, conclusion |
| Reviewer response | Separates journal response letters from conference rebuttals (different length, tense, structure) |
| Submission materials | Cover letters, highlights (85-character limit), AI-use disclosure, CRediT statements |
| LaTeX-aware editing | Edits `.tex` source directly, preserving `\cite{}`, `\ref{}`, math, and custom macros |
| Whole-draft consistency | Terminology, abbreviation first-use, symbols, tense, numbers, and claim strength across sections |
| Deterministic check scripts | Mechanically verify that citations, numbers, and equations survived a rewrite |
| Integrity guardrails | Forbids fabricated citations, datasets, results, and unsupported claims |

## What changed from the previous version

| | v0.1 | v0.2 |
|---|---|---|
| Change reporting | Revised text plus vague notes | L1/L2/L3 tiers with an auditable ledger |
| Claim protection | "Do not exaggerate" as a principle | Load-bearing vocabulary, a strength ladder, mandatory disclosure |
| Reviewer response | One template | Journal letter and conference rebuttal handled separately |
| Submission materials | None | Cover letter, highlights, AI disclosure, CRediT |
| LaTeX | None | Dedicated source-editing rules and preservation checking |
| Whole-draft checks | None | Terminology, abbreviations, symbols, tense, claim consistency |
| Scripts | Keyword bingo | Citation/number preservation, abbreviation first-use, venue limits |
| Field adaptation | Terms and emphasis | **What reviewers in that field actually attack** |

## Supported Writing Tasks

Polishing · Expansion · Merging · Compression to a limit · CN→EN · EN→CN · Abstract · Introduction · Related work · Method · Experiment · Discussion and limitations · Conclusion · Journal response letter · Conference rebuttal · Cover letter · Highlights · AI disclosure · Title optimization · Contribution statements · Terminology consistency · Whole-draft consistency · Naturalization · Prompt optimization

## Supported Research Fields

Built-in Field Adapters cover: computer vision, machine learning and AI, NLP and LLMs, medical imaging and clinical research, remote sensing, robotics, data mining and recommendation, bioinformatics, materials science and chemistry, and the social sciences.

Each adapter records not a vocabulary list but **what reviewers in that field actually attack** — remote sensing reviewers ask about geographic generalization, clinical reviewers about external validation, NLP reviewers about data contamination. Writing that anticipates the field's characteristic objection is the difference between a defensible paper and a major revision.

The list above is **not a limit on what the Skill supports**. Unlisted fields use the same general academic writing workflow: identify the task, preserve technical meaning, keep evidence boundaries clear, maintain terminology consistency, and adapt to the context you provide. Supply your field, target venue style, and key terminology when asking. Where information is missing, the Skill uses placeholders or asks — it does not invent field facts.

## Repository structure

```text
academic-writing-assistant/
├── .codex-plugin/plugin.json
├── assets/logo/
├── skills/academic-writing-assistant/
│   ├── SKILL.md                    # Fidelity contract, routing, output contract, integrity
│   ├── references/                 # Loaded on demand
│   │   ├── fidelity-protocol.md    # The three zones and tiers, with worked examples
│   │   ├── writing-workflows.md    # How to execute each task
│   │   ├── reviewer-response.md    # Journal letter vs. conference rebuttal
│   │   ├── submission-package.md   # Cover letter, highlights, AI disclosure
│   │   ├── latex-and-formats.md    # LaTeX, Word, Markdown handling
│   │   ├── consistency-pass.md     # Whole-draft consistency
│   │   ├── field-adapter.md        # What reviewers attack, by field
│   │   ├── style-guide-zh.md       # Chinese academic register
│   │   ├── style-guide-en.md       # English register and CN-interference patterns
│   │   ├── task-router.md          # Task identification and requests to redirect
│   │   ├── output-templates.md     # Response shapes
│   │   ├── quality-checklist.md    # Pre-send checks
│   │   ├── citation-safety.md      # Citation and evidence boundaries
│   │   ├── terminology.md          # CN↔EN term selection and consistency
│   │   └── examples.md             # End-to-end worked examples
│   ├── assets/terminology-map.zh-en.json
│   └── scripts/                    # Deterministic checks
├── examples/  ├── tests/  ├── docs/  ├── evals/
├── README.md  ├── README_EN.md  └── LICENSE
```

`SKILL.md` holds the core mechanism and routing; detailed rules live in `references/` so agents load only what they need.

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

You can also ask Claude Code to install it:

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

If your agent can read GitHub repositories, give it this link:

```text
https://github.com/LvvUP/academic-writing-assistant
```

If your agent does not support Skills, use `SKILL.md` as the main instruction and load files from `references/` as needed.

Do not copy only `scripts/`. The scripts perform mechanical checks; the fidelity rules, task routing, and integrity boundaries live in `SKILL.md` and `references/`.

## Quick Examples

### Polishing — what the change ledger looks like

Input:

```text
I work on medical image segmentation. Polish this for an SCI paper:
Our method can reduce the annotation difficulty, the segmentation results are
relatively good, it helps with small lesions, and it clearly outperforms
existing methods.
```

Example output:

#### Revised text

```text
The proposed method reduces the annotation burden in medical image segmentation
and improves the delineation of small lesions compared with the evaluated
baselines. [please add the datasets, metrics, and values]
```

#### Change ledger

L1 (grammar/articles/tense): 4 changes, not enumerated.

| # | Original | Revised | Tier | Reason |
|---|---|---|---|---|
| 1 | relatively good | improves the delineation ... compared with the evaluated baselines | L3 | No comparison target; English papers need to name what the comparison is against |
| 2 | clearly outperforms existing methods | compared with the evaluated baselines | L3 | "Clearly/significantly" reads as a statistical significance claim. If a test was run, tell me the method and p-value and this can be restored |

#### Needs confirmation

- Which datasets and metrics (Dice / IoU / HD95)?
- Which specific baselines? Naming them substantially reduces the chance a reviewer challenges the fairness of the comparison.
- Is the annotation-burden reduction quantified (time, pixels, or number of labeled samples)?

Note that **no Dice score was invented** to complete the sentence — missing information appears as a placeholder, and both L3 entries explain how to revert.

### CN→EN — it tells you which sentence should not be translated literally

Input:

```text
Translate for an SCI paper: 针对遥感图像中目标尺度变化大、背景复杂的问题，
本文提出一种多尺度特征融合方法，具有重要的理论意义和应用价值。
```

Example output:

#### English Translation

```text
To address the large scale variation and complex backgrounds in remote sensing
images, this study proposes a multi-scale feature fusion method.
```

#### Terminology choices

| Chinese | English | Note |
|---|---|---|
| 遥感图像 | remote sensing images | Standard term in the field |
| 目标尺度变化 | scale variation | More idiomatic than "target scale change" |
| 多尺度特征融合 | multi-scale feature fusion | Conventional; not "feature merging" |

#### Translation notes

- Dropped 具有重要的理论意义和应用价值 (L3). This is conventional closing framing in Chinese papers, but translated literally as "has important theoretical significance and application value" it reads in English as an unsupported grand claim. If you want to keep the point, state the specific implication instead.

### Conference rebuttal — handled differently from a journal letter

Input:

```text
An ICLR reviewer wrote "The improvement over baselines is marginal and may be
within noise." We ran 5 seeds: mean improvement 2.1 points, std 0.3.
```

Example output:

```text
**Marginal improvement / noise (R2).** We report results over 5 seeds: the
proposed method improves by 2.1 points on average (std 0.3), while the baseline's
own seed variance is [please fill in the baseline's std]. The gap therefore
exceeds the run-to-run variation by a substantial margin. We will add per-seed
results and variance to Table 2 in the revision.
```

With the note: add the baseline's seed variance — it is the most direct evidence against the "within noise" objection, and reporting only your own method's variance does not fully answer it.

## Scripts

Standard library only, no third-party dependencies. They handle what models do unreliably and machines do exactly.

```bash
# After a rewrite: did any citation, number, equation, or macro get lost?
python skills/academic-writing-assistant/scripts/fidelity_check.py \
    --before original.tex --after revised.tex

# Whole-draft hygiene: abbreviations used before definition, terminology drift,
# unearned "significant", tense mixing, word limits
python skills/academic-writing-assistant/scripts/manuscript_audit.py draft.md \
    --section abstract --limit-words 250

# Per-line character counts for highlights (Elsevier: 85 including spaces)
python skills/academic-writing-assistant/scripts/manuscript_audit.py highlights.txt \
    --limit-chars 85 --per-line

# Chinese terminology variants
python skills/academic-writing-assistant/scripts/terminology_checker.py draft.md

# Section structural elements
python skills/academic-writing-assistant/scripts/structure_checker.py \
    --section experiment draft.md
```

`fidelity_check.py` is the one to run by default. Its output is evidence rather than reassurance: it names exactly which protected items changed. A dropped `\cite{}` compiles cleanly and reads normally, but it means an uncited claim — exactly the failure that re-reading misses and a script catches.

See [docs/scripts.md](docs/scripts.md) for details.

## Design principles

1. **Fidelity before fluency.** Improve the expression; never move the evidence boundary.
2. **Auditable changes.** Tiered reporting makes the important edits easy to find — a ledger too long to read is no ledger at all.
3. **Deterministic work goes to scripts.** Citation and number preservation is verified, not trusted.
4. **Field adaptation is a reviewer's perspective.** Knowing what a field asks is more useful than knowing its vocabulary.
5. **Progressive disclosure.** Keep `SKILL.md` lean; complex rules live in `references/`.
6. **Proportionate ceremony.** A one-line fix does not need a table.

## Academic Integrity

This is an academic expression assistant, not a paper-writing or result-generation tool.

It must avoid:

- fabricated references, authors, years, venues, titles, DOIs, or arXiv IDs;
- fabricated datasets, sample sizes, metric values, ablation findings, statistical tests, or p-values;
- fabricated ethics approvals, registration numbers, or funding numbers;
- claiming an experiment was run or a revision was made, unless the author said so;
- exaggerated contribution, novelty, clinical relevance, or deployment readiness;
- changes to the technical meaning of user-provided content;
- assistance with evading academic integrity checks.

Where evidence is missing, it writes a **conspicuous placeholder** — `[please add the main quantitative results]` — rather than plausible invention. A placeholder is a service; a plausible invention is a landmine.

On "reduce my AI detection score" requests: the Skill does not rewrite against a detector's score, since those tools are unreliable in both directions. It addresses the real underlying problem instead — text flagged as machine-generated usually is uniform in sentence length, evenly weighted, vague, and hedge-heavy, and fixing that is simply better academic writing.

On AI disclosure: most publishers now require disclosure of substantive generative-AI use. Elsevier asks for a dedicated section before the references; ICLR treats undisclosed substantive LLM use as a Code of Ethics violation. Language polishing is commonly exempt, but thresholds differ by venue. `references/submission-package.md` provides a disclosure template and the current landscape — confirm against your target venue's own author guide.

## Roadmap

- `v0.1`: core Skill, task routing, field adaptation, integrity rules, examples, helper scripts.
- `v0.2` (current): fidelity contract and change tiers, journal/conference response separation, submission materials, LaTeX-aware editing, whole-draft consistency, deterministic check scripts.
- `v0.3`: reviewer attack patterns for more disciplines, figure/table/equation conventions, thesis chapter support.
- `v0.4`: terminology expansion and community-contributed field packs.
- `v1.0`: stable structure, expanded example library, evaluation set, contributor workflow.

See [ROADMAP.md](ROADMAP.md).

## Contributing

Contributions are welcome, especially:

- reviewer attack patterns and writing emphasis for new fields;
- terminology maps and inconsistency rules;
- safer output templates;
- non-sensitive academic writing examples;
- scripts and tests.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Contributions that fabricate citations, encourage unsupported claims, or weaken integrity guardrails will not be accepted.

## License

Released under the MIT License. See [LICENSE](LICENSE).

If this project helps you write clearer and more responsible academic papers, consider giving it a Star so more researchers can find it.
