# 安装、更新与卸载

核心写作只需要宿主能加载 `SKILL.md`；安装工具和机械核查需要 Python 3.9 或更新版本。安装工具只使用标准库，不联网、不修改宿主配置，不自动启用云同步。宿主目录与原生调用的依据、实测范围见 [兼容矩阵](compatibility.md)。

新建环境建议使用仍受维护的 **Python 3.12**。3.9 是最低 API 要求和兼容性回归目标，已于 2025-10-31 结束上游维护（[Python 官方版本状态](https://devguide.python.org/versions/)）；不需要为本项目替换系统 Python。

当前 0.3.0 版本采用 **AGPL-3.0-only**，完整包包含许可证和必要声明，见 [许可说明](licensing.md)。安装到已有目标时会拒绝操作，不自动覆盖旧副本。

0.3.0 已合并到默认分支 `main`。以下命令从默认分支取得当前版本；已有副本可先保留本地改动，再切换到 `main` 并更新。

## 个人安装

取得仓库并进入它的根目录；已有副本可以直接使用：

```sh
git clone https://github.com/LvvUP/academic-writing-assistant.git
cd academic-writing-assistant
```

按宿主选择一条。`--home-root "$HOME"` 明确指定自己的主目录，只读取这个变量，不修改 `HOME` 或 `CODEX_HOME`。

```sh
# Codex：推荐的个人 Skill 目录
python3 -B scripts/install_skill.py install --host codex --home-root "$HOME"

# Claude Code
python3 -B scripts/install_skill.py install --host claude --home-root "$HOME"

# Cursor
python3 -B scripts/install_skill.py install --host cursor --home-root "$HOME"

# Grok Build：限官方编码 Agent，不适用于普通 Grok 网页或模型 API
python3 -B scripts/install_skill.py install --host grok-build --home-root "$HOME"
```

工具会在对应宿主目录下新建 `academic-writing-assistant`。**同名目标已经存在时直接拒绝，空目录也不会被覆盖。** 它不会把手动安装的目录自动接管为可更新目录。

| `--host` | `--home-root` 下的安装位置 |
|---|---|
| `codex` | `.agents/skills/academic-writing-assistant` |
| `claude` | `.claude/skills/academic-writing-assistant` |
| `cursor` | `.cursor/skills/academic-writing-assistant` |
| `grok-build` | `.grok/skills/academic-writing-assistant` |

## 项目安装与任意工作目录

项目安装使用完整目标路径；路径末尾必须是 Skill 标识。下面的 `/path/to/project` 需替换为自己的项目目录：

```sh
python3 -B scripts/install_skill.py install \
  --destination "/path/to/project/.agents/skills/academic-writing-assistant"
```

Claude Code 将 `.agents` 换成 `.claude`；Cursor 可使用 `.cursor`；Grok Build 使用 `.grok`。个人与项目目录无需同时安装；重复安装可能让宿主选择到另一份规则。

安装源始终按安装脚本的实际位置找到仓库内 Skill；目标相对路径则按当前工作目录解释。离开仓库运行时，给脚本本身的完整路径：

```sh
python3 -B "/path/to/academic-writing-assistant/scripts/install_skill.py" install \
  --destination "./.agents/skills/academic-writing-assistant"
```

不需要 `sudo`。目标、源文件和它们的祖先目录若为符号链接或 Windows 重解析点（包括目录联接 junction），工具会拒绝；硬链接、设备文件和 `..` 路径也不接受。请明确选择真实目录，不通过关闭检查来绕过保护。Windows 可用已安装的 Python 启动器替换 `python3`；原生 Windows 测试状态见兼容矩阵。

## 调用

重新打开或刷新宿主的 Skill 列表后，使用它的原生方式：

```text
Codex:       $academic-writing-assistant 请润色这段中文，保留数值和证据范围：……
Claude Code: /academic-writing-assistant 请将这段中文译成英文：……
Cursor:      在 Agent 输入框输入 /，选择 academic-writing-assistant，再输入任务。
Grok Build:  /academic-writing-assistant 请检查这段审稿回复的事实与行动状态：……
```

`$academic-writing-assistant` 不是 Claude Code 的原生斜杠命令。没有原生 Skills 的宿主可以手动加载主指令和本次所需参考文件；它实际不能读取或运行的部分必须标为未检查。

## 更新

先在仓库副本中确认并取得准备安装的版本。更新工具从本地副本读取，不执行 `git pull`。若确实要跟随当前分支的远程更新，可先运行：

```sh
git status --short
git pull --ff-only
python3 -B scripts/install_skill.py update --host codex --home-root "$HOME"
```

其他宿主替换 `--host`；项目安装复用最初的 `--destination`。更新前核对目录中的安装记录与每个文件的 SHA-256、大小和实际清单。修改过、缺失、额外新增的文件或目录都会导致拒绝；没有强制覆盖开关。

新包先写入同一父目录的临时目录，完整后才替换。正常替换失败时恢复原安装；若目标被其他进程占用、旧目录在操作过程中发生变化，工具保留备份并输出实际位置。执行期间请暂停编辑或运行该安装目录。它不会把并发修改或中断恢复包装成成功。

## 卸载

```sh
python3 -B scripts/install_skill.py uninstall --host codex --home-root "$HOME"
```

卸载同样要求安装记录、文件哈希和清单完全匹配。只移除该工具安装且保持未改动的文件，不清理相邻 Skills、用户笔记或宿主设置。没有本工具安装记录的手动副本，请先自行核对与备份后手动处理。

## 导出和手动放置

导出一个新目录，用于检查、手动复制或后续打包。目标必须不存在；这里使用仓库已忽略的本地输出目录：

```sh
python3 -B scripts/install_skill.py export \
  --destination ".local/export/academic-writing-assistant" --json
```

导出严格按 [package-manifest.json](../skills/academic-writing-assistant/package-manifest.json) 的明确清单读取文件。包含 `SKILL.md`、必需的 `references/scripts/assets`、可选宿主元数据、此版本的 `LICENSE` 与 `THIRD_PARTY_NOTICES.md`，以及清单本身。不按后缀自动收集新文件，不包含缓存、仓库文档、内部记录、开发环境或安装记录。

手动安装时将这个完整目录放到上表对应位置，先确认那里没有同名目录，避免合并复制。只复制 `SKILL.md` 或 `scripts/` 会遗漏规则、资源或许可证。导出副本不含管理用安装记录，因此不能用 `update` / `uninstall` 自动接管。

清单不是签名。安装记录中的哈希用于检测本地安装后的变更，不证明仓库来源可信或内容已通过学术审查。公开发布前仍需独立审查实际交付清单和内容。

## 核查与排障

日常运行脚本建议加 `-B`，避免 Python 在安装目录产生字节码缓存：

```sh
python3 -B "/path/to/skill/scripts/manuscript_audit.py" draft.txt --checks claims --json
```

- **已有同名目录**：保留当前副本；确认它是否由本工具安装。不要删除未知目录或改安装记录来强行通过。
- **报告额外文件 / `__pycache__`**：普通 Python 运行可能产生缓存。工具不会自动删除或信任 `.pyc`。先确认这些文件的来源，备份或移出 Skill 目录，再重试。自定义术语表、稿件和笔记也应放在 Skill 外，通过文件路径传入。
- **文件或安装记录已修改**：先保留自己的改动，与准备安装的版本比较；可另选目录导出。只有回到原安装记录描述的完整内容，自动更新/卸载才会继续。
- **磁盘不足 / 写入失败**：先释放空间。暂存写入失败会清理本操作新建的暂存目录，保留原安装。若错误指出 `.awa-previous-*` 中的保留文件，按输出位置核对并恢复，勿将整个匹配目录批量删除。
- **宿主没有发现 Skill**：核对当前宿主、项目/个人作用域、目录末尾名称及 `SKILL.md`，再刷新列表。官方目录说明不等于当前版本已经实际加载；旧版 Codex 兼容路径见兼容矩阵。
- **`python3` 不存在或版本过旧**：先使用系统已有的受支持 Python。核心文本写作可继续，机械检查标为未运行。
- **包 lint 提示缺少 PyYAML**：这是开发校验的依赖，不是日常写作或四个稿件检查脚本的运行依赖。开发核查方式见 [脚本说明](scripts.md) 与 [贡献指南](../CONTRIBUTING.md)。

安装工具退出码：`0` 为所请求操作成功；`1` 为拒绝操作或文件系统失败，具体是否保留/恢复见错误信息；`2` 为命令行参数用法错误。`--json` 成功结果在标准输出，错误结果在标准错误；不会打印稿件或配置文件内容。

## English quick start

Use the same commands above with an explicit `--host` and `--home-root`, or an exact `--destination`. Installation refuses any existing destination. Update and uninstall require the tool's receipt and unchanged files, with no extra files or directories. Preserve your edits and move confirmed generated caches outside the Skill before retrying; `python3 -B` prevents new bytecode caches. Export copies only the explicit package manifest, including licenses, and does not create an installation receipt. See the [compatibility matrix](compatibility.md) for official documentation versus actual testing.
