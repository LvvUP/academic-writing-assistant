# 兼容说明 / Compatibility

本项目遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)：一个包含 `SKILL.md` 的文件夹，外加按需读取的 `references/`、`scripts/` 和 `assets/`。六个支持的平台共用同一份 Skill，无需为不同平台维护不同版本。

`SKILL.md` 的 frontmatter 只使用规范定义的字段：`name`（与文件夹同名）、`description`（不超过 1024 字符）、`license` 和 `metadata`。

## 支持的平台

### 安装到 Skills 目录的 Agent

安装脚本把 Skill 放到下表的**用户级目录**，在该 Agent 的所有项目中可用；用 `--destination` 放到**项目级目录**则只在该项目中生效。Windows 下 `~` 指 `%USERPROFILE%`。

| Agent | `--host` | 用户级目录 | 项目级目录 | 还会读取的用户级目录 | 调用方式 |
|---|---|---|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/skills) | `claude` | `~/.claude/skills/` | `.claude/skills/` | — | `/academic-writing-assistant` 或自动调用 |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `codex` | `~/.agents/skills/` | `.agents/skills/` | 见下方说明 | `$academic-writing-assistant`、`/skills` 或自动调用 |
| [Cursor](https://cursor.com/docs/skills) | `cursor` | `~/.cursor/skills/` | `.cursor/skills/` 或 `.agents/skills/` | `~/.agents/skills/`、`~/.claude/skills/`、`~/.codex/skills/` | 在 Agent 输入框输入 `/` 选择，或自动调用 |
| [Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces) | `grok-build` | `~/.grok/skills/` | `.grok/skills/` | `~/.agents/skills/`；也会读取 Claude Code 的 Skills | `/academic-writing-assistant` 或自动调用 |
| [OpenCode](https://opencode.ai/docs/skills/) | `opencode` | `~/.config/opencode/skills/` | `.opencode/skills/` | `~/.agents/skills/`、`~/.claude/skills/` | 自动加载，或在提示中写 `@academic-writing-assistant` |

### 通过上传技能包安装的平台

| 平台 | 安装方式 | 调用方式 |
|---|---|---|
| [WorkBuddy](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) | 用 `export --archive` 导出技能包，在「专家·技能·连接器 → 技能 → 添加技能 → 上传技能」中导入 | 在对话中直接提出写作任务；输入 `/` 可唤起技能列表 |

说明：

- 目录与调用方式依据上表链接的官方文档（2026 年 11 月 11 日核对）。各产品更新较快，以其最新文档为准。
- **Codex：** 官方文档列出的用户级目录是 `~/.agents/skills/`。早期版本使用的 `~/.codex/skills/` 已不在现行文档中，但 Cursor 的文档仍把它列为会读取的 Codex 目录；安装脚本会检查这个目录里是否有同名副本并提示，不会向其中写入。
- **WorkBuddy：** 各项说法的出处如下（均为 2026 年 11 月 11 日核对）。
  - [技能页](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)：自备的技能包需通过「添加技能 → 上传技能」导入；已安装的技能可在对话中直接调用；技能可以关闭，关闭后仍留在已安装列表中，但不参与新任务的调用。
  - [更新日志](https://www.codebuddy.cn/docs/workbuddy/Changelog)：技能描述取自 `SKILL.md` 的 frontmatter（4.24.2）；可以用 `/` 唤起技能列表（4.7.1）。
  - [权限说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes)：默认权限以工作空间为边界，所以安装提示词让它把技能包导出到当前工作空间。
  - **官方文档没有写明的：** 上传包的格式（压缩包还是文件夹、`SKILL.md` 放在哪一层），以及本地技能目录。本项目因此只提供技能包，不向 WorkBuddy 的本地目录写入文件；压缩包把 `SKILL.md` 放在第一层，并同时导出内容相同的文件夹。压缩包能否被接受、文件夹能否作为替代，都未经官方文档确认，也尚未在 WorkBuddy 客户端中逐版本验证。
- 新装的 Skill 何时出现：Claude Code 在当前会话中即可识别（若 `~/.claude/skills/` 是新建的，运行 `/reload-skills`）；Codex 会自动检测，看不到时重启；Cursor 在启动时发现 Skill；其他平台建议新开会话。逐个平台的确认方法见 [安装指南](installation.md#验证安装成功)。
- 文件夹名必须保持为 `academic-writing-assistant`，与 `SKILL.md` 中的 `name` 一致。
- 其他支持 Agent Skills 的工具目前不在官方支持范围内。需要时可用安装脚本的 `--destination` 指定其 Skills 目录，但未经本项目验证。

## 避免重复安装

上表“还会读取”一列说明：同一份 Skill 可能被多个 Agent 看到。为多个 Agent 分别安装时，某些 Agent 中会出现两份同名 Skill。安装脚本会在输出的 `note` 中列出这类副本，但不会改动它们。

建议：

- 同时使用 Claude Code 与 Cursor / OpenCode / Grok Build：只装 `--host claude` 一份，其他几个都会读取它。
- 同时使用 Codex 与 Cursor / OpenCode / Grok Build：只装 `--host codex` 一份。
- 同时使用 Claude Code 与 Codex：需要两份（Codex 不读取 `~/.claude/skills/`，Claude Code 不读取 `~/.agents/skills/`）。Cursor 等可能显示两份，内容相同；更新时用两个 `--host` 分别 `update`，保持版本一致。
- 不要把旧版本改名后留在 Skills 目录里；`update --backup-existing` 会把旧副本移到 Skills 目录之外。
- WorkBuddy 的技能由它自己管理，与上面这些目录互不影响。

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
