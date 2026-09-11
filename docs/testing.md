# 测试与交付检查

本指南面向贡献者，介绍本地测试、独立包验证和公开交付检查。持续集成结果见 [GitHub Actions](https://github.com/LvvUP/academic-writing-assistant/actions/workflows/ci.yml)。

稿件脚本只需 Python 标准库。开发测试使用 [requirements-dev.txt](../requirements-dev.txt) 中固定版本的 pytest、PyYAML 及依赖；Python 3.9 使用条件依赖，Windows 使用 colorama。建议在自己的虚拟环境安装，避免更改全局环境。

Python 3.10+ 使用 pytest 9.1.1；Python 3.9 保留其最后支持的 8.4.2。仓库根目录的 `pytest.ini` 确保从根目录或 `tests/` 运行时都加载 `conftest.py`，为默认测试调用建立独占临时目录，并在结束时清理，避开旧版 pytest 的可预测共享目录问题（[CVE-2025-71176 上游修复](https://github.com/pytest-dev/pytest/pull/14343)）。这是本仓库测试的缓解措施，未修补第三方 pytest 包本身；其他项目中的旧版 pytest 不受此保护。显式使用 `--basetemp` 时请指定可安全清空的专用目录。Pygments 已更新到包含 [ADL 正则修复](https://github.com/pygments/pygments/pull/3064) 的 2.20.0。

```sh
python3 -m venv .internal/dev-venv
# 按当前系统激活虚拟环境，然后在仓库根目录运行：
python -m pip install --only-binary=:all: -r requirements-dev.txt
python -B -m pytest -q -p no:cacheprovider tests/
python -B skills/academic-writing-assistant/scripts/skill_lint.py .
python -B scripts/check_delivery.py .
python -B scripts/check_delivery.py . --index
git diff --check
```

`check_delivery.py` 默认使用 Git 的已跟踪和未忽略新文件清单，不读取被忽略的私人正文。被跟踪的忽略文件仍会按路径检查并阻止交付。`--index` 读取暂存区 blob，能发现工作树已修正但尚未重新暂存的内容。`--package` 检查明确指定的导出目录和清单，并拒绝包中多出的文件；资源是否完整由独立包 lint 进一步验证。

工作树和导出检查会在读取前拒绝符号链接、硬链接与 Windows 重解析点（包括目录联接 junction），防止通过公开路径读到私人文件的别名。文本必须可按 UTF-8/BOM 解码；NUL、UTF-16 或无法识别的二进制内容按覆盖不足阻止交付。PNG、JPEG、GIF、WebP 仅按扩展名与文件头识别并计入待人工检查的图片，不能据此认定图片或元数据安全。公开 HTTP(S) 链接中的 `/home/` 路径不会被当作机器目录；其中的凭据模式仍会检查。

守卫报告内部目录、私人稿件/原始日志命名、机器用户目录、部分高置信度凭据和 Agent 会话标记。未检查内容的压缩包也会阻止源码交付；先在明确的临时导出目录核查，不自动展开未知归档。它不判断所有正文是否适合公开，不解释图片，也不替代完整密钥扫描。输出默认只有规则和数量；本地排查可加 `--show-paths`，此输出不应上传或粘贴到公开 issue。不会输出原始命中内容。退出码为 0（当前范围未发现问题）、1（需处理）、2（输入/运行错误）。

导出包在临时目录验证，避免覆盖已安装 Skill：

```sh
python -B scripts/install_skill.py export --destination .internal/export/academic-writing-assistant
python -B scripts/check_delivery.py .internal/export/academic-writing-assistant --package
python -B .internal/export/academic-writing-assistant/scripts/skill_lint.py .internal/export/academic-writing-assistant --package
```

目标目录已存在时，安装器会拒绝覆盖；选择新的空目标，或仅在确认是自己生成的可重建导出后手动处理。

CI 配置 Ubuntu/Windows 的 Python 3.9 与 3.12，以及 macOS ARM 的 Python 3.12，使用只读仓库权限，不使用带仓库秘密的 PR 执行入口，也不上传扫描报告。macOS runner 架构以 [GitHub 官方列表](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) 为准；本机 Rosetta 下的 Python 3.9 测试不能代替 ARM 原生测试。所选 Python 版本的分发信息来自 [官方版本清单](https://github.com/actions/python-versions/blob/main/versions-manifest.json)。本机测试与远程矩阵结果是不同证据；远程作业尚未实际运行时不能宣称全部系统已通过。

Gitleaks 使用官方 [v8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1) 的 Linux x64 归档，下载后按官方 checksum 校验，再运行 Git 历史和实际导出包扫描。原始日志与报告只留在临时 runner，错误日志仅提示本地复现。新增忽略规则不会清除已有历史记录；历史问题需单独处理。

第三方 Actions 固定当前正式 release 的完整 commit SHA：已阅读 [checkout v7.0.1](https://github.com/actions/checkout/commit/3d3c42e5aac5ba805825da76410c181273ba90b1) 的 ref 识别、PR 检查和 Git 参数转义差异，以及 [setup-python v7.0.0](https://github.com/actions/setup-python/commit/5fda3b95a4ea91299a34e894583c3862153e4b97) 的 ESM 迁移、依赖及 manifest 取回验证变更。两者使用 Node 24，要求 Actions Runner 至少 2.327.1；本工作流使用 GitHub 托管 runner，不把该配置承诺扩展到旧自托管环境。这是变更审查，不是对第三方完整供应链的安全认证。Dependabot 定期提出 Actions/Python 更新；合并前核对官方差异、许可证及矩阵结果。Gitleaks 更新时同步核对官方 release、归档校验和与本地合成负例，保留固定版本，禁止绕过校验。
