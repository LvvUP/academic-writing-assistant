# 安装、验证、升级与卸载

支持 **Claude Code、Codex、Cursor、Grok Build、OpenCode、WorkBuddy**。六个平台用的是同一份 Skill，都由仓库自带的 `scripts/install_skill.py` 准备文件：

- **Claude Code、Codex、Cursor、Grok Build、OpenCode**：脚本把 Skill 安装到该 Agent 的 Skills 目录。
- **WorkBuddy**：脚本导出一个技能包，你在 WorkBuddy 的「上传技能」里选中它。

你可以让 AI Agent 替你运行脚本，也可以自己在终端运行，结果完全一样。脚本需要 Python 3.9 或更新版本，只使用标准库，不联网。各平台的目录与依据见 [兼容说明](compatibility.md)。

## 让 Agent 替你安装（推荐）

### Claude Code、Codex、Cursor、Grok Build、OpenCode

把下面这段话发给你的 Agent：

```text
请帮我安装（已安装则更新）学术写作 Skill「academic-writing-assistant」，全程只用仓库自带的安装脚本：
1. 判断你是哪个 Agent，确定 --host：Claude Code → claude，Codex → codex，Cursor → cursor，Grok Build → grok-build，OpenCode → opencode。不是这五个就告诉我并停止。
2. 把 https://github.com/LvvUP/academic-writing-assistant（main 分支）git clone --depth 1 到一个临时文件夹，在其中运行（需 Python 3.9+；Windows 可用 py -3 代替 python3）：
   python3 -B scripts/install_skill.py install --host <上面的值> --home-root "$HOME"
3. 如果提示已安装，把 install 换成 update 再运行；如果提示需要 --backup-existing，加上它再运行（旧副本会移到备份文件夹，不会删除）。遇到其他错误就原样告诉我并停止：不要手动复制或删除文件、不要绕过检查、不要用 sudo。
4. 验证：把上面命令里的 install 换成 verify 再运行一次，应输出 verified 和版本号。
5. 删除临时文件夹，把安装路径、版本、备份位置（如有）和脚本输出的 note 提示告诉我，并说明调用方式、是否需要新开会话。
```

### WorkBuddy

WorkBuddy 的官方文档要求自备的技能包通过「上传技能」导入，所以分两步：先让 WorkBuddy 准备技能包，再由你上传。把下面这段话发给 WorkBuddy：

```text
请帮我准备学术写作 Skill「academic-writing-assistant」的技能包，我要通过「上传技能」把它装进 WorkBuddy：
1. 把 https://github.com/LvvUP/academic-writing-assistant（main 分支）git clone --depth 1 到当前工作空间里的一个临时文件夹。
2. 在该文件夹中运行（需 Python 3.9+；Windows 可用 py -3 代替 python3；把 <工作空间> 换成当前工作空间的绝对路径）：
   python3 -B scripts/install_skill.py export --destination "<工作空间>/awa-package/academic-writing-assistant" --archive
   它会生成技能文件夹 awa-package/academic-writing-assistant 和压缩包 awa-package/academic-writing-assistant.zip。如果提示已存在，说明以前导出过：先告诉我，由我决定是否删除旧的 awa-package 文件夹后重试。遇到其他错误就原样告诉我并停止，不要手动拼装文件。
3. 验证：确认压缩包第一层有 SKILL.md，并读出其中 metadata 下的 version。
4. 删除第 1 步的临时文件夹（保留 awa-package），把压缩包和技能文件夹的完整路径、版本号告诉我，并提醒我接下来到「专家·技能·连接器 → 技能 → 添加技能 → 上传技能」选中这个压缩包。
```

然后在 WorkBuddy 中上传：

1. 左侧边栏点击 **专家·技能·连接器**，选中 **技能** 页签。
2. 点击 **添加技能 → 上传技能**，拖入或选中 `academic-writing-assistant.zip`。官方文档只说“选中本地技能包”，没有说明格式；如果压缩包不被接受，可以改试同一目录下内容相同的 `academic-writing-assistant` 文件夹（这一做法未经官方文档确认）。
3. 列表里已有旧版本时，先在「已安装」中卸载旧版本，再上传新包。

