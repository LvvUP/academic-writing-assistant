# 安装、更新与卸载

本项目只有一种安装方式：仓库自带的 `scripts/install_skill.py`。你可以让 AI Agent 替你运行它，也可以自己在终端运行，两者装出来的副本完全一样，都能安全地更新和卸载。

支持 **Claude Code、Codex、Cursor、Grok Build、OpenCode**。安装脚本需要 Python 3.9 或更新版本，只使用标准库，不联网。各 Agent 的目录与调用方式见 [兼容说明](compatibility.md)。

## 让 Agent 替你安装（推荐）

把下面这段话发给你的 Agent：

```text
请帮我安装（已安装则更新）学术写作 Skill「academic-writing-assistant」，全程只用仓库自带的安装脚本：
1. 判断你是哪个 Agent，确定 --host：Claude Code → claude，Codex → codex，Cursor → cursor，Grok Build → grok-build，OpenCode → opencode。不是这五个就告诉我并停止。
2. 把 https://github.com/LvvUP/academic-writing-assistant（main 分支）git clone --depth 1 到一个临时文件夹，在其中运行（需 Python 3.9+；Windows 可用 py -3 代替 python3）：
   python3 -B scripts/install_skill.py install --host <上面的值> --home-root "$HOME"
3. 如果提示已安装，把 install 换成 update 再运行；如果提示需要 --backup-existing，加上它再运行（旧副本会移到备份文件夹，不会删除）。遇到其他错误就原样告诉我并停止：不要手动复制或删除文件、不要绕过检查、不要用 sudo。
4. 完成后删除临时文件夹，把脚本输出的安装路径、版本和 note 提示告诉我，并说明调用方式、是否需要新开会话。
```

**更新：** 再发送一次同样的话。脚本每次从新下载的仓库读取最新版本，不需要长期保留仓库副本。

## 自己在终端运行

```sh
git clone --depth 1 https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

| Agent | `--host` | 安装位置（相对于 `--home-root`） |
|---|---|---|
| Claude Code | `claude` | `.claude/skills/academic-writing-assistant` |
| Codex | `codex` | `.agents/skills/academic-writing-assistant` |
| Cursor | `cursor` | `.cursor/skills/academic-writing-assistant` |
| Grok Build | `grok-build` | `.grok/skills/academic-writing-assistant` |
| OpenCode | `opencode` | `.config/opencode/skills/academic-writing-assistant` |

更新与卸载使用相同的参数：

```sh
git pull --ff-only    # 或重新 clone 一份
python3 -B scripts/install_skill.py update --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py uninstall --host claude --home-root "$HOME"
```

Windows 可用 `py -3` 或 `python` 代替 `python3`。PowerShell 中 `"$HOME"` 可直接使用；cmd 中请写 `"%USERPROFILE%"`。加 `--json` 可得到结构化结果。

成功时脚本会输出安装路径和版本，更新时显示 `旧版本 -> 新版本`。

### 安装到项目目录

只想在某个项目中使用时，用 `--destination` 指定完整路径（末尾必须是 `academic-writing-assistant`）：

```sh
python3 -B scripts/install_skill.py install \
  --destination "/path/to/project/.claude/skills/academic-writing-assistant"
```

`update`、`uninstall` 使用同一个 `--destination`。各 Agent 的项目级目录见 [兼容说明](compatibility.md)。

## 已有旧副本：`--backup-existing`

如果目标位置已有一份不是由本脚本安装的副本（例如以前手动复制、用 `npx skills` 等其他工具安装），或者副本里的文件被修改过、多了 `__pycache__` 等文件，`install` 和 `update` 都会拒绝并说明原因，不会改动任何文件。

确认要换成新版本时运行：

```sh
python3 -B scripts/install_skill.py update --host claude --home-root "$HOME" --backup-existing
```

脚本会把整个旧文件夹**移到**备份位置（不删除、不合并），再安装一份由脚本管理的新副本。备份位于 Skills 目录之外，例如 `~/.claude/.academic-writing-assistant-backups/<时间>/academic-writing-assistant`，所以 Agent 不会把它当成第二份 Skill。确认不再需要后，你可以自行删除备份。安装失败时，旧副本会被放回原处。

## 输出中的 note：其他位置的同名副本

有些 Agent 会同时读取多个目录。例如 Cursor、OpenCode 也读取 `~/.claude/skills` 和 `~/.agents/skills`。安装或更新后，如果这些目录里还有本 Skill 的其他副本，脚本会列出来并说明哪些 Agent 可能显示两份：

```text
note: another copy exists at ~/.agents/skills/academic-writing-assistant (keep it current with update --host codex); Cursor, Grok Build, OpenCode may list the Skill twice.
```

脚本不会动这些副本。同时使用多个 Agent 时，可参考 [避免重复安装](compatibility.md#避免重复安装) 决定保留哪几份；保留多份时，用对应的 `--host` 分别更新。

## 安全保护

- 只复制 [包清单](../skills/academic-writing-assistant/package-manifest.json) 列出的文件，不包含测试、文档或缓存。
- 目标已存在时 `install` 拒绝操作；`update` 和 `uninstall` 会先逐一核对安装记录中的文件哈希，你修改或新增的文件会让操作停止。
- `--backup-existing` 只移动旧副本，从不删除。
- Skills 目录和安装包内部的符号链接、Windows 目录联接、硬链接和 `..` 路径都会被拒绝。仓库所在位置和 `--home-root` 本身会先解析为真实路径，因此从 macOS 的 `/tmp` 等系统链接位置运行也没有问题。
- 不需要 `sudo`，不修改 Agent 的设置。

## 常见问题

- **Agent 里看不到这个 Skill：** 确认 `SKILL.md` 位于上表中的安装位置，然后新开会话或重启 Agent。
- **提示 `Already installed ... by this tool`：** 已经安装过，把 `install` 换成 `update`。
- **提示需要 `--backup-existing`：** 见上文 [已有旧副本](#已有旧副本--backup-existing)。
- **提示 `Symlink or reparse-point path refused`：** Skills 目录本身是符号链接（例如把 `~/.agents/skills` 链接到别处）。脚本出于安全考虑不会写入，请改用真实目录，或用 `--destination` 指定链接指向的真实路径。
- **使用的 Agent 不在这五个之中：** 目前不提供官方支持。如果它支持 Agent Skills，可以用 `--destination` 安装到它的 Skills 目录。
- **没有 Python：** 安装脚本需要 Python 3.9+。安装后的写作功能本身不依赖 Python，只有可选的机械核查脚本需要它。

脚本退出码：`0` 成功；`1` 拒绝操作或文件系统错误（错误信息说明原因，已有文件不会被删除）；`2` 参数用法错误。

## English quick start

There is one installation method: the bundled `scripts/install_skill.py`, run either by your agent (paste the prompt from the [README](../README_EN.md#-install)) or by you:

```sh
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
```

`--host` is one of `claude`, `codex`, `cursor`, `grok-build` or `opencode`. Use `update` / `uninstall` with the same options. The installer copies only the files in the package manifest and verifies hashes before updating or removing. A copy it did not install (or one that was modified) is never overwritten; `update --backup-existing` moves it to a backup folder outside the skills directory and installs a managed copy. After install and update it reports the version and lists other copies that some agents may also load.
