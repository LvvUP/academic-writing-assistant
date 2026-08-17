<div align="center">

<img src="assets/logo/revision-compass.svg" alt="Revision Compass" width="120">

# Academic Writing Assistant

面向中英文学术论文的领域自适应写作 Skill。

**中文** | [English](README_EN.md)

</div>

## 项目定位

`academic-writing-assistant` 是一个面向科研作者的学术写作 Skill / Plugin，用于论文润色、中英互译、章节写作、审稿回复与 rebuttal、投稿材料准备、以及全文一致性检查。

它解决的核心问题不是"让文字更流畅"——那件事模型本来就会做，而且正因为做得太好而危险：流畅的改写会悄悄抬高论断。"在部分数据集上有所改善"变成 "significantly outperforms existing methods"，作者读到比自己原文漂亮的英文，就直接用了。等审稿人发现，代价已经产生。

所以这个 Skill 的重点是**改得动、也查得清**：哪些内容一个字都不能动，哪些词改了就等于改了科学主张，以及作者如何在一分钟内核对完所有改动。

适合研究生、博士生、青年教师、科研作者，以及希望把学术写作流程沉淀为可复用 Skill 的 AI Agent 用户。

## 核心机制：保真契约

改写前把每句话拆成三个区域，这是整个 Skill 最有用的习惯。

| 区域 | 内容 | 处理方式 |
|---|---|---|
| **锁定区** | 数值、单位、p 值、数据集名、方法名、引用标记、公式、符号、交叉引用、伦理批号 | 原样保留。发现疑似错误也**只标记不修改**——你看不到数据，作者能看到 |
| **承重语言** | 情态词（may/表明/证明）、量化词（all/部分）、范围限定（"在所评估的数据集上"）、因果动词（导致 vs 相关）、新颖性主张（first/SOTA/significantly） | 只能向更准确的方向改，且必须披露 |
| **自由表层** | 语法、冠词、时态、句子拆分、连接词、冗余、语序、同强度同义替换 | 放手改。这里才是价值所在 |

每处改动按三级标注：

- **L1 表层**：语法、冠词、时态、拼写 → 汇总成一行"共 N 处"，不逐条列
- **L2 结构**：拆分合并、语序调整、术语统一 → 每条一句话说明
- **L3 主张**：触及承重语言 → **绝不静默应用**，必须给出理由或留作待确认

这样分级的原因很实际：作者收到 40 条不分轻重的修改，会全部接受而不逐条看，因为核对成本太高；收到"L1 共 12 处 + L2 三处 + L3 一处需你确认"，才会真的去读那关键的四条。让重要的改动变得容易被发现，这是 Skill 的核心职责。

## 核心功能

| 功能 | 说明 |
|---|---|
| 保真改写 | 三区域 + 三级改动分级，输出可逐句核对的改动台账 |
| 任务路由 | 识别润色、翻译、扩写、合并、压缩、章节写作、审稿回复等任务 |
| 领域适配 | 按领域调整写作重点——重点是**该领域审稿人会攻击什么** |
| 中英学术翻译 | 中译英 / 英译中，附术语表与译法说明 |
| 章节写作 | 摘要、引言、相关工作、方法、实验、讨论、结论 |
| 审稿回复 | 区分期刊 response letter 与会议 rebuttal（两者篇幅、时态、结构均不同） |
| 投稿材料 | Cover letter、Highlights（85 字符限制）、AI 使用声明、CRediT 贡献声明 |
| LaTeX 感知编辑 | 直接改 `.tex` 源码，保住 `\cite{}`、`\ref{}`、公式与自定义宏 |
| 全文一致性 | 术语、缩写首次定义、符号、时态、数值、主张强度跨章节核查 |
| 确定性核对脚本 | 机械核对引用/数值/公式是否在改写中丢失，不靠"读一遍" |
| 学术诚信护栏 | 禁止虚构文献、数据集、实验结果与不受支持的结论 |

## 与上一版的差异

| | v0.1 | v0.2 |
|---|---|---|
| 改动呈现 | 返回新文本 + 几条含糊说明 | L1/L2/L3 分级 + 可逐句核对的改动台账 |
| 主张保护 | "不要夸大"（原则性表述） | 承重语言清单 + 强度阶梯 + 改动必须披露 |
| 审稿回复 | 单一模板 | 期刊 letter 与会议 rebuttal 分开处理 |
| 投稿材料 | 无 | Cover letter、Highlights、AI 声明、CRediT |
| LaTeX | 无 | 专门的源码编辑规则与保全核对 |
| 全文检查 | 无 | 术语/缩写/符号/时态/主张强度一致性 |
| 脚本 | 关键词 bingo | 引用与数值保全核对、缩写首用、投稿字数限制 |
| 领域适配 | 术语与写作重点 | **该领域审稿人的典型攻击点** |

