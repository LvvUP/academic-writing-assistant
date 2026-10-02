# 变更日志 / Changelog

## 0.4.0

面向所有学科的通用版本，并大幅简化安装。

### 写作能力

- **全学科适配**：学科适配重写为 12 个学科大类（人文、法学、经管、社科、教育心理、医学与公共卫生、生命科学与农学、理化材料、数学统计、地球环境、工程、计算机与人工智能），并给出未列学科的通用流程。
- **新增学位论文、开题报告与基金申请书工作流**：区分计划、预期与已完成，研究基础与成果清单只使用作者提供的事实。
- **新增引用格式指南**：顺序编码、作者—年份、脚注体系，GB/T 7714、APA、IEEE、Vancouver、Chicago 等常见要点；格式转换只使用已提供的元数据。
- **研究类型扩展**：新增定量观察与调查、人文与法学阐释、案例研究、设计与工程实现四类。
- **中文写作指南扩充**：口语化、空泛开头、“的”字堆叠、欧化长句等常见问题；标点、数字、单位与中文摘要要点；“显著”的统计含义与日常含义。
- **英文写作指南扩充**：中文作者常见英文问题（不可数名词复数、冠词、空泛开头、悬垂修饰等）及对应的保真边界。
- **承重语言补充**：法律规范效力（应当/可以/不得）、人文阐释性限定纳入保护范围。
- 新增经济学、法学、历史学、开题报告的合成示例。

### 核查脚本

- `fidelity_check.py` 识别中文法条与章节序号（如“第十条”“第3章”，并将“第十二条”与“第12条”视为同一项）、中文作者—年份引用（如“（张三，2020）”）和书名号标题（如《劳动合同法》）。
- `manuscript_audit.py` 的词数统计将数字计为词，带重音符号的拉丁字母词（如 naïve）不再被拆分，CJK 扩展区汉字计入字数。
- 术语表新增统计、医学与公共卫生、心理与教育、经济与管理词组，提示“发病率/患病率”“信度/可靠性”等不应混用的概念。

### 安装与文档

- 推荐用一段提示词让 AI Agent 自行安装；同时支持 `npx skills`、安装脚本和手动复制。
- `install_skill.py` 新增 WorkBuddy、CodeBuddy、Gemini CLI、GitHub Copilot、OpenCode、Trae、Qoder、Kiro、Windsurf 的安装目录。
- README 重写，示例覆盖多个学科；兼容说明覆盖 Claude Code、Codex、Cursor、Grok Build、WorkBuddy 等常见 Agent，并说明如何避免重复安装。

## 0.3.0

- 保留三区域、L1/L2/L3 与重要改动台账，统一“只输出正文”、证据不足、作者行为和引用检索的规则。
- 区分统计依据未提供与未做检验、相关与因果、作者原值与推算值、百分点与相对百分比、已完成工作与未来计划。
- 引入快速润色、标准修订和深度结构审阅三种力度，以及关键主张到证据位置的对应。
- 增加理论、定性与综述研究的适配和示例；作者术语优先。
- 改进数值、单位、比较、区间、引用和 LaTeX 的静态保真比对；结果区分“覆盖范围内未变”“需要核对”“覆盖不足”。
- 统一四个稿件脚本的 UTF-8 输入、`--json`、`--strict` 与退出码。
- 增加清单驱动的安装、更新、卸载与导出工具，保护用户已修改的文件。
- 当前版本采用 **AGPL-3.0-only**；保留历史 MIT 版本已授予的权利与声明，见 [许可说明](docs/licensing.md)。

## 0.2.0

Reframes the Skill around fidelity: how far a revision may move a sentence
before it changes what the author is claiming, and how the author audits that.

- **Fidelity contract** in `SKILL.md`: locked zone / load-bearing language /
  free surface, with L1–L3 change tiers and a change ledger.
- New references for fidelity examples, submission materials, LaTeX and
  document formats, and whole-draft consistency.
- `scripts/fidelity_check.py` and `scripts/manuscript_audit.py`.
- Reviewer-response guidance separates journal response letters from
  conference rebuttals; field adapter, writing workflows and style guides
  rewritten.

## 0.1.0

- Initial release: task routing, field adaptation, writing workflows, output
  templates, quality checklist, citation safety rules and style guides.
- Terminology, section-structure and repository lint helper scripts.
