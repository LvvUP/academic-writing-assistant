# 安装、更新与卸载

核心写作只需要你的 AI Agent 能加载 `SKILL.md`。下面四种方式任选其一；各 Agent 的目录见 [兼容说明](compatibility.md)。

## 方式一：让 Agent 自己安装（推荐）

把下面这段话发给你的 Agent：

```text
请帮我安装（已安装则更新）学术写作 Skill「academic-writing-assistant」。
来源：https://github.com/LvvUP/academic-writing-assistant （main 分支），只需要其中的 skills/academic-writing-assistant/ 文件夹。
1. 判断你运行在哪个 Agent，确定它的用户级 Skills 目录（Windows 下 ~ 即 %USERPROFILE%）。参考：
   Claude Code ~/.claude/skills · Codex ~/.agents/skills · Cursor ~/.cursor/skills · Grok Build ~/.grok/skills
   WorkBuddy ~/.workbuddy/skills 或 ~/.codebuddy/skills（以你实际加载的为准）· Gemini CLI ~/.gemini/skills · GitHub Copilot ~/.copilot/skills
   其他 Agent 以其官方文档为准（多数支持 ~/.agents/skills）；无法确定时先问我，不要猜。
2. 用 git clone --depth 1 或下载 ZIP 到临时目录，把该文件夹完整复制为“Skills 目录/academic-writing-assistant/”，文件夹名保持不变。不要运行仓库里的脚本，不要使用 sudo。
3. 如果目标位置或你会读取的其他 Skills 目录里已有同名 Skill，先告诉我旧版本号，把旧文件夹移到所有 Skills 目录之外备份，再放入新版，避免出现两份。
4. 完成后确认 SKILL.md 存在并删除临时目录，告诉我安装路径、版本号、是否需要重启或新开会话，以及调用方式。
```

**更新：** 再发送一次同样的提示词。**卸载：** 让 Agent 删除对应 Skills 目录中的 `academic-writing-assistant` 文件夹。

## 方式二：skills CLI（一条命令，多种 Agent）

需要 Node.js。[skills](https://github.com/vercel-labs/skills) 是一个开源的跨 Agent 安装工具，运行后可选择要安装到哪些 Agent：

```sh
npx skills add LvvUP/academic-writing-assistant -g
```

- `-g` 安装到用户级目录；省略则安装到当前项目。
- `-a` 指定 Agent，例如 `-a claude-code codex cursor`。
- 更新：`npx skills update`；卸载：`npx skills remove academic-writing-assistant`。具体参数以该工具的说明为准。

## 方式三：仓库自带的安装脚本

需要 Python 3.9 或更新版本。脚本只使用标准库、不联网，会记录安装清单，以便安全地更新和卸载：

```sh
git clone https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

| `--host` | 安装位置（相对于 `--home-root`） |
|---|---|
| `claude` | `.claude/skills/academic-writing-assistant` |
| `codex` | `.agents/skills/academic-writing-assistant` |
| `cursor` | `.cursor/skills/academic-writing-assistant` |
| `grok-build` | `.grok/skills/academic-writing-assistant` |
| `workbuddy` | `.workbuddy/skills/academic-writing-assistant`（若 WorkBuddy 未识别，可改用 `codebuddy`） |
| `codebuddy` | `.codebuddy/skills/academic-writing-assistant` |
| `gemini` | `.gemini/skills/academic-writing-assistant` |
| `copilot` | `.copilot/skills/academic-writing-assistant` |
| `opencode` | `.config/opencode/skills/academic-writing-assistant` |
| `trae` / `trae-cn` | `.trae/skills/…` / `.trae-cn/skills/…` |
| `qoder` | `.qoder/skills/academic-writing-assistant` |
| `kiro` | `.kiro/skills/academic-writing-assistant` |
| `windsurf` | `.codeium/windsurf/skills/academic-writing-assistant` |

安装到项目目录或其他位置时，用 `--destination` 指定完整路径（路径末尾必须是 `academic-writing-assistant`）：

```sh
python3 -B scripts/install_skill.py install \
  --destination "/path/to/project/.claude/skills/academic-writing-assistant"
```

更新与卸载（先在仓库中 `git pull` 获取新版本）：

```sh
git pull --ff-only
python3 -B scripts/install_skill.py update --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py uninstall --host claude --home-root "$HOME"
```

Windows 可用 `python` 或 `py -3` 代替 `python3`，`--home-root` 使用 `%USERPROFILE%`。

**安全保护：**

- 目标已存在时拒绝安装，不会覆盖已有文件夹。
- 更新与卸载前逐一核对安装记录中的文件哈希；你修改过或新增的文件会让操作停止，不会被覆盖或删除。
- 拒绝符号链接、Windows 目录联接和 `..` 路径；不需要 `sudo`。
- 只复制 [包清单](../skills/academic-writing-assistant/package-manifest.json) 列出的文件，不包含测试、文档或缓存。

脚本只管理由它自己安装的副本。用提示词、skills CLI 或手动复制安装的副本，请用相同方式更新；如果想改用脚本管理，先把旧副本移到所有 Skills 目录之外，再用脚本重新安装。

## 方式四：手动安装

1. 下载仓库（`git clone` 或在 GitHub 页面下载 ZIP）。
2. 把 `skills/academic-writing-assistant/` **整个文件夹**复制到对应 Agent 的 Skills 目录。只复制 `SKILL.md` 会缺少参考规则和脚本。
3. 新开会话或重启 Agent。

## 常见问题

- **Agent 里看不到这个 Skill：** 确认路径为 `Skills 目录/academic-writing-assistant/SKILL.md`，文件夹名没有被改动；然后新开会话或重启 Agent。
- **出现两份同名 Skill：** 有些 Agent 会读取多个目录，见 [避免重复安装](compatibility.md#避免重复安装)。
- **安装脚本提示目标已存在：** 说明该位置已有副本。请先确认它的来源并自行备份，脚本不会自动覆盖。
- **安装脚本提示有额外文件或 `__pycache__`：** 运行脚本时 Python 可能生成缓存。确认后把这些文件移出 Skill 目录再重试；日常运行脚本时加 `-B` 可避免生成缓存。
- **没有 Python：** 不影响写作功能，只是无法运行可选的机械核查脚本。

## English quick start

Paste the install prompt from the [README](../README_EN.md#-install) into your agent, or run `npx skills add LvvUP/academic-writing-assistant -g`, or use the bundled installer:

```sh
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

The installer refuses existing destinations, verifies file hashes before update and uninstall, rejects symlinks and copies only the files listed in the package manifest. Copies installed by prompt, the skills CLI or by hand should be updated the same way they were installed.
