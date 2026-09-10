# 0.3.0 升级验收记录

本记录区分脚本回归、模型行为、宿主加载和公开交付。`PASS` 只指列出的实际检查范围；未运行的项目不计入通过。原始日志、评估响应和内部审查记录保留本地，不作为公开附件。

## 版本与交付状态

- 基线：`6af0be1916b6ce6452fee2d1ddf053f37584380d`，插件版本 0.2.0；本次重新执行基线测试为 **45 PASS**，仓库 lint **PASS**。
- 升级：0.3.0 开发候选，分支 `codex/academic-writing-upgrade`。最终提交、PR 与远程验证状态将在公开交付后补记；目前为 **PENDING**。
- 本地原有用户改动检查：开始时目标仓库工作树干净；开发使用独立分支，未重置原主分支或清理相邻项目。

## 问题与回归覆盖

| 已处理范围 | 可复跑的测试 |
|---|---|
| 正负号、科学计数指数、单位、p 值、区间端点与运算关系；引用、公式、自定义宏和位置；跨行关系等未支持内容的覆盖提示 | `tests/test_fidelity_regressions.py`、`tests/test_numeric_relations.py` |
| 保留 LaTeX 正文，统计证据按局部论断检查，限定比较范围与因果提示 | `tests/test_manuscript_regressions.py` |
| UTF-8/BOM、stdin、无效输入、深层 JSON/YAML、受控退出、不修改原稿 | `tests/test_input_boundaries.py` |
| frontmatter、包内资源、硬链接/符号链接与不安全资源拒绝 | `tests/test_lint_regressions.py` |
| 术语类别和作者词表优先级、多种研究结构、长输入性能边界 | `tests/test_terms_structure_regressions.py` |
| 安装、更新、导出、卸载、冲突拒绝、路径与旧文件保护、故障恢复 | `tests/test_install_skill.py` |
| 工作树、实际 index blob、包清单、私人路径、凭据模式和未知二进制覆盖 | `tests/test_delivery_guard.py` |
| 公开资料、示例、Logo、兼容包装、版本与许可证一致性 | `tests/test_project_integrity.py`、`tests/test_scripts.py` |

这些检查会提示需要作者复核的位置，不认证科学语义、统计设计、引用支持关系或全文正确性。正文数值关系跨行时明确报告覆盖不足，严格模式返回 1，不能把仅有的项匹配当成关系已核对。最终审查的新回归曾在修复前实际失败，修复后重新验证；没有删除失败用例或降低判据来取得通过。

## 实际执行

本机为 macOS 15.7.3 / Darwin 24.6、arm64 主机，Python 3.9.6 进程通过 Rosetta 运行于 x86_64，另用 Python 3.12.14。最终脚本修复后的全量测试：Python 3.9.6 为 **519 PASS、0 FAIL、0 SKIP**（29.27 秒），Python 3.12.14 为 **519 PASS、0 FAIL、0 SKIP**（10.79 秒）。仓库/独立包 lint、官方 Skill/插件结构校验、actionlint 1.7.12 和差异空白检查均 **PASS**。远程 Ubuntu、Windows、macOS 矩阵在首次推送前为 **NOT RUN**。

复跑命令及固定依赖见 [测试指南](testing.md)。核心命令为：

```sh
python -B -m pytest -q -p no:cacheprovider tests/
python -B skills/academic-writing-assistant/scripts/skill_lint.py .
python -B scripts/check_delivery.py .
python -B scripts/check_delivery.py . --index
```

独立 Skill 导出按清单复制 **35 个文件**，与最终源包及隔离安装内容逐文件 SHA-256 一致。实际更新安装后，从无关工作目录运行已安装脚本，严格模式正确拦截合成数值关系变化，输入文件保持不变。核心稿件脚本使用标准库，开发 lint 另外需要 PyYAML。包检查与原生宿主运行分别记录，不能互相替代。

## 模型评估与宿主范围

实际模型评估共 **56 个响应、14 个执行上下文**。48 个原始响应中，基线 **24/24 PASS**，初始升级快照 **23 PASS、1 FAIL**；失败为 E04-R2 遗漏作者已知的“实验尚未完成”状态。另有成对独立上下文 E07/E15 共 4 个响应，以及修复后成对 E04 共 4 个响应，分别通过，但没有合并分母或覆盖原失败。

模型为记录到的 `gpt-6-astra`、推理强度 `ultra`；精确模型构建、temperature 和 seed 未暴露。方法限制、实际工具证据、快照摘要和原失败见 [完整评估记录](../evals/results-2026-09-10.md)。最终审查期间的脚本修复晚于冻结评估，没有声称在最终包上重跑全部模型任务，也不据此宣称整体效果优于基线。