## 支持的学术写作任务

学术润色 · 段落扩写 · 段落合并 · 压缩到字数限制 · 中译英 · 英译中 · 摘要 · 引言 · 相关工作 · 方法 · 实验 · 讨论与局限 · 结论 · 期刊审稿回复 · 会议 rebuttal · Cover letter · Highlights · AI 使用声明 · 标题优化 · 贡献点改写 · 术语一致性 · 全文一致性检查 · 学术自然化 · 提示词优化

## 支持的研究领域

内置领域适配预设覆盖：计算机视觉、机器学习与人工智能、自然语言处理与大模型、医学影像与临床研究、遥感、机器人、数据挖掘与推荐、生物信息学、材料科学与化学、社会科学与教育管理。

每个预设记录的不是词汇表，而是**该领域审稿人实际会攻击什么**——遥感审稿人问地理泛化，临床审稿人问外部验证，NLP 审稿人问数据污染。写作时预先回应这些质疑，是可辩护的论文与大修之间的差别。

上面的列表**不是支持范围上限**。未列出的领域同样使用通用学术写作流程：先识别任务、保留技术含义、控制证据边界、统一术语，再根据你提供的研究背景适配。提问时补充研究领域、目标期刊风格与核心术语即可；信息不足时 Skill 会使用占位符或提示你补充，而不是编造领域事实。

## 目录结构

```text
academic-writing-assistant/
├── .codex-plugin/plugin.json
├── assets/logo/
├── skills/academic-writing-assistant/
│   ├── SKILL.md                    # 保真契约、路由、输出规范、诚信边界
│   ├── references/                 # 按需加载的详细规则
│   │   ├── fidelity-protocol.md    # 三区域与三级改动的实例讲解
│   │   ├── writing-workflows.md    # 各任务的具体做法
│   │   ├── reviewer-response.md    # 期刊 letter vs 会议 rebuttal
│   │   ├── submission-package.md   # cover letter / highlights / AI 声明
│   │   ├── latex-and-formats.md    # LaTeX、Word、Markdown 处理
│   │   ├── consistency-pass.md     # 全文一致性检查
│   │   ├── field-adapter.md        # 各领域审稿人攻击点
│   │   ├── style-guide-zh.md       # 中文学术语体
│   │   ├── style-guide-en.md       # 英文语体与中式英语干扰模式
│   │   ├── task-router.md          # 任务识别与需要重定向的请求
│   │   ├── output-templates.md     # 各任务输出形态
│   │   ├── quality-checklist.md    # 回复前的自检
│   │   ├── citation-safety.md      # 引用与证据边界
│   │   ├── terminology.md          # 中英术语选择与一致性
│   │   └── examples.md             # 端到端完整示例
│   ├── assets/terminology-map.zh-en.json
│   └── scripts/                    # 确定性核对脚本
├── examples/  ├── tests/  ├── docs/  ├── evals/
├── README.md  ├── README_EN.md  └── LICENSE
```

`SKILL.md` 保留核心机制与路由；详细规则放在 `references/`，Agent 按需读取。

## 安装

### Codex 安装

把这句话发给 Codex：

```text
请从 https://github.com/LvvUP/academic-writing-assistant 安装 Academic Writing Assistant Skill 到我的本地 Codex skills 目录，并验证 $academic-writing-assistant 可以被调用。
```

安装完成后，新开一个 Codex 会话即可使用：

```text
Use $academic-writing-assistant to polish this academic paragraph.
```

<details>
<summary>手动安装备用</summary>

```bash
git clone https://github.com/LvvUP/academic-writing-assistant.git
mkdir -p ~/.codex/skills
cp -R academic-writing-assistant/skills/academic-writing-assistant ~/.codex/skills/
```

如果你的 Codex 环境支持本地插件，也可以使用仓库中的 `.codex-plugin/plugin.json` 作为插件 manifest。

</details>

### Claude Code 安装

同样可以让 Claude Code 自动安装：

