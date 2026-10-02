# 兼容说明 / Compatibility

本项目遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)：一个包含 `SKILL.md` 的文件夹，外加按需读取的 `references/`、`scripts/` 和 `assets/`。所有支持该规范的 AI Agent 共用同一份 Skill，无需为不同平台维护不同版本。

## 各 Agent 的 Skills 目录

把 `skills/academic-writing-assistant/` 整个文件夹放到下表中的**用户级目录**，即可在该 Agent 的所有项目中使用；放到**项目级目录**则只在该项目中生效。Windows 下 `~` 指 `%USERPROFILE%`。

| Agent | 用户级目录 | 项目级目录 | 调用方式 |
|---|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | `/academic-writing-assistant` 或自动调用 |
| Codex | `~/.agents/skills/` | `.agents/skills/` | `$academic-writing-assistant`、`/skills` 或自动调用 |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` | 在 Agent 输入框输入 `/` 选择，或自动调用 |
| Grok Build | `~/.grok/skills/` | `.grok/skills/` | `/academic-writing-assistant` 或自动调用 |
| WorkBuddy | `~/.workbuddy/skills/` 或 `~/.codebuddy/skills/` | `.codebuddy/skills/` | 对话中自动调用；也可在应用内技能市场上传技能包 |
| CodeBuddy | `~/.codebuddy/skills/` | `.codebuddy/skills/` | 自动调用 |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` | 自动调用 |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` | `/academic-writing-assistant` 或自动调用 |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | 自动调用 |
| Windsurf | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` | `@academic-writing-assistant` 或自动调用 |
| Kiro | `~/.kiro/skills/` | `.kiro/skills/` | `/academic-writing-assistant` 或自动调用 |
| Cline | `~/.cline/skills/` | `.cline/skills/` | `/academic-writing-assistant` 或自动调用 |
| Roo Code | `~/.roo/skills/` | `.roo/skills/` | 自动调用 |
| Trae / Trae CN | `~/.trae/skills/` / `~/.trae-cn/skills/` | `.trae/skills/` | 自动调用 |
| Qoder | `~/.qoder/skills/` | `.qoder/skills/` | 自动调用 |
| 其他支持 Agent Skills 的工具 | 多数读取 `~/.agents/skills/` | `.agents/skills/` | 以该工具文档为准 |

说明：

- 各产品更新较快，目录与调用方式以其官方文档为准。WorkBuddy 官方文档说明会加载用户级 `.codebuddy` 配置中的技能，社区教程多使用 `~/.workbuddy/skills/`；如果放入后没有出现在技能列表中，换另一个目录并重启 WorkBuddy。Trae、Qoder 的目录参照 [skills CLI](https://github.com/vercel-labs/skills) 的约定。
- 新放入的 Skill 通常需要新开会话，部分 Agent 需要重启后才会出现在列表中。
- 文件夹名必须保持为 `academic-writing-assistant`，与 `SKILL.md` 中的 `name` 一致。

## 避免重复安装

不少 Agent 会同时读取多个目录。例如 Cursor 也会读取 `~/.claude/skills/`，GitHub Copilot、Grok Build、OpenCode 等也会读取 `~/.agents/skills/`。如果你为多个 Agent 分别安装，某个 Agent 中可能出现两份同名 Skill。

建议：

- 只在实际使用的 Agent 目录中安装一份；需要多个 Agent 共用时，优先放在它们都会读取的目录。
- 更新时直接替换原文件夹。备份旧版本时，把它移到**所有 Skills 目录之外**，不要在 Skills 目录里保留改名的副本。

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
