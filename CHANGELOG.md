# 变更日志 / Changelog

## 0.3.0（Unreleased，未发布）

本节描述当前开发候选，不代表已经发布正式版本。历史版本记录见下方 0.2.0 与 0.1.0；未来方向统一维护在 [路线图](ROADMAP.md)。

### 写作与证据

- 保留三区域、L1/L2/L3 和重要改动台账，统一仅正文输出、语言路由、条件稿与作者确认规则。
- 明确区分统计依据未提供与未做检验、相关与因果、作者原值与推算值、百分点与相对百分比，以及已完成工作与未来计划。
- 引入按任务缩放的快速润色、标准修订和深度结构审阅，以及关键主张到实际证据位置的对应。
- 实际利用可读表格、全文与来源；按元数据、摘要、全文分别报告核验范围，检索遵守用户来源限制与外传授权。
- 增加理论、定性与综述适配及合成示例；作者术语优先，相关概念不再作为等价词直接统一。
- 修正摘要工作稿遗漏明确未完成状态的规则：仅正文也保留已知进度，不能由结果材料缺失推断研究未完成。
- 投稿政策按来源、年份、轨道和核验日期记录；声明与审稿回复不补造作者行为、伦理审批或未来承诺。

### 脚本与接口

- 改进数值、符号、单位、比较、区间、重复项、引用和 LaTeX 静态解析；报告来源位置、原文片段及部分上下文变化。
- 保真 JSON 保留原类别并新增 `_meta`（schema version 2）。结果区分 `UNCHANGED_WITHIN_COVERAGE`、`REVIEW_NEEDED` 与 `INSUFFICIENT`；无可检查项不再表示整稿通过。
- 四个稿件入口统一 UTF-8/BOM、标准输入、`--json`、`--strict` 和输入错误处理。保真前后文件最多一个可使用标准输入。
- 修正稿件审计中的正文提取、统计线索范围与计量边界；缩写提示不等于数学符号定义检查。自动时态审计未实现，显式 `--checks tense` 报告未检查，严格模式退出 1。
- 术语检查区分等价写法、文风偏好与相关概念，保留原文位置并改进重叠匹配；`--map` 使用完整自定义词表替换默认词表。
- 结构检查新增 `--research-type`，覆盖经验、理论、综述与定性研究；改进占位识别与长文本处理，关键词提示不构成质量评分。
- 保留旧章节与术语兼容入口。稿件脚本默认扫描完成退出 0，严格模式发现问题或覆盖不足退出 1，输入或运行错误退出 2；详见 [接口说明](docs/scripts.md)。

### 安装、测试与公开交付

- 增加显式包清单，以及安装、更新、卸载和独立导出工具；拒绝覆盖未知目标，按安装记录与文件内容保护已有改动。
- 以单一核心适配宿主路径和能力降级，分别报告官方说明、目录映射、原生发现与实际模型调用结果。未运行环境保留未验证状态。
- 增加确定性边界回归、固定开发依赖、最小权限 CI、SHA 固定的 Actions 和校验归档的密钥扫描配置。
- 增加工作树、暂存区与独立包交付守卫；私人资料、原始记录与公开文档分开管理，忽略规则不替代 Git 历史检查。
- 增加可复跑的合成行为评估协议与 [实际结果](evals/results-2026-09-10.md)。保留初始升级版 23 PASS / 1 FAIL 的原始 24 项结果，修复后定向验证另列，不据此宣称总体优于基线。
- 整理中文优先的公开文档、贡献与验证说明，合并重复路线图。平台与原生宿主测试边界见 [兼容矩阵](docs/compatibility.md)。

### 许可

- 当前候选采用 **AGPL-3.0-only**，独立 Skill 包包含许可及必要历史/第三方声明。
- 保留历史 MIT 版本已经授予的权利与必要版权声明。版本边界与外部材料说明见 [许可说明](docs/licensing.md) 和 [声明清单](THIRD_PARTY_NOTICES.md)。

## 历史记录说明

以下 0.2.0、0.1.0 内容按历史原文保留，不作为当前工具能力保证。旧条目中的“验证保留”、符号与时态检查等表述，须结合当前 [脚本覆盖边界](docs/scripts.md) 理解；例如自动时态审计未实现，机械比对不能证明全文科学语义。历史提及的 85 字符或其他投稿要求也不是所有 venue 的通用规则，使用前按 [政策来源](skills/academic-writing-assistant/references/policy-sources.md) 核查。

## 0.2.0

Reframes the Skill around fidelity: how far a revision may move a sentence
before it changes what the author is claiming, and how the author audits that.

### Added

- **Fidelity contract** in `SKILL.md`: locked zone / load-bearing language /
  free surface, with L1–L3 change tiers and a change ledger.
- `references/fidelity-protocol.md` — worked examples of the zones and tiers,
  including cases where an edit should not be made.
- `references/submission-package.md` — cover letters, highlights (85-character
  limit), generative-AI disclosure statements, CRediT contribution statements.
- `references/latex-and-formats.md` — editing `.tex` source without breaking
  `\cite{}`, `\ref{}`, math, or custom macros; Word and Markdown handling.
- `references/consistency-pass.md` — whole-draft terminology, abbreviation,
  symbol, tense, number, and claim-strength consistency.
- `scripts/fidelity_check.py` — verifies that citations, cross-references,
  numbers, math blocks, and macros survived a rewrite.
- `scripts/manuscript_audit.py` — abbreviation first-use, terminology drift,
  significance language without a test, unbounded claims, causal overreach,
  hedge stacking, tense mixing, and word/character limits.

### Changed

- `references/reviewer-response.md` now separates journal response letters from
  conference rebuttals, which differ in length budget, tense, and structure.
- `references/field-adapter.md` records what each field's reviewers attack
  rather than listing vocabulary; adds NLP/LLM and social sciences.
- `references/writing-workflows.md` rewritten around technique; adds
  compression to a limit.
- `references/style-guide-en.md` adds systematic Chinese-interference patterns.
- `references/style-guide-zh.md` adds thesis-versus-journal conventions.
- `references/task-router.md` covers bare-text input and requests to redirect.
- `scripts/structure_checker.py` adds related_work and conclusion sections,
  placeholder detection, and JSON output.
- `scripts/terminology_checker.py` reports occurrence counts and the dominant
  variant; the terminology map roughly doubles in coverage.
- READMEs rewritten in both languages, with the Revision Compass logo retained.

## 0.1.0

- Initial release.
- Academic Writing Assistant Skill with task routing, field adaptation, writing
  workflows, output templates, quality checklist, citation safety rules, and
  style guides.
- Terminology, section-structure, and repository lint helper scripts.
- Examples, tests, docs, and open-source governance files.
