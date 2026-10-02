# 兼容说明 / Compatibility

本项目遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)：一个包含 `SKILL.md` 的文件夹，外加按需读取的 `references/`、`scripts/` 和 `assets/`。五个支持的 Agent 共用同一份 Skill，无需为不同平台维护不同版本。

## 支持的 Agent

安装脚本把 Skill 放到下表的**用户级目录**，在该 Agent 的所有项目中可用；用 `--destination` 放到**项目级目录**则只在该项目中生效。Windows 下 `~` 指 `%USERPROFILE%`。

| Agent | `--host` | 用户级目录 | 项目级目录 | 还会读取的用户级目录 | 调用方式 |
|---|---|---|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) | `claude` | `~/.claude/skills/` | `.claude/skills/` | — | `/academic-writing-assistant` 或自动调用 |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `codex` | `~/.agents/skills/` | `.agents/skills/` | `~/.codex/skills/`（旧目录） | `$academic-writing-assistant`、`/skills` 或自动调用 |
| [Cursor](https://cursor.com/docs/skills) | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` 或 `.agents/skills/` | `~/.agents/skills/`、`~/.claude/skills/`、`~/.codex/skills/` | 在 Agent 输入框输入 `/` 选择，或自动调用 |
| [Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces) | `grok-build` | `~/.grok/skills/` | `.grok/skills/` | `~/.agents/skills/`；也会读取 Claude Code 的 Skills | `/academic-writing-assistant` 或自动调用 |
| [OpenCode](https://opencode.ai/docs/skills/) | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | `~/.agents/skills/`、`~/.claude/skills/` | 描述任务后由 Agent 自动加载 |

说明：

- 目录与调用方式依据上表链接的官方文档（2026 年 10 月核对）。各产品更新较快，以其最新文档为准。
- 新装的 Skill 何时出现：Claude Code 在当前会话中即可识别（若 `~/.claude/skills/` 是新建的，运行 `/reload-skills`）；Codex 文档建议看不到时重启；其他 Agent 建议新开会话。
- 文件夹名必须保持为 `academic-writing-assistant`，与 `SKILL.md` 中的 `name` 一致。
- 其他支持 Agent Skills 的工具目前不在官方支持范围内。需要时可用安装脚本的 `--destination` 指定其 Skills 目录，但未经本项目验证。

## 避免重复安装

上表"还会读取"一列说明：同一份 Skill 可能被多个 Agent 看到。为多个 Agent 分别安装时，某些 Agent 中会出现两份同名 Skill。安装脚本会在输出的 `note` 中列出这类副本，但不会改动它们。

建议：

- 同时使用 Claude Code 与 Cursor / OpenCode / Grok Build：只装 `--host claude` 一份，其他几个都会读取它。
- 同时使用 Codex 与 Cursor / OpenCode / Grok Build：只装 `--host codex` 一份。
- 同时使用 Claude Code 与 Codex：需要两份（Codex 不读取 `~/.claude/skills/`，Claude Code 不读取 `~/.agents/skills/`）。Cursor 等可能显示两份，内容相同；更新时用两个 `--host` 分别 `update`，保持版本一致。
- 不要把旧版本改名后留在 Skills 目录里；`update --backup-existing` 会把旧副本移到 Skills 目录之外。

## 能力差异

Skill 的核心是文字指令，任何能加载 `SKILL.md` 的 Agent 都能完成写作任务。其他能力取决于 Agent 本身：

| Agent 提供的能力 | 可以做的事 | 没有该能力时 |
|---|---|---|
| 读取文件 | 按需读取 `references/` 中的详细规则、术语表和你的稿件 | 使用已加载的核心规则，并说明哪些资料未读取 |
| 运行 Python | 用 `scripts/` 中的脚本做数值、引用、术语的机械比对 | 继续文本层面核查，说明机械检查未执行 |
| 联网检索、解析文档 | 查证文献与投稿政策，读取 PDF、Word 等格式 | 给出检索方向与明确占位，不凭记忆编造来源 |

没有原生 Skills 功能的聊天工具，也可以手动上传或粘贴 `SKILL.md` 及当前任务需要的参考文件来使用。

## Python 与操作系统

核心写作不需要 Python。可选的核查脚本和安装工具只使用 Python 标准库，需要 **Python 3.9 或更新版本**（推荐 3.12），支持 macOS、Linux 和 Windows；持续集成在这三个系统上运行测试。

脚本在本地运行、不联网。本地脚本不联网并不代表云端模型不会接收你的稿件，请按所用平台和机构的数据政策选择提交的材料。

## Codex 插件包装

仓库保留了可选的 `.codex-plugin/plugin.json`，供需要插件形式的 Codex 环境使用。直接安装 Skill 文件夹不依赖它。
