<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass-dark.svg">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass: pages, revision lines and a check mark" width="120">
</picture>

# Academic Writing Assistant

### Let AI edit your paper without editing your data or conclusions

A **discipline-agnostic academic writing Skill** for Chinese and English manuscripts: polishing · CN↔EN translation · section drafting · theses and grant proposals · reviewer responses · submission materials<br>
Works across the sciences, engineering, medicine, economics, social sciences, humanities and law — one Skill for Claude Code, Codex, Cursor, Grok Build, WorkBuddy and other AI agents.

[![Version](https://img.shields.io/badge/version-0.4.0-2563EB)](CHANGELOG.md)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-2563EB)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-111827)](https://agentskills.io)
[![GitHub stars](https://img.shields.io/github/stars/LvvUP/academic-writing-assistant?style=social)](https://github.com/LvvUP/academic-writing-assistant/stargazers)

[中文](README.md) · **English**

[Install](#-install) · [Examples](#-examples) · [Features](#-features) · [Disciplines](#-disciplines) · [FAQ](#-faq)

</div>

---

## 💡 Why

Grammar and fluency are rarely the problem when AI edits a paper. The danger is edits that **read better but quietly change the facts**:

| You wrote | Typical AI "polish" | Problem |
|---|---|---|
| The method **may** improve performance **in some settings** | The method significantly improves performance | Hedges removed, claim inflated |
| A is **associated with** B | A **causes** B | Correlation becomes causation |
| Accuracy 92.3% | Accuracy 93.2% | Number changed |
| (no citation) | …(Smith et al., 2021) | Fabricated reference |
| We **plan to** run a survey | We ran a survey | Plan becomes result |

Academic Writing Assistant gives your agent a **fidelity contract**: improve the language freely, but never move the facts or the evidence boundary — and list every change to claim strength so you decide whether to accept it.

## 🚀 Install

### Option 1: paste a prompt into your AI agent (recommended)

Send this to Claude Code, Codex, Cursor, Grok Build, WorkBuddy or any agent that supports Skills:

```text
Please install (or update, if already installed) the academic writing Skill "academic-writing-assistant".
Source: https://github.com/LvvUP/academic-writing-assistant (main branch). I only need its skills/academic-writing-assistant/ folder.
1. Work out which agent you are running in and find its user-level skills directory (on Windows, ~ = %USERPROFILE%). Hints:
   Claude Code ~/.claude/skills · Codex ~/.agents/skills · Cursor ~/.cursor/skills · Grok Build ~/.grok/skills
   WorkBuddy ~/.workbuddy/skills or ~/.codebuddy/skills (whichever you actually load) · Gemini CLI ~/.gemini/skills · GitHub Copilot ~/.copilot/skills
   For other agents follow their official docs (most read ~/.agents/skills). If unsure, ask me; don't guess.
2. Shallow-clone (git clone --depth 1) or download the ZIP into a temp directory, then copy that whole folder to "<skills dir>/academic-writing-assistant/", keeping the folder name. Don't run any script from the repo and don't use sudo.
3. If a skill with the same name already exists in the target or in any other skills directory you load, tell me its version, move the old folder to a backup outside every skills directory, then put the new one in place, so there are never two copies.
4. Afterwards confirm SKILL.md exists, delete the temp directory, and tell me the install path, version, whether I need to restart or open a new session, and how to invoke it.
```

The agent works out which platform it is running on and puts the Skill in the right place. Send the same prompt again whenever you want to update.

<details>
<summary><strong>Option 2: command line</strong></summary>

**One command for many agents** (requires Node.js; uses the open-source [skills](https://github.com/vercel-labs/skills) CLI and lets you pick which agents to install for):

```sh
npx skills add LvvUP/academic-writing-assistant -g
```

**Bundled installer** (Python 3.9+; supports safe update and uninstall):

```sh
git clone https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

`--host` accepts `claude`, `codex`, `cursor`, `grok-build`, `workbuddy`, `codebuddy`, `gemini`, `copilot`, `opencode`, `trae`, `trae-cn`, `qoder`, `kiro` and `windsurf`.

**Manual:** copy the whole `skills/academic-writing-assistant/` folder into your agent's skills directory.

See [compatibility](docs/compatibility.md) for each agent's directory and invocation, and the [installation guide](docs/installation.md) for update and uninstall.

</details>

### Usage

Open a new session and describe your writing task in plain language — the agent loads the Skill automatically. You can also invoke it explicitly:

```text
/academic-writing-assistant Please polish this abstract, keep all numbers, citations and the scope of conclusions, and list important changes.

[paste your text]
```

> Most agents use `/academic-writing-assistant`; Codex uses `$academic-writing-assistant`. You can also just describe your writing task.

## ✨ Examples

> All examples are synthetic; data and citations are for demonstration only.

### Polishing: informal wording and a causal overclaim (social science)

**Original (Chinese)**

> 我们对 412 名大学生做了问卷调查，结果发现每天刷短视频的时间越长，学习投入就越低（r = −0.29，p < 0.001）。这说明刷短视频会严重影响大学生的学习，学校应该采取措施进行干预。

*(We surveyed 412 students and found that the longer they spent on short videos each day, the lower their study engagement. This shows short videos seriously harm students' learning, and schools should intervene.)*

**Polished**

> 本研究对 412 名大学生开展问卷调查，发现每日短视频使用时长与学习投入呈负相关（r = −0.29，p < 0.001）。[干预建议：请补充支持因果关系或干预效果的依据后再写入。]

**Important changes**

| Original | Revised | Tier | Reason |
|---|---|---|---|
| seriously harm students' learning | negatively correlated with study engagement | L3 claim | A survey correlation supports "associated", not "harm" or "seriously" |
| schools should intervene | placeholder | L3 claim | The recommendation depends on a causal claim; restore it as a conditional suggestion if causal or intervention evidence is supplied |

<details>
<summary><strong>CN→EN translation: an observational study does not "reduce risk" (medicine)</strong></summary>

**Chinese source**

> 在这项回顾性队列研究中，我们纳入了 2018—2022 年间在本院就诊的 1,236 名 2 型糖尿病患者。与未使用该药物的患者相比，使用该药物的患者心血管事件风险较低（HR = 0.78，95% CI 0.64–0.95），但这一关联在 65 岁及以上患者中不明显。

**English translation**

> In this retrospective cohort study, we included 1,236 patients with type 2 diabetes who attended our hospital between 2018 and 2022. Compared with non-users, patients who used the drug had a lower risk of cardiovascular events (HR = 0.78, 95% CI 0.64–0.95), although this association was not evident in patients aged 65 years or older.

**Translation notes:** 风险较低 becomes *had a lower risk*, not *reduced the risk*, because a cohort study supports an association; 不明显 becomes *not evident*, not *no effect*. Numbers, the confidence interval and the age threshold map one-to-one.

</details>

<details>
<summary><strong>Reviewer response: only state revisions the author has completed (computer science)</strong></summary>

**Reviewer comment**

> The accuracy gain may come at the cost of higher inference latency.

**Author notes (Chinese)**

> 已在同一张 GPU、batch size = 1、相同输入分辨率下测量推理延迟：baseline 为 18 ms/图像，我们的方法为 21 ms/图像；准确率分别为 84.2% 和 86.1%。已将结果补入修订稿表 4，并在第 5.2 节补充权衡讨论。

**Draft response**

> Thank you for raising this point. We have quantified the accuracy–latency trade-off on the same GPU, with a batch size of 1 and the same input resolution. Our method achieves an accuracy of 86.1% at 21 ms per image, compared with 84.2% at 18 ms per image for the baseline. The gain in accuracy comes with higher latency. We have added these results to Table 4 and a discussion of the trade-off to Section 5.2 of the revised manuscript.

**Structure:** answer the concern, give comparable results, then point to completed revisions. Table and section numbers and completion status all come from the author's notes; no new experiments are promised on the author's behalf.

</details>

[More examples →](examples/)

## 📋 Features

| What you're doing | What the Skill handles |
|---|---|
| ✍️ Revising | Chinese and English polishing, expansion, merging, compression to a limit, titles and contributions |
| 🌐 Translating | CN→EN and EN→CN with terminology notes; LaTeX and citations preserved |
| 📄 Drafting | Abstract, introduction, related work, methods, results, discussion and conclusion from your material |
| 🎓 Theses and proposals | Thesis chapters, bilingual abstracts, research proposals and grant applications |
| 💬 Responding to reviewers | Journal response letters and conference rebuttals that separate completed revisions from plans |
| 📮 Submitting | Cover letters, highlights, AI-use statements, CRediT statements |
| 📚 References and formats | Reference lists in GB/T 7714, APA and other styles; LaTeX citations, math and cross-references kept intact |
| 🔍 Whole-draft checks | Consistency of terms, abbreviations, symbols, numbers and claims across sections |

## 🧭 Disciplines

Built-in writing guidance for 12 discipline families; anything else follows a general procedure that respects your field's conventions and structure:

> Humanities · Law · Economics & management · Social sciences · Education & psychology · Medicine & public health · Life sciences & agriculture · Physics, chemistry & materials · Mathematics & statistics · Earth & environmental sciences · Engineering · Computer science & AI

Research types are handled on their own terms too: experimental, survey and econometric, qualitative, theoretical, review, humanities and legal interpretation, case study and design research. A history paper will not be asked for an "experimental setup", and interview themes will not become population percentages.

## 🛡️ The fidelity contract

| Zone | Includes | Handling |
|---|---|---|
| 🔒 **Locked** | Numbers, units, p-values, citations, formulas, statutes, direct quotations, ethics IDs… | Kept verbatim; suspected errors are flagged, never silently "fixed" |
| ⚖️ **Load-bearing** | may, some, associated, causes, significant, first, shall… | Strengthening or weakening needs evidence and is listed separately |
| ✏️ **Free surface** | Grammar, spelling, punctuation, word order, redundancy | Improved directly |

Every change is tiered **L1 surface / L2 structure / L3 claim**. One-line fixes come back as plain text; longer revisions include a ledger of important changes; claim changes are never silent.

On academic integrity: it **never fabricates** references, data, results or author actions, and marks missing information with explicit placeholders such as `[please supply…]`. It does not optimize for AI-detection or plagiarism scores. Full rules: [SKILL.md](skills/academic-writing-assistant/SKILL.md).

## 🔧 Optional local checks

Core writing needs no Python. If your agent can run Python, the bundled scripts add mechanical checks:

| Script | Purpose |
|---|---|
| `fidelity_check.py` | Compares numbers, citations, formulas and statute numbers before and after a revision |
| `manuscript_audit.py` | Abbreviation definitions, "significant" without a test, word and character limits |
| `terminology_checker.py` | Variant translations of one concept and easily confused related concepts |
| `structure_checker.py` | Elements a section such as an abstract may be missing |

The scripts use only the Python standard library, run locally and make no network requests. See [script docs](docs/scripts.md).

## ❓ FAQ

<details>
<summary><strong>Will it change my data or conclusions?</strong></summary>

Not silently. Numbers, citations and formulas are locked; any change to claim strength is listed in the ledger with a reason. If the text and a table disagree, it flags the conflict instead of picking one.

</details>

<details>
<summary><strong>Can it lower my AI-detection or plagiarism score?</strong></summary>

It does not optimize for detector scores and promises none. It can fix genuine vagueness, repetition, logic and citation problems.

</details>

<details>
<summary><strong>Is my manuscript safe?</strong></summary>

The bundled scripts run locally, make no network requests and collect no data. Your AI agent or cloud model will still receive the text you provide, so follow your platform's and institution's data policies.

</details>

More in the [FAQ](docs/faq.md) (Chinese).

## 🤝 Contributing

Discipline conventions, terminology and synthetic examples are welcome, as are script fixes. Please read the [contributing guide](CONTRIBUTING.md); see the [roadmap](ROADMAP.md) and [changelog](CHANGELOG.md).

If this Skill helps your writing, please give it a ⭐ **star** so more researchers can find it.

[![Star History Chart](https://api.star-history.com/svg?repos=LvvUP/academic-writing-assistant&type=Date)](https://star-history.com/#LvvUP/academic-writing-assistant&Date)

## 📄 License

**AGPL-3.0-only** — see [LICENSE](LICENSE) and the [licensing notes](docs/licensing.md). Permissions granted under earlier MIT versions remain valid.
