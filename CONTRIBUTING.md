# Contributing / 贡献指南

[中文](#中文) | [English](#english)

## 中文

欢迎改进写作规则、术语关系、合成示例、辅助脚本和文档。贡献应让作者更容易表达研究、核对重要改动，同时保留证据边界、作者术语与学术诚信。

### 贡献边界与许可

- 不编造文献、结果、数据集、伦理审批、作者贡献或已完成/计划的行动；缺失材料用明确占位。
- 示例和测试使用明确标注的合成材料，不包含私人稿件、真实审稿意见、参与者资料或凭据。不要添加未经授权的原文、图像或数据。
- 不添加绕过查重或检测、保证录用、保证科学结果或无来源宣传数字的功能和表述。
- 新贡献必须由你拥有相应权利，并有权以 **AGPL-3.0-only** 提供。保留必要版权、许可和第三方声明；引入外部材料前说明来源与适用许可，不能只替换许可头。
- 历史 MIT 版本已经授予的权利不因当前许可变更而撤销。当前贡献与旧版本的关系见 [许可说明](docs/licensing.md)、[LICENSE](LICENSE) 和 [第三方与历史声明](THIRD_PARTY_NOTICES.md)。

### 开发环境与验证

开发环境推荐 Python 3.12，最低兼容版本为 3.9；下方 `python3` 表示所选解释器。稿件检查与安装工具使用标准库，仓库 lint 需要 PyYAML，开发依赖固定在 [requirements-dev.txt](requirements-dev.txt)。在自己的虚拟环境安装依赖，在仓库根目录运行：

```sh
python3 -B -m venv .internal/dev-venv
# 按系统激活该虚拟环境后：
python3 -B -m pip install --only-binary=:all: -r requirements-dev.txt
python3 -B -m pytest -q -p no:cacheprovider tests/
python3 -B skills/academic-writing-assistant/scripts/skill_lint.py .
python3 -B scripts/check_delivery.py .
python3 -B scripts/check_delivery.py . --index
git diff --check
```

Windows 可使用所激活环境的 Python 解释器替换 `python3`。`-B` 避免产生安装目录内的字节码缓存；安装器会拒绝带未知额外文件的更新和卸载，不要为让测试通过而自动清理用户文件。

脚本或包接口发生变化时，先用有意义的输入复现问题，再验证结构化结果、来源位置、数量、退出码、输入保护和覆盖限制。涉及 Python 或文件系统兼容时执行相应环境的检查；配置了 CI 矩阵不等于它已实际通过。

独立包在新的临时目标检查，不能覆盖现有 Skill：

```sh
python3 -B scripts/install_skill.py export --destination .internal/export/academic-writing-assistant
python3 -B scripts/check_delivery.py .internal/export/academic-writing-assistant --package
python3 -B .internal/export/academic-writing-assistant/scripts/skill_lint.py .internal/export/academic-writing-assistant --package
```

目标已存在时另选未使用的目录。新增运行资源须同步 [包清单](skills/academic-writing-assistant/package-manifest.json)，并验证脱离仓库的实际读取与运行。完整安全扫描、图片人工检查、依赖与 CI 更新要求见 [测试说明](docs/testing.md)。

### 修改写作行为与添加领域资源

保持 [SKILL.md](skills/academic-writing-assistant/SKILL.md) 精简，详细规则按需放入 `references/`。三区域、L1/L2/L3 和台账是核心机制；变更它们时，在 PR 中说明具体问题、证据及作者可观察的结果。只检查规则字符串存在，不能证明模型正确遵循。

新增学科或研究类型时，说明实际写作问题、适用条件、术语与概念区别，提供有依据的来源或明确限定的经验，避免泛称“所有审稿人都要求”。作者术语优先；词表应区分等价写法、文风偏好和相关但不同概念。参考 [领域规则](skills/academic-writing-assistant/references/field-adapter.md)、[研究类型](skills/academic-writing-assistant/references/research-types.md) 与 [术语表](skills/academic-writing-assistant/assets/terminology-map.zh-en.json)。

重要行为变化依 [评估指南](evals/README.md) 做真实模型验证：固定双方的版本、输入、次序与判据，使用一致配置与独立评分。保留失败、覆盖不足和未运行，修复后的新验证单列，不能覆盖原结果。没有独立评审或实际模型调用时明确写明，不将自审、示例或脚本通过称为行为通过。

### 提交 PR 前

- [ ] 修改保留保真契约、引用与作者行为边界，短任务不增加无用报告。
- [ ] 新示例、测试和资源可公开且许可清楚，必要声明完整。
- [ ] 相关测试、lint、独立包检查与实际暂存内容守卫已执行，结果和未验证范围如实记录。
- [ ] 行为变化有适当评估与独立审查；未执行部分没有标为通过。
- [ ] 中文与英文 README、接口说明、CHANGELOG 和必要元数据同步，保留原 Logo。
- [ ] 实际审阅公开 diff 与待交付文件清单，没有私人正文、机器用户路径、原始会话或扫描日志。

开发记录放在明确忽略的 `.internal/` 或 `.local/`，公开 `docs/` 和合成测试继续纳入版本控制。忽略规则不移除已跟踪文件，也不清除历史；发现真实敏感信息时停止公开传播并按 [安全政策](SECURITY.md) 处理。守卫和密钥扫描提供的是有限检测，不能代替人工审阅。

PR 描述先说明解决的问题与最终行为，再给实际测试、评估和限制。不要提交原始会话、私密评分映射或扫描报告，也不要把尚未运行的平台称为兼容认证。

## English

Contributions should improve academic expression and make consequential changes easier to audit, without weakening evidence, terminology, citation, or author-action boundaries.

### Scope and licensing

Use clearly identified synthetic examples and tests. Do not contribute private manuscripts, real peer reviews, participant data, credentials, fabricated research claims, or material you lack permission to redistribute. Avoid detector-evasion features, publication guarantees, and unsupported promotional claims.

You must hold the rights needed to provide each new contribution under **AGPL-3.0-only**. Preserve required copyright, license, and third-party notices; identify the source and license of external material. Rights already granted for historical MIT versions are not revoked. See the [licensing guide](docs/licensing.md), [LICENSE](LICENSE), and [notices](THIRD_PARTY_NOTICES.md).

### Development and review

Python 3.12 is recommended for development; Python 3.9 is the minimum supported version. Use an isolated environment with the pinned [development requirements](requirements-dev.txt); `python3` denotes the selected interpreter. The commands in the Chinese section run tests, repository lint, worktree and staged-content delivery checks, then validate a standalone export. Manuscript checks and the installer use the standard library; development lint requires PyYAML. Use `python3 -B` to avoid creating caches inside an installed Skill. Choose a new export destination and preserve existing installations and user changes.

Keep the core Skill concise and detailed guidance in references. Preserve the three zones, L1/L2/L3, and the change ledger. New field guidance needs a stated scope and supporting sources or qualified experience; terminology must distinguish equivalents from related concepts and respect author definitions. Runtime resources belong in the explicit package manifest and must work outside the repository.

For substantive behavior changes, follow the [evaluation protocol](evals/README.md): fix versions, inputs, order, and criteria before running both versions under comparable settings, and obtain independent scoring. Retain failures and separate post-fix runs. Static checks, examples, self-review, and model self-reports do not establish successful behavior or independent review.

### Before opening a PR

- [ ] Preserve the fidelity contract and research integrity boundaries.
- [ ] Use publishable synthetic material with clear licensing and required notices.
- [ ] Run relevant tests, lint, standalone-package checks, and the delivery guard against the actual staged content.
- [ ] Report actual model evaluation and independent review, including failures and work not run.
- [ ] Update affected bilingual READMEs, interfaces, changelog, and metadata; retain the original logo.
- [ ] Review the public diff and file list for private content, machine-specific user paths, raw sessions, and scanner logs.

Keep internal records in `.internal/` or `.local/`, while public docs and synthetic tests remain tracked. Ignoring a path does not remove tracked content or Git history. Follow the [security policy](SECURITY.md) for real sensitive findings. In the PR, describe the concrete problem, resulting behavior, actual validation, and limits; do not upload raw evaluation sessions or scanning reports. See [testing](docs/testing.md) and the [compatibility matrix](docs/compatibility.md) for distinct verification scopes.
