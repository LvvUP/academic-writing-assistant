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
- [ ] 如果行为、安装方式或文档结构发生变化，README 和相关文档已同步更新。

### 添加新的研究领域

请在 `skills/academic-writing-assistant/references/field-adapter.md` 中添加对应领域小节，并至少说明：

1. 常见任务；
2. 写作重点；
3. 常用术语；
4. 需要避免的表述或结论。

如有必要，可以同时在 `assets/terminology-map.zh-en.json` 中添加术语条目，并在 `examples/` 下补充安全示例。

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
- [ ] README and related docs are updated if behavior, installation, or documentation structure changes.

### Adding a New Research Field

Add a field section to `skills/academic-writing-assistant/references/field-adapter.md` with:

1. common tasks;
2. writing focus;
3. common terms;
4. expressions or claims to avoid.

If useful, also add terminology entries to `assets/terminology-map.zh-en.json` and a safe example under `examples/`.
