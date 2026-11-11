# Contributing / 贡献指南

[中文](#中文) | [English](#english)

## 中文

欢迎改进写作规则、学科适配、术语表、合成示例、核查脚本和文档。所有贡献都应帮助作者把研究表达清楚，同时保留证据边界、作者术语与学术诚信。

### 基本原则

- **不编造。** 不添加虚构的文献、数据、数据集、伦理审批、作者贡献或研究行动；缺失信息用明确占位。
- **示例必须是合成材料。** 不包含私人稿件、未发表成果、真实审稿意见、个人信息或密钥；合成示例应明确标注。
- **不做检测规避。** 不添加绕过查重或 AI 检测、保证录用或保证结果的功能与表述。
- **有据可查。** 新增学科惯例、投稿政策或规范要求时，说明来源和适用范围，避免“所有期刊都要求”之类的泛化。
- **许可。** 你需要拥有贡献内容的相应权利，并同意以 **AGPL-3.0-only** 提供。详见 [许可说明](docs/licensing.md)。

### 适合贡献的内容

- **学科适配**：在 [field-adapter.md](skills/academic-writing-assistant/references/field-adapter.md) 补充某学科的写作惯例与常见审读问题。
- **术语**：在 [术语表](skills/academic-writing-assistant/assets/terminology-map.zh-en.json) 中添加词组，标明是等价写法、文风偏好还是不同概念。
- **示例**：在 [examples/](examples/) 添加合成示例，展示输入、预期输出与验收要点。
- **脚本**：修复核查脚本的漏检或误报，并附回归测试。

### 本地验证

需要 Python 3.9 及以上（推荐 3.12）。在虚拟环境中安装开发依赖后，于仓库根目录运行：

```sh
python -m pip install -r requirements-dev.txt
python -B -m pytest -q tests/
python -B skills/academic-writing-assistant/scripts/skill_lint.py .
```

新增随 Skill 分发的文件时，同步更新 [package-manifest.json](skills/academic-writing-assistant/package-manifest.json)。

### 发布新版本（维护者）

版本号写在 `SKILL.md` 的 `metadata.version`、`.codex-plugin/plugin.json`、`ROADMAP.md`、`docs/licensing.md` 和两份 `THIRD_PARTY_NOTICES.md` 中，发布前保持一致，并在 `CHANGELOG.md` 写明变化。合并到 main 后创建 `v<版本号>` 标签和 GitHub Release，并把下面命令生成的 `academic-writing-assistant.zip` 作为附件上传，供通过上传技能包安装的平台直接下载：

```sh
python -B scripts/install_skill.py export --destination /path/to/output/academic-writing-assistant --archive
```

### 提交 PR 前

- [ ] 保真契约（三区域、L1/L2/L3）与诚信边界没有被削弱。
- [ ] 新示例与资源是合成材料或有明确许可。
- [ ] 测试与 lint 已通过。
- [ ] `SKILL.md` 保持精简，详细规则放在 `references/`。
- [ ] 中英文 README、CHANGELOG 已按需同步，保留原 Logo。

## English

Contributions to writing rules, discipline adapters, terminology, synthetic examples, checking scripts and documentation are welcome. Every change should help authors express their research clearly while preserving evidence boundaries, author terminology and academic integrity.

- **Never fabricate** references, data, datasets, ethics approvals, author contributions or research actions; use explicit placeholders.
- **Examples must be synthetic** and clearly labeled. No private manuscripts, unpublished results, real review letters, personal data or credentials.
- **No detection evasion**, guaranteed acceptance or guaranteed results.
- **Cite your basis** for discipline conventions or venue policies, and state their scope.
- **License:** you must have the right to contribute the material under **AGPL-3.0-only**.

Run the checks with Python 3.9+ from the repository root:

```sh
python -m pip install -r requirements-dev.txt
python -B -m pytest -q tests/
python -B skills/academic-writing-assistant/scripts/skill_lint.py .
```

Keep `SKILL.md` lean, put detailed rules in `references/`, update the package manifest when adding distributed files, and keep both READMEs and the logo intact.

Maintainers: when publishing a release, keep the version consistent across the files listed in the Chinese section, tag `v<version>`, and attach the `academic-writing-assistant.zip` produced by `scripts/install_skill.py export --archive` to the GitHub Release.