```text
请从 https://github.com/LvvUP/academic-writing-assistant 安装 Academic Writing Assistant Skill 到我的本地 Claude Code skills 目录，并验证 $academic-writing-assistant 可以被调用。
```

<details>
<summary>手动安装备用</summary>

```bash
git clone https://github.com/LvvUP/academic-writing-assistant.git
mkdir -p ~/.claude/skills
cp -R academic-writing-assistant/skills/academic-writing-assistant ~/.claude/skills/
```

</details>

安装完成后，新开一个 Claude Code 会话即可使用：

```text
Use $academic-writing-assistant to translate this Chinese academic paragraph into English.
```

### 其他 Agent 安装

如果你的 Agent 支持 Skill 目录机制，复制整个目录：

```text
skills/academic-writing-assistant/
```

如果你的 Agent 可以读取 GitHub 仓库，直接把链接交给它：

```text
https://github.com/LvvUP/academic-writing-assistant
```

如果你的 Agent 不支持 Skill 机制，可以将 `SKILL.md` 作为主指令，在需要时加载 `references/` 中的对应文件。

不要只复制 `scripts/`。脚本只做机械核对，真正的保真规则、任务路由和诚信边界都在 `SKILL.md` 与 `references/` 中。

## 使用示例

### 学术润色：看到改动台账长什么样

输入：

```text
我做医学影像分割的，帮我润色成 SCI 风格：我们的方法能减少标注困难的问题，
分割结果比较好，对小病灶也有帮助，明显优于现有方法。
```

输出示例：

#### 修改后文本

```text
The proposed method reduces the annotation burden in medical image segmentation
and improves the delineation of small lesions compared with the evaluated
baselines. [请补充具体数据集、指标与数值]
```

#### 改动台账

L1（语法/冠词/时态）：共 4 处，未逐条列出。

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | 分割结果比较好 | improves the delineation ... compared with the evaluated baselines | L3 | "比较好"无对照对象；英文论文需指明与谁比较 |
| 2 | 明显优于现有方法 | compared with the evaluated baselines | L3 | "明显/significantly" 在英文中读作统计显著性主张。若已做显著性检验，告知检验方法与 p 值可改回 |

#### 需确认

- 使用了哪些数据集、哪些评价指标（Dice / IoU / HD95）？
- "现有方法"具体指哪些 baseline？写明方法名称能显著降低审稿人质疑对比公平性的概率。
- 标注负担的降低是否有量化（标注时长 / 标注像素量 / 所需样本数）？

注意输出里**没有编造任何 Dice 数值**来把句子补完整——缺的信息以占位符呈现，而两条 L3 都说明了如何撤回。

### 中译英：会告诉你哪句话不该直译

输入：

```text
翻译成 SCI 英文：针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种
多尺度特征融合方法，具有重要的理论意义和应用价值。
```

输出示例：

#### English Translation

```text
To address the large scale variation and complex backgrounds in remote sensing
images, this study proposes a multi-scale feature fusion method.
```

#### 术语选择

| 中文 | English | 说明 |
|---|---|---|
| 遥感图像 | remote sensing images | 遥感领域标准表述 |
| 目标尺度变化 | scale variation | 比 target scale change 更符合领域惯例 |
| 多尺度特征融合 | multi-scale feature fusion | 通用表述；不用 feature merging |

#### 翻译说明

- 删除了"具有重要的理论意义和应用价值"（L3）。这类表述在中文论文中是惯例性收尾，直译成 "has important theoretical significance and application value" 在英文中会被读作缺乏支撑的宏大主张。如需保留这层意思，建议改为具体陈述。

### 会议 rebuttal：与期刊回复信区别对待

输入：

```text
ICLR 审稿人说 "The improvement over baselines is marginal and may be within noise."
我们跑了 5 个种子，均值提升 2.1 个点，标准差 0.3。
```

输出示例：

```text
**Marginal improvement / noise (R2).** We report results over 5 seeds: the
proposed method improves by 2.1 points on average (std 0.3), while the baseline's
own seed variance is [请填写 baseline 的标准差]. The gap therefore exceeds the
run-to-run variation by a substantial margin. We will add per-seed results and
variance to Table 2 in the revision.
```

并提示：建议补充 baseline 的种子方差——这是回应"是否在噪声范围内"最直接的证据；只给自己方法的方差无法完全回答审稿人的问题。

## 脚本

脚本只用 Python 标准库，不依赖第三方包。它们负责的是模型做不可靠、而机器做得准的部分。

