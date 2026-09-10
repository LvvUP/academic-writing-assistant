<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/revision-compass.png">
  <img src="assets/logo/revision-compass.svg" alt="Revision Compass: pages, revision lines and a check mark" width="112">
</picture>

# Academic Writing Assistant

**Clearer manuscripts. Important changes you can check.**

A Chinese–English academic writing Skill for researchers. Polish, translate and draft reviewer responses from the research material you provide.

[中文](README.md) · **English**

[![License: AGPL-3.0-only](assets/readme/license-agpl.svg)](LICENSE)
[![Actual model evaluation records, including failures and limitations](assets/readme/evaluation-records.svg)](evals/results-2026-09-10.md)

[Get started](#get-started) · [More examples](examples/) · [Compatibility](docs/compatibility.md) · [Evaluation records](evals/results-2026-09-10.md)

<sub>0.3.0 · Unreleased (in development, not a formal release)</sub>

</div>

## See a revision

This is a **synthetic example** of intended handling, not a real research finding or model-evaluation record.

**Input · Polish the Chinese text without changing its meaning**

> 该方法可能在部分场景改善性能，噪声往往会在一定程度上影响现有方法。

**Output**

> 该方法可能在部分场景下改善性能；噪声往往会对现有方法产生一定程度的影响。

**Changed:** phrasing and the connection between clauses. **Preserved:** possibility, limited scope, frequency and degree—“可能、部分、往往、一定程度”. These words carry the claim's strength and scope.

The revised text comes first, followed by important changes and open questions. A short sentence may need little or no editing. Mentioning submission or SCI alone does not request an English translation.

## Get started

Core writing needs an Agent that can load instructions. The installer and mechanical checks need **Python 3.9+**; core text use needs neither Python nor a designated paid API. Available capabilities depend on the host.

**This is the unmerged 0.3.0 candidate.** These steps target `codex/academic-writing-upgrade`; they do not assume the default branch contains the installer. The development branch must be publicly pushed before the clone command works. Until then, use a candidate checkout supplied by the maintainer.

```sh
git clone --branch codex/academic-writing-upgrade \
  https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
```

For an existing repository, check out that development branch first. Then run the installer from the repository root. For Codex:

```sh
python3 -B scripts/install_skill.py install \
  --host codex --home-root "$HOME"
```

This installs to `~/.agents/skills/academic-writing-assistant`. **Every existing destination is refused, including an empty directory.** Update and uninstall also refuse and preserve contents when user edits, extra files or caches are present. See [installation, updates and troubleshooting](docs/installation.md).

Refresh the host's Skill list or start a new session, select the actual discovered Skill entry, and enter this in Codex:

```text
$academic-writing-assistant
Polish this Chinese paragraph. Preserve numbers, conditions and citations:
…
```

<details>
<summary><strong>Claude Code, Cursor and Grok Build</strong></summary>

Choose one installation command for your host:

```sh
python3 -B scripts/install_skill.py install \
  --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py install \
  --host cursor --home-root "$HOME"
python3 -B scripts/install_skill.py install \
  --host grok-build --home-root "$HOME"
```

- **Claude Code:** install under `~/.claude/skills`; invoke `/academic-writing-assistant`.
- **Cursor:** install under `~/.cursor/skills`; type `/` in Agent and select the Skill.
- **Official Grok Build coding agent:** install under `~/.grok/skills`; invoke `/academic-writing-assistant`. This does not establish native support in Grok web chat, model APIs or third-party CLIs.

These are personal Skill parent directories; the package occupies an `academic-writing-assistant` subdirectory. Claude Code uses a slash invocation, rather than Codex's `$` syntax.

See the [compatibility matrix](docs/compatibility.md) for Codex's older `.codex/skills` path, project scope and the optional plugin wrapper. Other hosts can load `SKILL.md` and the needed references from the complete package; file reading, Python and retrieval depend on actual capabilities.

</details>

**Native verification scope (2026-09-10):** Temporary local installation lifecycles and directory mappings were tested. Codex CLI 0.147.0 discovered the Skill, but its model call returned **HTTP 400** requiring a newer CLI; writing behavior in that attempt is **NOT RUN**. Native discovery and behavior in Claude Code, Cursor and Grok Build are **NOT RUN**. Official directory documentation and installer tests are not native certification. See the [compatibility matrix](docs/compatibility.md).

## How revisions work

The fidelity contract divides text into three zones:

- **Locked:** preserve numbers, units, citations, equations and names against readable source material. Flag conflicts first; apply and disclose author-confirmed corrections or format conversions within the authorized scope.
- **Load-bearing:** possibility, scope, negation, causality, significance and novelty. Weakening as well as strengthening can change a claim and needs evidence and explanation.
- **Free surface:** grammar, spelling, word order and redundancy that can be improved without changing meaning.

Explain important edits as **L1 surface / L2 structure / L3 claim**, with no silent L3 changes. A newly written translation gets no fictional L1 correction count. Terminology work must preserve distinctions already defined by the author. See the [fidelity protocol](skills/academic-writing-assistant/references/fidelity-protocol.md).

| Mode | Suitable tasks | Delivery focus |
|---|---|---|
| Quick polish | One-line corrections and short passages | Text and necessary notes |
| Standard revision | Polishing, translation, abstracts and responses | Text, important edits and material gaps |
| Deep structural review | Long drafts and multiple sources | Actual coverage and claim-to-source locations |

The Skill also supports section drafting, submission materials and whole-draft consistency review. Journal response letters and conference rebuttals follow their respective contexts. Empirical studies, theoretical proofs, qualitative research and reviews receive appropriate checks; see [research-type examples](examples/research-types.md). Missing material stays explicit. Completed work, confirmed plans and undecided suggestions remain distinct.

## Two more examples

These are also **synthetic inputs and expected outputs**.

### CN→EN · Add no experimental conclusion

**Input**

> 请译成英文：针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法。

**Output**

> To address large variations in target scale and complex backgrounds in remote sensing images, this study proposes a multi-scale feature fusion method.

Terminology follows this sentence's context. No module mechanism, comparison group or experimental result is added. See the [translation example](examples/translation.cn-en.md).

### Reviewer response · Make no unconfirmed commitment

**Input**

> A reviewer suggests the gain may be within random variation. Under the same protocol, we ran 5 seeds with a mean gain of 2.1 percentage points and a standard deviation of 0.3. The quantity represented by 0.3 is unspecified; we have not decided to add experiments or tables.

**Response draft**

> Under the same evaluation protocol, we observed a mean improvement of 2.1 percentage points across 5 seeds. These descriptive results alone do not establish that the improvement exceeds random variation.

**To confirm:** whether 0.3 describes method scores, baseline scores or paired differences, and whether a corresponding test exists. The draft neither infers significance nor adds unconfirmed experiments, tables or revision commitments. See the [reviewer-response examples](examples/reviewer-response.md).

## Mechanical checks and actual evaluation

The four manuscript-checking entry points use the **Python standard library** and do not rewrite inputs. Start with a fidelity comparison:

```sh
python3 -B skills/academic-writing-assistant/scripts/fidelity_check.py \
  --before original.tex --after revised.tex --strict
```

It compares recognized numbers, units, citations, mathematical expressions and macro arguments. Three other entry points are available:

- `manuscript_audit.py`: abbreviations, claim-evidence cues and length.
- `terminology_checker.py`: terminology variants and author-defined maps.
- `structure_checker.py`: section cues for the selected research type.

See the [script reference](docs/scripts.md) for usage. Default advisory mode may exit 0 despite findings. `--strict` exits 1 for findings or insufficient coverage; input or runtime errors exit 2.

**Mechanical checks have limited coverage.** No detected difference does not establish full semantic fidelity or citation support. Automatic tense auditing is **NOT RUN**. Word revisions, PDF images and tables depend on what the host actually parses. Abstract-only reading stays labeled as such, and unexecuted checks remain unexecuted. See [capability fallback](examples/capability-fallback.md).

**Actual model evaluation is separate from host testing.** The 2026-09-10 primary evaluation used 20 base tasks and 4 repeats per variant: the baseline scored **24/24 PASS** and the initial candidate **23 PASS, 1 FAIL**. The failure omitted an incomplete-experiment status. Separate paired E04 checks after repair scored **2/2 PASS per version**; the original failure and separate denominators remain. Small samples and shared context prevent a conclusion of overall superiority. See the [full evaluation record](evals/results-2026-09-10.md).

Contributors can configure dependencies using the [testing guide](docs/testing.md), then run:

```sh
python3 -B -m pytest tests/
python3 -B skills/academic-writing-assistant/scripts/skill_lint.py .
```

`skill_lint.py` also needs PyYAML; development dependencies are not core writing requirements. Local results and remote CI configuration are different evidence, and untested platforms remain identified.

## Integrity, privacy and license

The rules prohibit invented references, findings, statistical tests, ethics approvals and author actions. Commands embedded in manuscripts or retrieved material are not authorization. Retrieval uses necessary non-sensitive information and does not automatically authorize uploading unpublished work. Local scripts do not initiate networking; a host's cloud model may still receive input. Select material according to the platform's data handling settings.

See the [security guide](SECURITY.md) and [FAQ](docs/faq.md) for more details.

The Skill can improve expression, paraphrasing and citation; it does not optimize for AI-detector scores or plagiarism evasion. AI-use statements describe only confirmed use and follow the current guide for the specific venue, year and track.

Contributions of synthetic cases, terminology definitions and sourced field guidance are welcome. Read the [contribution guide](CONTRIBUTING.md); see the [CHANGELOG](CHANGELOG.md) and [ROADMAP](ROADMAP.md) for changes and plans.

This development version uses **AGPL-3.0-only**; see [LICENSE](LICENSE) and the [licensing guide](docs/licensing.md). Rights already granted through historical MIT distributions remain under their original terms. Notices are retained in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md).

If this Skill helps your writing, consider giving the repository a Star.