最终候选在新隔离项目中的 Codex 原生 Skill 发现 **PASS**；既有 CLI 0.147.0 的模型调用实际 **FAILED（HTTP 400）**，触发后的写作行为 **NOT RUN**。Claude Code、Cursor、Grok Build 的目录规范与隔离映射经过核对，其原生模型流程 **NOT RUN**。详见 [宿主矩阵](compatibility.md)。

## README、Logo 与许可证

实际调用本机已安装的 `beautify-github-readme` 技能，在内容稳定后按其工作流维护中文首页和英文版。使用安装的 Chrome 152 与 Playwright 实际预览两种语言、浅/深色、960/360 像素视口共 8 个组合；图片加载、页面宽度、锚点、展开交互和浏览器错误检查通过，并逐段人工看图。该结果是本地 GitHub 宽度 Markdown 预览；GitHub 线上渲染在首次推送前为 **NOT RUN**。

保留原 SVG/PNG Logo，SHA-256 分别为：

- SVG：`989ad202c9977b4b205efb0bd2f36213eb29db84861e0056f70881647774e39a`
- PNG：`edda5c6be80b27047d58a6342e705552f02254f5c464abba74a714884455619e`

当前项目及独立包改为 **AGPL-3.0-only**；两份标准 LICENSE 一致，保留历史 MIT 授权及版权声明，未追溯撤销旧授权。已核对可访问贡献历史、原有资产和声明范围，未发现具体迁移障碍。开发依赖保留各自许可证，本检查不是完整供应链法律认证。详见 [许可证说明](licensing.md) 与 [第三方声明](../THIRD_PARTY_NOTICES.md)。

## 独立审查与安全范围

各阶段调用了真实独立 Agent 检查实际 diff、证据和文件清单。最终工程与学术审查发现了额外问题；修复后的学术复核 **PASS**，包含 18 个独立探针、4 个 CLI 组合，以及双 Python 各 105 个稿件回归。工程最终复核 **PASS**：双 Python 各 39 个数值/CLI/位置独立探针及 174 个相关回归；输入边界另有双 Python 各 22 个独立探针与 225 个相关回归。首次漏报和后续标点、跨行问题的失败证据均保留；作者自检不计为独立审查。

专业扫描使用 **Gitleaks 8.30.1**，结果只记录范围、退出状态和数量。首次历史检查覆盖非浅克隆的全部本地对象：15 个 commit、108 个 blob、49 个 tree，以及当时 origin 广告的全部分支与 PR ref；无 tag。实际执行 Git 历史扫描（该工具日志记录 13 个提交）和全部本地 blob/commit/tag 内容扫描（覆盖 15 个提交对象），均退出 **0**、**0 findings**。全部 30 个作者/提交者头部使用 GitHub noreply 地址；公共项目标识、公开服务的 noreply 归属及合法版权声明按上下文保留，没有将整个 tests 或 docs 加入允许列表。

已读取可访问历史 PR 正文和提交说明，检查专业扫描、私人路径与联系信息候选。唯一历史 PNG 与原 Logo 摘要相同；视觉检查和 PNG 元数据解析未发现私人文字、GPS 或作者信息。SVG 与新增本地徽章不含外部图片、脚本或追踪请求。

首次 GitHub 项目检查取得全部分页：1 个历史 PR，无普通 issue、评论、release、tag、Actions run 或 artifact，未发现附件 URL；当时无 CI 日志可下载。新增 PR 和 CI 日志须在公开后再次核对。Wiki Git 入口未取得可用仓库，属 **未验证**；其他人的 clone、不可访问或已删除的远程对象、缓存及云平台留存不在可证明的清除范围。

最终 35 文件导出包的 Gitleaks 扫描已退出 **0**、**0 findings**。工作树和实际暂存区各 **98 个公开文件**，交付守卫与各自快照的 Gitleaks 扫描均 **PASS**，无待分类命中；公开文件均为普通单链接文件。`.internal/` 与 `.local/` 的实际 Git 跟踪清单为空，35 文件包不含内部资料。提交创建后的新增对象与待推送补丁将在首次推送前再扫描，当前 **PENDING**。`.internal/`、`.local/` 是明确的忽略目录；没有忽略整个 `docs/`。加入 ignore 不表示清除了历史。

本地检查脚本不主动联网；宿主云模型如何处理稿件是独立问题。漏洞报告入口的实际状态和可用流程见 [SECURITY.md](../SECURITY.md)。

## 远程交付

开发分支推送、PR、远程 CI、简介/topics 读取验证和最终工作树状态目前 **PENDING**，将按真实结果更新。主分支合并、正式版本发布、历史重写、强制推送和可见性修改不在本次执行动作中。