```bash
# 改写后核对：引用、数值、公式、交叉引用、自定义宏有没有丢
python skills/academic-writing-assistant/scripts/fidelity_check.py \
    --before original.tex --after revised.tex

# 全文体检：缩写先用后定义、术语漂移、无检验的 significant、时态混用、字数限制
python skills/academic-writing-assistant/scripts/manuscript_audit.py draft.md \
    --section abstract --limit-words 250

# Highlights 逐条字符数（Elsevier 85 字符含空格）
python skills/academic-writing-assistant/scripts/manuscript_audit.py highlights.txt \
    --limit-chars 85 --per-line

# 中文术语变体混用
python skills/academic-writing-assistant/scripts/terminology_checker.py draft.md

# 章节结构要素是否齐全
python skills/academic-writing-assistant/scripts/structure_checker.py \
    --section experiment draft.md
```

`fidelity_check.py` 是默认应该跑的那个。它给出的是证据而不是感觉：明确告诉作者哪些受保护内容发生了变化。一个丢失的 `\cite{}` 能正常编译、读起来也毫无异样，但它意味着一处未标注引用——这正是"再读一遍"抓不到、而脚本能抓到的东西。

详见 [docs/scripts.md](docs/scripts.md)。

## 设计原则

1. **保真优先于流畅**：改善表达，但不移动证据边界。
2. **改动可审计**：分级呈现，让重要的改动容易被发现——作者核对不动的台账等于没有台账。
3. **确定性的事交给脚本**：引用与数值的保全靠核对，不靠信任。
4. **领域适配是审稿视角**：知道该领域会被问什么，比知道该领域的词汇更有用。
5. **渐进披露**：`SKILL.md` 保持精简，复杂规则放入 `references/`。
6. **繁简相称**：一句话的修改不需要一张表格。

## 学术诚信

这是学术表达辅助工具，不是论文代写或结果生成工具。

它必须避免：

- 虚构参考文献、作者、年份、期刊、会议、论文题目、DOI 或 arXiv 编号；
- 虚构数据集、样本量、指标数值、消融结论、统计检验或 p 值；
- 虚构伦理批号、注册号、基金号；
- 声称做过某项实验或已完成某处修改（除非作者明确说明）；
- 夸大贡献、创新性、临床价值或部署能力；
- 改变用户提供内容的技术含义；
- 帮助规避学术诚信检查。

证据不足时使用**醒目的占位符**——`[请补充主要定量结果]`——而不是看起来合理的编造内容。占位符是服务，貌似合理的虚构是地雷。

关于"降低 AI 率"这类请求：Skill 不按检测器分数改写（这类工具在两个方向上都不可靠），但会处理背后的真实问题——被判为机器生成的文本通常确实存在句长均匀、论点等权、表述空泛、模糊语堆叠等问题，修掉这些本身就是更好的学术写作。

关于 AI 使用声明：多数出版商现已要求声明实质性的生成式 AI 使用。Elsevier 要求在参考文献前设置专门章节，ICLR 将未声明的实质性 LLM 使用视为违反行为准则。语言润色通常豁免，但门槛各家不同。`references/submission-package.md` 提供了声明模板与当前政策概况，具体请以目标期刊的作者指南为准。

## 路线图

- `v0.1`：核心 Skill、任务路由、领域适配、诚信规则、示例与辅助脚本。
- `v0.2`（当前）：保真契约与改动分级、期刊/会议审稿回复分离、投稿材料、LaTeX 感知编辑、全文一致性检查、确定性核对脚本。
- `v0.3`：更多学科的审稿攻击点、图表与公式表述规范、学位论文章节支持。
- `v0.4`：术语库扩展与社区贡献的领域包。
- `v1.0`：稳定结构、完整示例库、评估集与贡献流程。

详见 [ROADMAP.md](ROADMAP.md)。

## 贡献指南

欢迎贡献：

- 新领域的审稿攻击点与写作重点；
- 术语表与术语混用规则；
- 更安全的输出模板；
- 不含敏感信息的学术写作示例；
- 脚本与测试。

提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。包含虚构文献、鼓励不受支持结论或削弱学术诚信护栏的贡献不会被接受。

## 许可证

本项目使用 MIT License。详见 [LICENSE](LICENSE)。

如果这个项目帮助你写出更清晰、更负责的学术论文，欢迎给它一个 Star，让更多科研作者发现它。
