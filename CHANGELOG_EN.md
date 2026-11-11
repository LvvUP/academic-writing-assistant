# Changelog

[中文](CHANGELOG.md) · **English**

## 0.5.0

Better balance across disciplines, WorkBuddy support, and installs that can be verified. No file names, directories, install paths or existing command-line options changed, so earlier versions can be updated directly.

### Writing

- **Examples and guidance from more disciplines**: the bundled examples and the sample sentences in the Chinese and English style guides and the fidelity protocol now come from chemistry and materials, medicine, environmental science, management, law, history, education, engineering and computing.
- **Reminders to verify references and AI-use rules**: when the output contains references, the Skill reminds the author to verify each one before submission; for journal submissions, theses, research proposals, grant applications or coursework, it reminds the author to check the current rules of the journal, school or funder.
- **Updated citation guide**: explains which edition to follow now that GB/T 7714—2025 is in force, and adds the in-text and reference-list conventions of APA, MLA, Chicago, IEEE and Vancouver, with a note on legal citation.
- **More policy sources**: adds entry points to the AI-use policies of ICMJE, Springer Nature and Taylor & Francis, each with its own read date, and explains how theses, grant applications and Chinese-language journals are handled.
- **Trigger description**: tasks and trigger phrases in Chinese and English now come first.

### Check scripts

- `structure_checker.py` adds the research types `observational`, `interpretive`, `case_study` and `design`, and an abstract's evidence clue now follows the research type. It also accepts the discipline-neutral section names `results` and `literature_review`; `experiment` and `related_work` keep working.
- The terminology map adds groups for law, humanities, social sciences, chemistry and materials, life sciences, earth and environmental science and engineering, and more groups for statistics, medicine, and economics and management: 67 groups in total. Most new groups flag concepts that must stay distinct, such as standard deviation vs standard error, or 定金 vs 订金.

### Installation and documentation

- **WorkBuddy support**: `install_skill.py export --archive` exports the Skill folder and an archive, which is imported through WorkBuddy's 上传技能 (Upload skill).
- **New `verify` action**: a read-only check that an installed copy is complete and unmodified, reporting its version. The install prompt now ends with a verification step.
- The installation guide adds per-platform checks that the Skill is loaded and an upgrade section. The compatibility notes cover six platforms, with the official documentation they rely on and the date it was checked.
- README rewritten: adds a fidelity-contract illustration, with examples from the humanities and social sciences and from science and engineering.
- New synthetic examples for medicine, materials chemistry and engineering.
- Updated development and CI dependencies (pytest 9.2.0, pluggy 1.7.0, iniconfig 2.3.1, actions/setup-python 7.1.0).

## 0.4.0

A release for all disciplines, with a much simpler installation.

### Writing

- **All disciplines**: the discipline adapter was rewritten around 12 discipline families (humanities; law; economics and management; social sciences; education and psychology; medicine and public health; life sciences and agriculture; physics, chemistry and materials; mathematics and statistics; earth and environmental sciences; engineering; computer science and AI), with a general procedure for fields not listed.
- **New workflows for theses, research proposals and grant applications**: plans, expectations and completed work are kept apart, and track records and lists of outputs use only facts the author supplies.
- **New citation-format guide**: numeric, author–date and footnote systems, with key points of GB/T 7714, APA, IEEE, Vancouver, Chicago and others; format conversion uses only the metadata provided.
- **More research types**: quantitative observational and survey research, humanities and legal interpretation, case studies, and design and engineering implementation.
- **Expanded Chinese style guide**: colloquial wording, empty openers, stacked 的, Europeanized long sentences and other common problems; punctuation, numbers, units and Chinese abstracts; the statistical and everyday senses of 显著.
- **Expanded English style guide**: problems common in English written by Chinese-speaking authors (pluralized uncountable nouns, articles, empty openers, dangling modifiers and others) and the fidelity boundary for each.
- **More load-bearing language**: legal normative force (应当 / 可以 / 不得) and interpretive qualifiers in the humanities are now protected.
- New synthetic examples for economics, law, history and research proposals.

### Check scripts

- `fidelity_check.py` recognizes Chinese article and chapter numbers (such as “第十条” and “第3章”, treating “第十二条” and “第12条” as the same item), Chinese author–year citations (such as “（张三，2020）”) and titles in Chinese title marks (such as 《劳动合同法》).
- `manuscript_audit.py` counts numerals as words, no longer splits Latin words with diacritics (such as naïve), and counts CJK extension characters.
- The terminology map adds groups for statistics, medicine and public health, psychology and education, and economics and management, flagging concepts that must not be mixed, such as incidence vs prevalence, or 信度 vs 可靠性.

### Installation and documentation

- **One installation method**: the recommended route is to send a prompt to your AI agent, which runs the bundled `install_skill.py`. Running it yourself in a terminal uses the same script, and copies installed either way can be updated and removed safely.
- Supports Claude Code, Codex, Cursor, Grok Build and the newly added OpenCode.
- New `update --backup-existing`: an old copy that was made by hand, installed by another tool or modified is moved as a whole to a backup folder outside the skills directory (not deleted) and replaced by a managed copy.
- Install and update report the version (old and new on update) and list same-named copies in other directories that the same agent may load twice.
- Running the installer from a location reached through a system symlink, such as macOS `/tmp`, is no longer refused; symlinks inside the skills directory and the package are still refused.
- README rewritten with examples from several disciplines; the compatibility notes focus on the five supported agents and explain how to avoid duplicate installs.

## 0.3.0

- Keeps the three zones, the L1/L2/L3 tiers and the ledger of important changes, and unifies the rules for body-only output, insufficient evidence, author actions and citation retrieval.
- Distinguishes statistical evidence that was not supplied from tests that were not performed, correlation from causation, the author's original values from derived values, percentage points from relative percentages, and completed work from future plans.
- Introduces three depths (quick polish, standard revision and deep structural review) and a mapping from key claims to the location of their evidence.
- Adds adaptation and examples for theoretical, qualitative and review research; the author's terminology takes precedence.
- Improves the static fidelity comparison of numbers, units, comparisons, intervals, citations and LaTeX; results distinguish “unchanged within coverage”, “review needed” and “insufficient coverage”.
- Unifies UTF-8 input, `--json`, `--strict` and exit codes across the four manuscript scripts.
- Adds manifest-driven install, update, uninstall and export tooling that protects files the user has modified.
- The current version uses **AGPL-3.0-only**; rights and notices granted under the earlier MIT versions are retained, see the [licensing notes](docs/licensing.md).

## 0.2.0

Reframes the Skill around fidelity: how far a revision may move a sentence before it changes what the author is claiming, and how the author audits that.

- **Fidelity contract** in `SKILL.md`: locked zone, load-bearing language and free surface, with L1–L3 change tiers and a change ledger.
- New references for fidelity examples, submission materials, LaTeX and document formats, and whole-draft consistency.
- New `scripts/fidelity_check.py` and `scripts/manuscript_audit.py`.
- Reviewer-response guidance separates journal response letters from conference rebuttals; the field adapter, writing workflows and style guides were rewritten.

## 0.1.0

- Initial release: task routing, field adaptation, writing workflows, output templates, quality checklist, citation safety rules and style guides.
- Terminology, section-structure and repository lint helper scripts.
