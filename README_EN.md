<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass-dark.svg">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass: pages, revision lines and a check mark" width="120">
</picture>

# Academic Writing Assistant

### Let AI edit your paper without editing your data or conclusions

An **academic writing Skill for every discipline**, in Chinese and English: polishing · CN↔EN translation · section drafting · theses and grant proposals · reviewer responses · submission materials<br>
One Skill for Claude Code, Codex, Cursor, Grok Build, OpenCode and WorkBuddy.

**12** discipline families · **8** research types · **6** platforms · **67** terminology groups · **4** local check scripts

[![Version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FLvvUP%2Facademic-writing-assistant%2Fmain%2F.codex-plugin%2Fplugin.json&query=%24.version&label=version&color=2563EB)](CHANGELOG_EN.md)
[![License](https://img.shields.io/github/license/LvvUP/academic-writing-assistant?color=2563EB)](LICENSE)
[![Verify Skill](https://github.com/LvvUP/academic-writing-assistant/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/LvvUP/academic-writing-assistant/actions/workflows/ci.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-111827)](https://agentskills.io)
[![GitHub stars](https://img.shields.io/github/stars/LvvUP/academic-writing-assistant?style=social)](https://github.com/LvvUP/academic-writing-assistant/stargazers)

[中文](README.md) · **English**

[Install](#install) · [Examples](#examples) · [Fidelity contract](#the-fidelity-contract) · [Features](#features) · [Disciplines](#disciplines) · [Supported platforms](#supported-platforms) · [Upgrading](#upgrading) · [FAQ](#faq)

</div>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme/fidelity-contract.en.dark.svg">
    <img src="assets/readme/fidelity-contract.en.svg" width="100%" alt="One informal manuscript passage, two ways to edit it. Unbounded polishing sounds more professional but drops the hedges “may” and “in some settings”, turns 92.3% into 92% and replaces the method in [12] with “existing methods”. With Academic Writing Assistant the language becomes just as professional while hedges, the number and the citation stay as written, and the edit explains what changed and what the author should confirm.">
  </picture>
</p>

<p align="center"><sub>The same passage: unbounded polishing drops the hedges, turns 92.3% into 92% and replaces the method in [12] with “existing methods”; with the Skill the language is just as professional, all of these stay as written, and one question is raised for the author to confirm.</sub></p>

Grammar and fluency are rarely the problem when AI edits a paper. The danger is edits that **sound more professional but quietly change the facts**.

Academic Writing Assistant gives your agent a **fidelity contract**: improve the language freely, but never move the facts or the evidence boundary, and list every change to claim strength so you decide whether to accept it. You get the revised text, plus a short account of what changed, why, and which evidence is still missing.

## Install

Send the message below to your AI agent; it downloads, installs and verifies the Skill. It works for **Claude Code, Codex, Cursor, Grok Build and OpenCode**. For WorkBuddy, use the [separate prompt below](#workbuddy).

```text
Please install (or update, if already installed) the academic writing Skill "academic-writing-assistant", using only the repository's own installer:
1. Work out which agent you are and pick --host: Claude Code → claude, Codex → codex, Cursor → cursor, Grok Build → grok-build, OpenCode → opencode. If you are none of these, tell me and stop.
2. git clone --depth 1 https://github.com/LvvUP/academic-writing-assistant (main branch) into a temporary folder and run there (Python 3.9+; on Windows `py -3` can replace python3):
   python3 -B scripts/install_skill.py install --host <value above> --home-root "$HOME"
3. If it says the Skill is already installed, run it again with update instead of install. If it asks for --backup-existing, do as it says: run update with that flag added (the old copy is moved to a backup folder, not deleted). For any other error, show it to me and stop: don't copy or delete files by hand, don't bypass the checks, don't use sudo.
4. Verify: run the same command once more with verify instead of install. It should print "verified" and the version.
5. Delete the temporary folder, then tell me the install path, the version, the backup location (if any) and any notes the script printed, plus how to invoke the Skill and whether I need a new session.
```

To update later, send the same message again.

<details>
<summary><strong>Alternative: run the same installer yourself</strong></summary>

Requires Git and Python 3.9+:

```sh
git clone --depth 1 https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py verify --host claude --home-root "$HOME"
```

Replace `claude` with your agent:

| Agent | `--host` | Install location |
|---|---|---|
| Claude Code | `claude` | `~/.claude/skills/academic-writing-assistant` |
| Codex | `codex` | `~/.agents/skills/academic-writing-assistant` |
| Cursor | `cursor` | `~/.cursor/skills/academic-writing-assistant` |
| Grok Build | `grok-build` | `~/.grok/skills/academic-writing-assistant` |
| OpenCode | `opencode` | `~/.config/opencode/skills/academic-writing-assistant` |

To export a package for WorkBuddy:

```sh
python3 -B scripts/install_skill.py export --destination "$HOME/awa-package/academic-writing-assistant" --archive
```

To update, run `git pull --ff-only` first (or clone again), then use `update` instead of `install`; to remove, use `uninstall`. On Windows, `py -3` can replace `python3`. The prompt and the terminal use the same installer, so either one can update a copy installed by the other. See the [installation guide](docs/installation.md) (Chinese, with an English quick start) for details.

</details>

### WorkBuddy

WorkBuddy imports your own Skill packages through its upload dialog: let it prepare the package, then upload it yourself.

<details>
<summary><strong>Prompt for WorkBuddy and upload steps</strong></summary>

```text
Please prepare a package of the academic writing Skill "academic-writing-assistant" so that I can add it to WorkBuddy through "Upload skill" (上传技能):
1. git clone --depth 1 https://github.com/LvvUP/academic-writing-assistant (main branch) into a temporary folder inside the current workspace.
2. In that folder, run (Python 3.9+; on Windows `py -3` can replace python3; replace <workspace> with the absolute path of the current workspace):
   python3 -B scripts/install_skill.py export --destination "<workspace>/awa-package/academic-writing-assistant" --archive
   It creates the Skill folder awa-package/academic-writing-assistant and the archive awa-package/academic-writing-assistant.zip. If it says they already exist, an earlier export is still there: tell me, and I will decide whether to delete the old awa-package folder and retry. For any other error, show it to me and stop; don't assemble the files by hand.
3. Verify: confirm that SKILL.md is at the top level of the archive and read the version under metadata.
4. Delete the temporary folder from step 1 (keep awa-package), tell me the full paths of the archive and the Skill folder and the version, and remind me to upload the archive under 专家·技能·连接器 → 技能 → 添加技能 → 上传技能.
```

Then, in WorkBuddy:

1. Click **专家·技能·连接器** (Experts · Skills · Connectors) in the left sidebar and open the **技能** (Skills) tab.
2. Click **添加技能 → 上传技能** (Add skill → Upload skill) and drop or select `academic-writing-assistant.zip`. If the archive cannot be imported, use the `academic-writing-assistant` folder next to it, which has the same content.
3. If an older version is listed, uninstall it under 已安装 (Installed) first, then upload the new package.

If you prefer not to run commands, download `academic-writing-assistant.zip` from the latest release on the [Releases page](https://github.com/LvvUP/academic-writing-assistant/releases) and upload it directly.

> These steps follow the upload flow in WorkBuddy's [documentation](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) (Chinese); the sources for each statement are listed in the [compatibility notes](docs/compatibility.md) (Chinese). The English labels in parentheses are translations of the Chinese interface names. Please [open an issue](https://github.com/LvvUP/academic-writing-assistant/issues) if the upload fails.

</details>

### Check that it works

The installer's `verify` action checks the installed files. To confirm that your agent has loaded the Skill:

| Platform | How to check |
|---|---|
| Claude Code | Type `/` and find `academic-writing-assistant` in the list |
| Codex | Run `/skills`, or type `$` and select it |
| Cursor | Type `/` in the Agent input and search for `academic-writing-assistant` |
| Grok Build | Run `/skills`, or type `/academic-writing-assistant` |
| OpenCode | Write `@academic-writing-assistant` in your prompt; if it loads, the Skill is installed |
| WorkBuddy | It appears under 专家·技能·连接器 → 技能 → 已安装 (Installed) |

If it does not show up, open a new session or restart the agent; see the [installation guide](docs/installation.md#验证安装成功) (Chinese) for details.

### Usage

Describe your writing task in plain language and the agent loads the Skill automatically. You can also invoke it explicitly:

```text
/academic-writing-assistant Please polish this abstract.

[paste your text]
```

There is no need to add “don't change my data”: keeping numbers, citations and claim strength, and listing important changes, are the Skill's default rules.

> Claude Code and Grok Build use `/academic-writing-assistant`; Codex uses `$academic-writing-assistant`; in Cursor, type `/` in the Agent input and pick the Skill; OpenCode uses `@academic-writing-assistant`; in WorkBuddy, describe the task or type `/` to pick it from the skill list.

## Examples

> All examples are synthetic; people, data and citations are for demonstration only. Both edits are illustrations: “Unbounded polishing” shows common distortions, and “With Academic Writing Assistant” is the output expected under the Skill's rules.

### Humanities: one sentence from a letter, and a conjecture (history)

**Original (a non-native English draft)**

> I read two letters he wrote to his younger brother, and there is one sentence “Of late I think often of the scenery of Jiangnan”, so I think at that time he probably already had the idea to leave the capital, but it is not sure. This also shows he was very dissatisfied with the court's policies.

**Unbounded polishing**

> In two letters to his younger brother, he wrote that he had “lately been longing for the landscapes of the south”, which shows that he resolved to leave the capital out of dissatisfaction with the court's policies.

The prose is elegant now, but the quotation has been reworded (the letter says “Of late I think often of the scenery of Jiangnan”); the tentative “probably … not sure” has become “resolved to leave”; and the claim about his motive is presented as established.

**With Academic Writing Assistant**

> Two letters to his younger brother contain the sentence “Of late I think often of the scenery of Jiangnan”. This suggests that he had probably already thought of leaving the capital, although this cannot be confirmed.

What comes with it:

- **Language**: informal phrasing rewritten, for example “he probably already had the idea to leave the capital, but it is not sure” → “he had probably already thought of leaving the capital, although this cannot be confirmed”. The quotation is kept word for word, and the tentative tone is kept.
- **Claim (L3), your decision**: “This also shows he was very dissatisfied with the court's policies” is left out of the text. A sentence about missing Jiangnan is not enough to support a claim of dissatisfaction with the court's policies, which needs other sources. A bounded wording you can use as it stands:

  > Whether he was dissatisfied with the court's policies cannot be determined from these two letters alone and awaits corroboration from other sources.

### Science and engineering: an informal account of results (chemistry and materials)

**Original (a non-native English draft)**

> We calcined the catalyst at 500 °C for 2 hours and then tested it. Its activity is higher than the uncalcined one for about 37%, and after using 5 cycles the activity still has 91.5% (Table 3). So the stability of this catalyst is very good and it can be directly used in industrial production.

**Unbounded polishing**

> After calcination at 500 °C for 2 hours, the catalytic activity increased significantly by nearly 40%, and as much as 91.5% of the activity was retained after 5 cycles (Table 3), demonstrating excellent long-term stability and great potential for industrial application.

Here “about 37%” has been rounded up to “nearly 40%” and given a “significantly” that no test supports; “the activity still has 91.5%” has quietly been read as a retention rate; five cycles are now “long-term stability”; and the unsupported industrial claim has merely been given a more respectable wording.

**With Academic Writing Assistant**

> After calcination at 500 °C for 2 hours, the activity of the catalyst was about 37% higher than that of the uncalcined sample, and it remained at 91.5% after 5 cycles (Table 3).

What comes with it:

- **Language**: non-idiomatic wording rewritten, for example “Its activity is higher than the uncalcined one for about 37%” → “the activity of the catalyst was about 37% higher than that of the uncalcined sample”. The temperature, duration, both percentages and the table number are exactly as written, with no rounding.
- **To confirm**: is “about 37%” a relative increase or 37 percentage points? Is 91.5% the activity retained relative to the first cycle? Once you confirm, both can be stated more precisely.
- **Claims (L3), your decision**: “the stability … is very good” and “can be directly used in industrial production” go beyond data from 5 cycles and are not carried over as written. A bounded wording you can add as it stands:

  > This indicates a degree of cycling stability over the 5 cycles examined; stability over longer runs and the potential for industrial use remain to be verified under realistic operating conditions.

### More tasks and disciplines

<details>
<summary><strong>Polishing: a correlation does not become causation (social science)</strong></summary>

**Original (a non-native English draft)**

> We find 412 university students to do a questionnaire, and ask them how long they watch short videos every day and how about their study engagement. The result shows students who watch more have lower study engagement (r = −0.29, p < 0.001). This shows short videos seriously affect students' study, so schools should do something quickly.

**Polished**

> We surveyed 412 university students about their daily short-video use and their study engagement. Daily short-video use was negatively correlated with study engagement (r = −0.29, p < 0.001).

**A common wrong edit:** *The results showed that short-video use significantly reduced study engagement (r = −0.29, p < 0.001), which is consistent with previous studies [3].* The correlation has become causation, and a reference appears that the draft never contained.

**Important change (L3):** “This shows short videos seriously affect students' study” and “schools should do something quickly” are left out of the text: a survey correlation supports “associated”, not “affect” or “seriously”, nor a recommendation that depends on a causal claim. A bounded wording you can use: “This result suggests an association between the two; whether the relationship is causal, and in which direction, remains to be tested in longitudinal or intervention studies.”

</details>

<details>
<summary><strong>CN→EN translation: “lower risk” does not become “reduced the risk” (medicine)</strong></summary>

**Chinese source**

> 在这项回顾性队列研究中，我们纳入了 2018—2022 年间在本院就诊的 1,236 名 2 型糖尿病患者。与未使用该药物的患者相比，使用该药物的患者心血管事件风险较低（HR = 0.78，95% CI 0.64–0.95），但这一关联在 65 岁及以上患者中不明显。

**English translation**

> In this retrospective cohort study, we included 1,236 patients with type 2 diabetes who attended our hospital between 2018 and 2022. Compared with non-users, patients who used the drug had a lower risk of cardiovascular events (HR = 0.78, 95% CI 0.64–0.95), although this association was not evident in patients aged 65 years or older.

**A common wrong edit:** *use of the drug reduced the risk of cardiovascular events … and had no effect in patients aged 65 years or older.* The association has become causation, and “not evident” has become “no effect”.

**Translation notes:** the source says 风险较低 (lower risk) and 关联不明显 (the association was not evident), and the translation keeps the same claim strength: *had a lower risk*, not *reduced the risk*; *not evident*, not *no effect*. Numbers, the confidence interval and the age threshold map one-to-one.

</details>

<details>
<summary><strong>CN→EN translation: “shall” does not weaken into “should” (law)</strong></summary>

**Chinese source (synthetic provision, not current law)**

> 用人单位应当在用工之日起一个月内与劳动者订立书面劳动合同；未订立的，不得以此为由拒绝支付劳动报酬。

**English translation**

> The employer shall conclude a written employment contract with the employee within one month from the date on which employment begins. Where no such contract has been concluded, the employer shall not refuse to pay remuneration on that ground.

**A common wrong edit:** *The employer should conclude a written employment contract … and should not refuse to pay remuneration on that ground.* The obligation (*shall*) and the prohibition (*shall not*) have both been weakened into advice (*should*).

**Translation notes:** 应当 is the obligatory *shall* and 不得 is *shall not*; neither is weakened into *should*. The time limit, its starting point and the condition are unchanged.

</details>

<details>
<summary><strong>Polishing: a simulation is not “ready for engineering use” (engineering)</strong></summary>

**Original (Chinese)**

> 我们用有限元仿真算了一下，这个支架的最大应力是 182 MPa，比许用应力 235 MPa 小，所以这个结构是安全的，可以直接用到工程上。

*(Our finite element simulation gives a maximum stress of 182 MPa in the bracket, below the allowable stress of 235 MPa, so the structure is safe and can be used in engineering directly.)*

**Polished**

> 有限元仿真结果显示，该支架的最大应力为 182 MPa，低于许用应力 235 MPa。

**A common wrong edit:** 仿真结果证明该结构安全可靠，可直接应用于工程实践。 *(The simulation proves that the structure is safe and reliable and can be applied directly in engineering practice.)* One simulation has been written up as engineering validation.

**Important change (L3):** “the structure is safe and can be used directly” goes beyond what one simulation supports. If tests or a code check have been completed, supply them and the claim can be written; otherwise a bounded alternative is “meets the strength requirement under the simulated load case”, with loads and boundary conditions stated. Values and units are unchanged.

**To confirm:** is 235 MPa the allowable stress set by the design code, or the yield strength of the material? The two imply different safety margins.

</details>

<details>
<summary><strong>Reviewer response: only state revisions the author has completed (computer science)</strong></summary>

**Reviewer comment**

> The accuracy gain may come at the cost of higher inference latency.

**Author notes (Chinese)**

> 我们同意需要量化推理开销。已在同一张 GPU、batch size = 1、相同输入分辨率下测量推理延迟：baseline 为 18 ms/图像，我们的方法为 21 ms/图像；准确率分别为 84.2% 和 86.1%。已将这组结果补入修订稿表 4，并在第 5.2 节补充准确率与延迟的权衡。请写成英文期刊回复。

**Draft response**

> Thank you for raising this point. We have quantified the accuracy–latency trade-off on the same GPU, with a batch size of 1 and the same input resolution. Our method achieves an accuracy of 86.1% at 21 ms per image, compared with 84.2% at 18 ms per image for the baseline. The gain in accuracy comes with higher latency. We have added these results to Table 4 and a discussion of the trade-off to Section 5.2 of the revised manuscript.

**A common wrong edit:** *We have conducted additional experiments on more devices and will release the code.* It commits the author to work that was never done or planned.

**Structure:** answer the concern, give comparable results, then point to completed revisions. Table and section numbers and completion status all come from the author's notes; no new experiments are promised on the author's behalf.

</details>

More examples are in [examples/](examples/) (Chinese), including economics, clinical medicine, theses, research proposals and grant applications, as well as checking claims against a table and terminology consistency.

## The fidelity contract

| Zone | Includes | Handling |
|---|---|---|
| **Locked** | Numbers, units, p-values, citations, formulas, statutes, direct quotations, ethics IDs… | Kept verbatim; suspected errors are flagged, not silently “fixed” |
| **Load-bearing** | may, some, associated, causes, significant, first, shall… | Strengthening or weakening needs evidence and is listed separately |
| **Free surface** | Grammar, spelling, punctuation, word order, redundancy | Improved directly |

Every change is tiered **L1 surface / L2 structure / L3 claim**. One-line fixes come back as plain text; longer revisions include a ledger of important changes; and the Skill requires the agent to list changes to claims separately rather than apply them silently. These are the edits the contract is aimed at:

| You wrote | The “polish” that should not happen | Problem |
|---|---|---|
| The method **may** improve performance **in some settings** | The method significantly improves performance | Hedges removed, claim inflated |
| A is **associated with** B | A **causes** B | Correlation becomes causation |
| improved by 2.1 **percentage points** | improved by 2.1% | Percentage points become a percentage, so the number means something else |
| (no citation) | …(Smith et al., 2021) | Fabricated reference |
| We **plan to** run a survey | We ran a survey | Plan becomes result |

**Academic integrity:** under the Skill's rules the agent does not fabricate references, data, results or author actions, and marks missing information with explicit placeholders such as `[please supply…]`. It does not optimize for AI-detection or plagiarism scores. It also reminds you of two things only you can do: verify every reference before you submit, and check your journal's, school's or funder's current rules on using AI tools. Full rules: [SKILL.md](skills/academic-writing-assistant/SKILL.md).

## Features

| What you're doing | What the Skill handles |
|---|---|
| Revising | Chinese and English polishing, expansion, merging, compression to a limit, titles and contributions |
| Translating | CN→EN and EN→CN with terminology notes; LaTeX and citations preserved |
| Drafting | Abstract, introduction, literature review, methods, results, discussion and conclusion from your material |
| Theses and proposals | Thesis chapters, bilingual abstracts, research proposals and grant applications |
| Responding to reviewers | Journal response letters and conference rebuttals that separate completed revisions from plans |
| Submitting | Cover letters, highlights, AI-use statements, CRediT statements |
| References and formats | Reference lists in GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver and other styles; LaTeX citations, math and cross-references kept intact |
| Whole-draft checks | Consistency of terms, abbreviations, symbols, numbers and claims across sections |

## Disciplines

Built-in writing guidance for 12 discipline families; anything else follows a general procedure that respects your field's conventions and structure.

| Area | Discipline families |
|---|---|
| Humanities & social sciences | Humanities · Law · Economics & management · Social sciences · Education & psychology |
| Medicine & life sciences | Medicine & public health · Life sciences & agriculture |
| Natural sciences & mathematics | Physics, chemistry & materials · Mathematics & statistics · Earth & environmental sciences |
| Engineering & computing | Engineering · Computer science & AI |

**Research types are handled on their own terms too:** experimental · survey and econometric · qualitative · theoretical · review · humanities and legal interpretation · case study · design research

The bundled examples and terminology map draw on many disciplines. The section-structure checks follow these 8 research types, so a history paper is not asked for an “experimental setup”; the Skill's rules also require that interview themes are not turned into population percentages.

## Supported platforms

| Platform | Installation | Invocation |
|---|---|---|
| Claude Code | Prompt install to `~/.claude/skills/` | `/academic-writing-assistant` or automatic |
| Codex | Prompt install to `~/.agents/skills/` | `$academic-writing-assistant` or automatic |
| Cursor | Prompt install to `~/.cursor/skills/` | Type `/` and pick it, or automatic |
| Grok Build | Prompt install to `~/.grok/skills/` | `/academic-writing-assistant` or automatic |
| OpenCode | Prompt install to `~/.config/opencode/skills/` | `@academic-writing-assistant` or automatic |
| WorkBuddy | Export a package, then import it through its upload dialog | Describe the task, or type `/` and pick it |

All six use the same Skill, which follows the [Agent Skills specification](https://agentskills.io/specification). Directories, the official documentation they are based on, and advice for using several agents side by side are in the [compatibility notes](docs/compatibility.md) (Chinese).

## Optional local checks

Core writing needs no Python. If your agent can run Python, the bundled scripts add mechanical checks:

| Script | Purpose |
|---|---|
| `fidelity_check.py` | Compares numbers, citations, formulas and statute numbers before and after a revision |
| `manuscript_audit.py` | Abbreviation definitions, “significant” without a test, word and character limits |
| `terminology_checker.py` | Variant wordings of one concept, and concepts that must stay distinct such as incidence vs prevalence |
| `structure_checker.py` | Elements a section such as an abstract, methods or results may be missing, by research type |

The scripts use only the Python standard library, run locally and make no network requests. See the [script docs](docs/scripts.md) (Chinese).

## Upgrading

Version 0.5.0 keeps every file name, directory and install path, so existing usage is unaffected.

| Your situation | How to upgrade |
|---|---|
| Installed with the prompt or the installer | Send the [install prompt](#install) again |
| An older copy made by hand or by another tool | Send the install prompt as well; the old copy is moved to a backup folder (not deleted) and the new version is installed |
| WorkBuddy | Prepare a new package, uninstall the old version under 已安装 (Installed), then upload |

See the [changelog](CHANGELOG_EN.md) for what changed and the [installation guide](docs/installation.md#升级) (Chinese) for other cases.

## FAQ

<details>
<summary><strong>Will it change my data or conclusions?</strong></summary>

The Skill requires the agent not to change them silently: numbers, citations and formulas are locked, any change to claim strength is listed in the ledger with a reason, and if the text and a table disagree the conflict is flagged instead of one value being picked. If your agent can run Python, `fidelity_check.py` can also compare the numbers, citations and formulas before and after a revision mechanically.

</details>

<details>
<summary><strong>Can it lower my AI-detection or plagiarism score?</strong></summary>

It does not optimize for detector scores and promises none. It can fix genuine vagueness, repetition, logic and citation problems.

</details>

<details>
<summary><strong>Is my manuscript safe?</strong></summary>

The bundled scripts run locally, make no network requests and collect no data. Your AI agent or cloud model will still receive the text you provide, so follow your platform's and institution's data policies.

</details>

<details>
<summary><strong>Can it write a literature review if I have no references?</strong></summary>

If your agent can search, it searches and reports what it actually read. If it cannot, it gives a structure, search terms and explicit citation placeholders rather than inventing references from memory. Either way, verify every reference yourself before submitting.

</details>

<details>
<summary><strong>Do I need to disclose that I used AI?</strong></summary>

That depends on the current rules of your journal, school or funder, which differ. The Skill reminds you to check and can draft a statement from the use you confirm, but it does not decide compliance for you.

</details>

More in the [FAQ](docs/faq.md) (Chinese).

## Contributing

Discipline conventions, terminology and synthetic examples are welcome, as are script fixes. Please read the [contributing guide](CONTRIBUTING.md); see the [roadmap](ROADMAP.md) and [changelog](CHANGELOG_EN.md).

If this Skill helps your writing, please give it a ⭐ **star** so more researchers can find it.

## License

**AGPL-3.0-only** — see [LICENSE](LICENSE) and the [licensing notes](docs/licensing.md).
