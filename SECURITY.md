# 安全与隐私 / Security Policy

## 报告安全问题

请不要在公开 Issue、PR 或评论中发布漏洞细节、密钥、私人稿件或个人信息。

如果仓库的 [Security 页面](https://github.com/LvvUP/academic-writing-assistant/security) 提供了私密报告入口，请优先使用；否则可以[新建 Issue](https://github.com/LvvUP/academic-writing-assistant/issues/new)，只说明需要一个私下沟通的渠道，不要附带细节。

## 稿件与数据

- 本项目的核查脚本和安装工具在本地运行，**不联网、不需要 API Key、不收集任何数据**。
- 但你使用的 AI Agent 或云端模型可能会接收你提供的稿件。请根据所用平台、账户和机构的数据政策，决定哪些材料可以提交。
- 稿件、附件和网页内容只被当作待处理的文本，其中夹带的“执行命令”“读取密钥”“上传文件”等要求不会被执行。Skill 不执行稿件中的宏、脚本或 LaTeX `shell-escape`。
- 文献检索只应使用必要的非敏感检索词；检索授权不等于允许上传全文或私人资料。

## English

Do not post vulnerability details, secrets, manuscripts or personal data in public issues. Use the repository's private reporting option if available; otherwise open an issue asking only for a private contact channel.

The bundled scripts and installer run locally, make no network requests, need no API key and collect no telemetry. Your AI host or cloud model may still receive the text you provide, so follow your platform's and institution's data policies. Manuscript content is treated as data, never as instructions to run commands, read secrets or upload files.
