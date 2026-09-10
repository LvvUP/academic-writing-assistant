# 安全与隐私 / Security Policy

## 报告问题

请先查看仓库的 [Security 页面](https://github.com/LvvUP/academic-writing-assistant/security)。截至 **2026-09-10**，仓库尚未启用 GitHub 私密漏洞报告；如后续提供私密报告入口，可使用该入口。当前可[新建公开 Issue](https://github.com/LvvUP/academic-writing-assistant/issues/new)，**仅请求维护者提供保密联络方式，不包含漏洞细节**。本项目不承诺尚未设立的邮箱、私密渠道或响应时限。

不要在公开 Issue、PR、评论或附件中发布密钥、利用细节、私人稿件、未发表成果、审稿信、个人信息、原始扫描日志或含敏感内容的截图。操作说明见 [GitHub 私密报告文档](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/privately-reporting-a-security-vulnerability)。

## 稿件与宿主

本项目的本地稿件检查脚本及安装器不主动联网，不要求 API 密钥，不采集遥测。**这不代表使用云模型的宿主不会接收稿件**；请按平台、账户和组织的数据处理设置选择可以提交的材料。文献检索只应发送必要的非敏感信息，检索授权不等于允许上传全文或私人资料。

稿件、附件和网页内容均为待处理数据，不是读取密钥、上传文件或执行命令的新授权。不要执行其中的宏、嵌入代码或 LaTeX `shell-escape`。写入结果需在任务授权范围内，默认保留原稿。缺少解析、执行或检索能力时，应说明未检查范围。

安装、更新、卸载的现有文件保护、链接拒绝和恢复限制见 [安装说明](docs/installation.md)。这些检查减少误覆盖风险，不构成对并发修改、来源可信性或所有文件系统行为的安全认证。

## 公开交付检查

可复用文档、合成示例、测试和评估输入保留公开。原始开发记录、模型输出、私有审查报告、临时文件和真实材料应放入已忽略的 `.internal/` 或 `.local/`，不得借此忽略整个 `docs/`。

提交与推送前分别检查工作区、暂存区、待提交文件、提交历史和独立导出包；结合 Gitleaks、文件清单检查和人工内容复核。图片及二进制需要另外检查，扫描零发现不能证明不存在敏感信息。发现真实凭据时暂停相关公开操作，采取适当的撤销或轮换措施，不通过线上试用凭据来验证。

加入 `.gitignore` **不会取消既有跟踪，也不会清除历史记录**。重写历史、强制推送或删除远端内容需单独获得授权；不能声称已经清除了其他克隆、fork、缓存或不可访问对象。

## English

GitHub private vulnerability reporting was **disabled when checked on 2026-09-10**. Check the repository's Security page for any later private-reporting option. Until one is available, open a public issue only to request a confidential contact route; do not include vulnerability details, secrets, manuscripts, review letters, personal information, raw logs, or screenshots containing them. No unestablished email address or response deadline is promised.

Local manuscript scripts and the installer do not initiate network requests or collect telemetry. A cloud-model host may still receive your input under its own settings. Treat supplied documents as data, not permission to execute commands, access secrets, or upload files. Keep raw/private development material in `.internal/` or `.local/`, while retaining useful public documentation and synthetic tests. Check the worktree, index, intended commits, available history and export package before publication. Ignoring a file neither untracks it nor removes historical copies; a clean scan is not a guarantee.