不想运行命令时，也可以在 [Releases 页面](https://github.com/LvvUP/academic-writing-assistant/releases) 下载最新版本附带的 `academic-writing-assistant.zip`，直接上传。

> WorkBuddy 的官方文档没有写明上传包的格式，也没有写明本地技能目录。本项目的压缩包把 `SKILL.md` 放在第一层，同时提供同内容的文件夹；这一步依据官方文档描述的上传流程编写，尚未在 WorkBuddy 客户端中逐版本验证。各项说法的官方出处见 [兼容说明](compatibility.md#通过上传技能包安装的平台)。上传遇到问题请 [提交 Issue](https://github.com/LvvUP/academic-writing-assistant/issues)。

## 自己在终端运行

```sh
git clone --depth 1 https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py verify --host claude --home-root "$HOME"
```

| Agent | `--host` | 安装位置（相对于 `--home-root`） |
|---|---|---|
| Claude Code | `claude` | `.claude/skills/academic-writing-assistant` |
| Codex | `codex` | `.agents/skills/academic-writing-assistant` |
| Cursor | `cursor` | `.cursor/skills/academic-writing-assistant` |
| Grok Build | `grok-build` | `.grok/skills/academic-writing-assistant` |
| OpenCode | `opencode` | `.config/opencode/skills/academic-writing-assistant` |

为 WorkBuddy 导出技能包（`--destination` 的最后一级必须是 `academic-writing-assistant`）：

```sh
python3 -B scripts/install_skill.py export \
  --destination "$HOME/awa-package/academic-writing-assistant" --archive
```

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

`update`、`verify`、`uninstall` 使用同一个 `--destination`。各 Agent 的项目级目录见 [兼容说明](compatibility.md)。

## 验证安装成功

**第一步：检查文件。** `verify` 是只读操作，逐个核对已安装文件与安装记录是否一致：

```sh
python3 -B scripts/install_skill.py verify --host claude --home-root "$HOME"
```

输出 `verified: <路径> (version 0.5.0, …)` 表示副本完整且未被改动；否则以 `Not verified:` 开头说明原因，退出码为 1。

**第二步：确认 Agent 已加载。**

| Agent | 怎么确认 | 没有出现时 |
|---|---|---|
| Claude Code | 输入 `/`，列表中有 `academic-writing-assistant` | 当前会话通常直接识别；`~/.claude/skills/` 是新建的目录时运行 `/reload-skills` |
| Codex | 运行 `/skills`，或输入 `$` 后能选到它 | 重启 Codex |
| Cursor | 在 Agent 输入框输入 `/`，搜索 `academic-writing-assistant` | 重启 Cursor |
| Grok Build | 运行 `/skills` 查看，或输入 `/academic-writing-assistant` | 新开会话 |
| OpenCode | 在提示中写 `@academic-writing-assistant`，或直接提出写作任务 | 新开会话 |
| WorkBuddy | 「专家·技能·连接器 → 技能 → 已安装」中有 `academic-writing-assistant`；在对话框输入 `/` 可唤起技能列表 | 新开对话；在「已安装」中确认它没有被关闭（关闭的技能不参与新任务的调用） |

也可以直接试一句：“请润色这句话并说明重要改动：该方法可能在部分场景下改善性能。” 正常时，“可能”和“部分”会被保留。

## 升级

0.5.0 没有改动文件名、目录和安装路径，升级后原有用法不变。

| 你的情况 | 怎么升级 |
|---|---|
| 用安装提示词或安装脚本装的（0.3.0 及以后） | 再发送一次上面的安装提示词；或在新下载的仓库里运行 `update` |
| 手动复制的、用 `npx skills` 等其他工具装的，或改过里面的文件 | 同样发送安装提示词。脚本会说明原因并要求加 `--backup-existing`：旧副本整体移到备份文件夹（不删除），再安装新副本 |
| WorkBuddy | 重新导出技能包（或从 Releases 下载），在「已安装」中卸载旧版本后上传 |
| 同时为多个 Agent 安装了多份 | 对每个 `--host` 分别 `update`，保持版本一致 |

升级后可以用 `verify` 确认版本号。旧版 README 中的安装提示词仍然可用，只是不包含验证步骤。

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

- 只复制 [包清单](../skills/academic-writing-assistant/package-manifest.json) 列出的文件，不包含测试、文档或缓存；导出的压缩包同样只含这些文件。
- 目标已存在时 `install` 拒绝操作；`update` 和 `uninstall` 会先逐一核对安装记录中的文件哈希，你修改或新增的文件会让操作停止。
- `--backup-existing` 只移动旧副本，从不删除；`export` 不覆盖已存在的文件夹或压缩包；`verify` 不写入任何文件。
- Skills 目录和安装包内部的符号链接、Windows 目录联接、硬链接和 `..` 路径都会被拒绝。仓库所在位置和 `--home-root` 本身会先解析为真实路径，因此从 macOS 的 `/tmp` 等系统链接位置运行也没有问题。
- 不需要 `sudo`，不修改 Agent 的设置。

## 常见问题

- **Agent 里看不到这个 Skill：** 先运行 `verify`，再按 [验证安装成功](#验证安装成功) 中的表格处理。
- **提示 `Already installed ... by this tool`：** 已经安装过，把 `install` 换成 `update`。
- **提示需要 `--backup-existing`：** 见上文 [已有旧副本](#已有旧副本--backup-existing)。
- **提示 `Symlink or reparse-point path refused`：** Skills 目录或 `--destination` 路径中有符号链接（例如把 `~/.agents/skills` 链接到别处）。脚本出于安全考虑不会写入，请改用真实目录，或用 `--destination` 指定链接指向的真实路径。
- **提示 `Archive already exists`：** 导出位置已有同名压缩包。换一个目录，或确认不再需要后自行删除旧的导出结果。
- **使用的 Agent 不在这六个之中：** 目前不提供官方支持。如果它支持 Agent Skills，可以用 `--destination` 安装到它的 Skills 目录。
- **没有 Python：** 安装脚本需要 Python 3.9+。WorkBuddy 用户可以直接下载 Releases 中的压缩包。安装后的写作功能本身不依赖 Python，只有可选的机械核查脚本需要它。

脚本退出码：`0` 成功；`1` 拒绝操作、验证未通过或文件系统错误（错误信息说明原因，已有文件不会被删除）；`2` 参数用法错误。

## English quick start

All six supported hosts use the bundled `scripts/install_skill.py`, run either by your agent (paste the prompt from the [README](../README_EN.md#install)) or by you:

```sh
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"
python3 -B scripts/install_skill.py verify --host claude --home-root "$HOME"
```

`--host` is one of `claude`, `codex`, `cursor`, `grok-build` or `opencode`. Use `update` / `uninstall` with the same options. The installer copies only the files in the package manifest and verifies hashes before updating or removing. A copy it did not install (or one that was modified) is never overwritten; `update --backup-existing` moves it to a backup folder outside the skills directory and installs a managed copy. `verify` is read-only and confirms that every installed file matches the installation record.

For WorkBuddy, export a Skill package and upload it in the client under **专家·技能·连接器 → 技能 → 添加技能 → 上传技能** (Skills → Add skill → Upload skill; the English labels in your client may differ):

```sh
python3 -B scripts/install_skill.py export \
  --destination "$HOME/awa-package/academic-writing-assistant" --archive
```

The command writes the Skill folder and `academic-writing-assistant.zip` with `SKILL.md` at the top level. WorkBuddy's documentation does not specify the package format or a local skills directory, so this step follows the documented upload flow and has not been verified against every client version.
