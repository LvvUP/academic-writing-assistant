# 宿主兼容与验证范围

本项目使用一个 [Agent Skills 开放规范](https://agentskills.io/specification) 核心包，宿主按实际能力加载同一份指令。官方支持、机器上存在某个版本、安装文件复制成功和真实模型行为是不同结论。

核验日期：**2026-09-10**。下表中的版本来自实际本机版本命令；原生加载或写作行为没有执行的项目明确保留 **NOT RUN**。

## 宿主矩阵

| 宿主 / 本机版本 | 官方加载与调用 | 已实际检查 | 原生加载 / 行为范围 |
|---|---|---|---|
| Codex CLI **0.147.0** | 项目 `.agents/skills`、个人 `~/.agents/skills`；`$academic-writing-assistant` 或 Skill 选择入口 | 版本命令；隔离安装及脚本运行；原生 `skills/list` 返回已安装文件的准确路径 | 原生发现 **PASS**；模型调用 **FAILED（HTTP 400）**，写作行为 **NOT RUN** |
| Claude Code **2.1.233** | 项目 `.claude/skills`、个人 `~/.claude/skills`；`/academic-writing-assistant` | 版本命令；安装工具的目录映射使用显式隔离主目录测试 | Claude 原生发现、触发与模型行为 **NOT RUN** |
| Cursor **3.18.25** | 项目 `.cursor/skills`、个人 `~/.cursor/skills`，官方也支持 `.agents/skills`；Agent 输入 `/` 选择 Skill | 已安装应用及其内置 CLI 版本；安装目录映射测试 | Cursor 原生发现、触发与模型行为 **NOT RUN** |
| **Grok Build** 官方编码 Agent；本机未发现 CLI | 项目 `.grok/skills`、个人 `~/.grok/skills`；`/academic-writing-assistant` | 官方文档核对；安装目录映射测试 | 产品版本、原生安装/发现/触发与模型行为 **NOT RUN** |
| Grok 网页聊天、模型 API、第三方同名 CLI | 不能由 Grok Build 的文档推导原生 Skills 支持；可手动载入文本 | 没有原生支持验证 | 原生支持 **未核实**；文件读取、Python、检索均按实际能力决定 |

Codex 原生发现最初使用许可与版本元数据更新前的冻结升级包；最终脚本修复后，又在新的隔离 Git 项目中实际安装、更新和复测。最终源包、35 文件导出包及安装内容逐文件 SHA-256 一致。按 `skills/list` 返回的实际 `SKILL.md` 路径匹配，得到 `scope=repo`、`enabled=true`，对应 cwd 的 `errors=[]`。返回名称实际为 `academic-writing-assistant:academic-writing-assistant`；入口可能显示限定名称，应选实际返回项，不能仅比较裸名称后判定未加载。默认进程配置即能发现；早期临时信任覆盖的复测结果一致，并非安装必需步骤。

另一次原生模型调用使用本机既有 `gpt-6-astra` 配置，服务返回 HTTP 400，指出该模型需要更新的 Codex。该调用 **FAILED**，没有生成可评估的写作结果，故触发后的指令遵循与模型行为仍为 **NOT RUN**。本次未升级 CLI、替换模型或把发现成功等同于写作能力通过；其余开发及文件系统检查继续执行。

本次未为任何宿主修改全局设置、覆盖已有 Skill 或开启云端同步。目录映射测试在临时目录中完成，不是启动了四种宿主的安装测试。Cursor 应用确实存在；其 CLI 不在普通 PATH 中，不等于没有安装。

另在当前 Codex Agent 会话中对冻结的 Skill 文件进行了[真实模型行为评估](../evals/results-2026-09-10.md)。该执行环境与上述旧版 CLI 分开记录；其结果不替代 Claude Code、Cursor 或 Grok Build 的原生测试，也不将 CLI 的 HTTP 400 改报为通过。

官方依据：

- [Codex Skills](https://learn.chatgpt.com/docs/build-skills)：当前推荐 `.agents/skills`；`agents/openai.yaml` 属于 OpenAI 的可选扩展。原生发现使用 [App Server 的 `skills/list`](https://learn.chatgpt.com/docs/app-server)；加载元数据与模型回合是不同检查。
- [Claude Code Skills](https://code.claude.com/docs/en/skills)：个人与项目目录、斜杠调用及自动匹配方式。
- [Cursor Skills](https://cursor.com/docs/skills)：Skill 发现目录、Agent 调用入口和云端相关设置应分别核对。
- [Grok Build 概览](https://docs.x.ai/build/overview)与 [Skills / Plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces)：说明的是官方编码 Agent 的加载机制，不能推广为所有 Grok 产品能力。

## Codex 旧目录与可选插件

旧版 `~/.codex/skills` 是兼容路径，本机 Codex 会话仍能发现其中已安装的其他技能；这不是本项目升级包已经验证加载的证据。新安装优先 `.agents/skills`。不要为了“迁移”自动删除旧目录，也不要在两个作用域保留未经核对的重复副本。

仓库保留 `.codex-plugin/plugin.json` 可选兼容包装；直接安装 Skill 不依赖该包装、仓库 README 或测试目录。官方 [插件构建文档](https://learn.chatgpt.com/docs/build-plugins) 区分兼容布局与新的根目录 `plugin.json` 布局，不应混用字段和校验结论。插件文件的结构校验不代表发布目录审核或实际插件执行通过。

## Python 与文件系统

安装/导出工具和四个稿件检查脚本使用标准库，最低语法与 API 要求为 **Python 3.9**。独立包携带必要模块、参考资料、词表、公开文件清单、许可证和历史许可声明。`skill_lint.py` 属于开发校验，需要额外的 PyYAML；这不影响核心文本写作。

新环境建议 Python 3.12；Python 3.9 已于 2025-10-31 结束上游维护，保留其测试仅用于最低兼容范围（[官方版本状态](https://devguide.python.org/versions/)）。

本阶段实际在 **macOS / Darwin 24.6.0、arm64 主机**执行；**Python 3.9.6 解释器通过 Rosetta 运行，进程架构为 x86_64**，另有 Python 3.12.14 回归验证。已完成临时隔离的安装→更新→导出→包 lint→卸载，以及从无关工作目录运行已安装脚本。没有改变 `HOME` 或 `CODEX_HOME`。输入稿件为明确合成文本。

| 文件系统范围 | 状态 |
|---|---|
| macOS 本地安装生命周期及变更保护 | **PASS**：真实临时目录测试 |
| 暂存写入 ENOSPC、发布冲突、恢复原安装 | **PASS**：故障注入用例；不等于断电恢复认证 |
| Windows 不覆盖目标的发布分支 | **PASS（模拟分支）**：模拟 Windows 的 rename 约束；原生 Windows **NOT RUN** |
| Linux 文件系统生命周期 | **NOT RUN**：本阶段未在 Linux 执行 |

安装器不编译或执行源包来获得正文，不运行用户宏，不使用 `shell-escape`。严格拒绝安装目录内额外文件；普通 Python 生成的缓存也会阻止更新/卸载。测试已覆盖这种拒绝与文件保留，处理方式见 [安装排障](installation.md#核查与排障)。

## 能力降级

| 宿主实际提供的能力 | 可执行范围 | 不得宣称 |
|---|---|---|
| 指令和文本 | 写作、翻译、可见文本的语义核对 | 已运行 Python 或看过未加载资源 |
| 本地文件读取 | 读取需要的 references、词表、稿件和实际可解析附件 | 已核对未解析的 PDF 图片、表格或 Word 修订层 |
| Python 执行 | 对真实前后文件运行机械检查，并报告实际范围 | 零差异已经证明全文科学语义或引用支持关系正确 |
| 授权检索 / 文档解析 | 核对已读文献与政策，注明对象、版本、读取范围 | 搜索摘要等于全文证据，或检索授权等于允许上传私人稿件 |

这些能力可以组合；有检索能力并不要求先有 Python。没有原生 Skills 的宿主可手动加载 `SKILL.md` 和当前任务所需参考文件，但按需加载、文件执行与调用语法仍可能不同，应准确报告。

本地脚本不主动联网不代表宿主云模型不会接收稿件。作者仍需结合所用平台与账户的数据处理设置选择可以提交的材料；检索只使用必要非敏感信息。
