# Contributing / 贡献指南

[中文](#中文) | [English](#english)

## 中文

欢迎为 Academic Writing Assistant 做贡献。

这个项目欢迎谨慎、可验证、符合学术诚信的改进。好的贡献应该让这个 Skill 更有用，同时不削弱它对证据边界、术语一致性和学术诚信的约束。

### 可以贡献什么

- 补充或改进领域适配规则。
- 添加术语对照、术语一致性检查规则和常见不一致模式。
- 优化常见学术写作任务的输出模板。
- 添加安全示例，避免包含私人、敏感或未公开论文内容。
- 改进辅助脚本和测试。
- 改进安装、使用和贡献文档。

### 不接受的内容

- 虚构参考文献、数据集、实验结果或评价指标。
- 鼓励无依据结论、代写论文或绕过学术诚信检查的功能。
- 包含私人信息、敏感数据或未公开稿件内容的示例。
- 没有证据支持的官方认证、用户数量、下载量或 star 数声明。
- 承诺发表论文、保证审稿通过或保证学术结果的表述。

### Pull Request 检查清单

在提交 PR 前，请确认：

- [ ] 修改没有削弱学术诚信边界。
- [ ] 新示例使用安全样本文本，必要时使用占位符。
- [ ] 新增术语条目包含简短说明。
- [ ] `SKILL.md` 保持简洁；详细规则放在 `references/` 中。
- [ ] `python -m pytest tests/` 可以通过。
- [ ] `python skills/academic-writing-assistant/scripts/skill_lint.py .` 可以通过。
- [ ] 如果行为、安装方式或文档结构发生变化，README 和相关文档已同步更新。

### 添加新的研究领域

请在 `skills/academic-writing-assistant/references/field-adapter.md` 中添加对应领域小节，并至少说明：

1. **该领域审稿人会攻击什么**——这是最有价值的部分。遥感审稿人问地理泛化，
   临床审稿人问外部验证，NLP 审稿人问数据污染。知道会被问什么，比知道该领域
   的词汇有用得多；
2. 需要警惕的具体表述（哪些写法会引来质疑）；
3. 常用术语。

写这部分时请基于你在该领域投稿或审稿的实际经验。凭印象拼凑的"审稿人关注点"
比没有更糟，因为它会误导作者把精力放在错误的地方。

如有必要，可以同时在 `assets/terminology-map.zh-en.json` 中添加术语条目
（每条需附说明），并在 `examples/` 下补充安全示例。

### 修改保真契约

`SKILL.md` 中的三区域（锁定区 / 承重语言 / 自由表层）与 L1/L2/L3 分级是整个
Skill 的核心机制，测试与 lint 都会检查它们的存在。如果你认为某处需要调整，
请在 PR 描述中说明理由——这部分改动会被仔细审阅。

## English

Thank you for considering a contribution to Academic Writing Assistant.

This project welcomes careful, verifiable, academically responsible improvements. Strong contributions make the Skill more useful without weakening its boundaries around evidence, terminology consistency, and research integrity.

### Ways to Contribute

- Add or improve field adaptation rules.
- Add terminology pairs, consistency checks, and inconsistency patterns.
- Improve output templates for common academic writing tasks.
- Add safe examples that do not include private, sensitive, or unpublished research content.
- Improve helper scripts and tests.
- Improve documentation for installation, usage, and contribution workflows.

### What We Do Not Accept

- Fake references, datasets, experiments, or evaluation metrics.
- Features that encourage unsupported claims, paper ghostwriting, or evasion of academic integrity checks.
- Examples containing private information, sensitive data, or unpublished manuscript content.
- Claims of official certification, user counts, download counts, or star counts without evidence.
- Wording that promises publication, review acceptance, or guaranteed academic outcomes.

### Pull Request Checklist

Before opening a PR:

- [ ] The change preserves academic integrity guardrails.
- [ ] New examples use safe sample text and placeholders where needed.
- [ ] New terminology entries include a short note.
- [ ] `SKILL.md` remains concise; detailed rules live in `references/`.
- [ ] `python -m pytest tests/` passes.
- [ ] `python skills/academic-writing-assistant/scripts/skill_lint.py .` passes.
- [ ] README and related docs are updated if behavior, installation, or documentation structure changes.

### Adding a New Research Field

Add a field section to `skills/academic-writing-assistant/references/field-adapter.md` with:

1. **What reviewers in that field attack.** This is the most valuable part.
   Remote sensing reviewers ask about geographic generalization, clinical
   reviewers about external validation, NLP reviewers about data contamination.
   Knowing what a field asks is far more actionable than knowing its vocabulary.
2. Specific phrasings to watch for — what wording invites a reviewer question.
3. Common terminology.

Write this from actual experience submitting to or reviewing for the field.
Invented "reviewer concerns" are worse than none, because they send authors to
spend effort in the wrong place.

If useful, also add terminology entries to `assets/terminology-map.zh-en.json`
(each needs an explanatory note) and a safe example under `examples/`.

### Changing the fidelity contract

The three zones (locked / load-bearing / free surface) and the L1/L2/L3 tiers in
`SKILL.md` are the mechanism the whole Skill rests on, and both the tests and
the lint script check that they are present. If you believe something there
needs to change, explain the reasoning in the PR description — those changes get
close review.
