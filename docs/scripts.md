# 机械核查脚本

核心写作不需要 Python。稿件检查脚本仅依赖 Python 标准库；开发用的 `skill_lint.py` 另需 PyYAML 来真正解析 YAML。安装与依赖见 [installation.md](installation.md)。下文 `<skill-root>` 是实际安装目录，稿件相对路径按调用者当前目录解释。

## 输入、输出与退出码

四个稿件检查入口均支持 UTF-8 / UTF-8 BOM 文本、`--json` 和 `--strict`。单稿件入口省略路径或用 `-` 时读取标准输入；保真比对可将其中一个路径设为 `-`，不能同时从一份标准输入读取前后两稿。空输入、不可解码输入、无效参数或 JSON 词表结构错误是输入错误，不能报“未发现问题”。脚本不修改输入文件。

CLI 在 Windows、macOS 和 Linux 上统一按 UTF-8 解码标准输入，并以 UTF-8 输出 JSON、Markdown 和标准错误，不依赖系统区域编码或 `PYTHONUTF8` 设置。管道调用方需发送 UTF-8 字节并按 UTF-8 解码输出；Python 的 `subprocess.run` 文本模式应显式传入 `encoding='utf-8'`。非法 UTF-8 输入退出 2，不以替换字符继续扫描。这个编码约定也适用于兼容入口和 `skill_lint.py` 的输出；作为 Python 库导入模块不会重配宿主标准流。

| 退出码 | 含义 |
|---|---|
| `0` | 扫描完成；默认模式发现待核查项仍为 0，应阅读报告 |
| `1` | 使用 `--strict` 后发现差异、待核查项、超限或覆盖不足 |
| `2` | 输入、配置或运行错误 |

机械提示不是论文质量评分或事实正确性证明。报告中的原文片段按 Markdown/HTML 转义展示。静态解析不执行稿件、宏、外部 TeX 输入、shell 命令或联网查询。

## 保真比对

```sh
python3 -B <skill-root>/scripts/fidelity_check.py --before original.tex --after revised.tex --json
python3 -B <skill-root>/scripts/fidelity_check.py --before original.tex --after revised.tex --strict
```

保留旧类别字段，新增 `_meta`（schema version 2）与来源位置、原始片段、重复项和上下文信息。检查范围包括带符号及指数的数值、常用单位、比较符、百分比/百分点、区间、引用键与命令、结构引用类型、公式和静态可定位的宏参数。不同科学含义不会仅因格式归一化被判等。

`numbers` 中的一项可以是完整数值关系，不等于一个独立标量：先读取各操作数的数值、幂和单位，再保留连接它们的运算符。例如 `5 ms ± 1 ms` 计为一项，两次出现仍计两项；`±`/`∓`、乘除和数值左右的比较方向不会被忽略。Unicode 负号与 ASCII 减号可归一，减法 `5 - 3` 不与文字范围 `5 to 3` 判等。数字/单位间空白、`\pm` 与 `±` 等明确等价写法允许归一，不进行单位换算或推导数值等价。

这里的正文数值关系归一限同一行的横向空白。若数字与已知单位、数字与运算符，或比较符与数值边界被换行分开，扫描器保留已识别的项并明确标记 `linewrapped_numeric_relationship` 覆盖不足，要求人工确认；不会把跨行关系当作已完整核查。仅将一行折为两行也可能同时出现项拆分提示与覆盖不足，`--strict` 返回 1。这样避免误将段落、列表或软换行自动拼接。数学块仍使用单独的数学空白处理规则。

带 `CI`、`confidence interval`、`interval`、`range`、置信区间/区间/范围上下文的两个字面端点保留开闭括号；`95% CI [1,2]` 为百分比和区间两项，`[1,2]` 与 `(1,2)` 不判等。没有这类上下文的普通 `[1,2]` 仍按编号引文处理。该区间扫描限同一行、起始括号后最多512字符及一个逗号分隔的两个字面端点；符号端点、嵌套或多个逗号造成的歧义标为覆盖不足。它不判定无标记括号究竟是坐标、区间还是引文，仍需人工结合语境判断。组合关系与区间的识别会改变 `numbers` 的项数及归一值；旧九类字段、原文位置、重复项和 `_meta` 接口保留，调用者不应将项数解释成原文数字个数。

`UNCHANGED_WITHIN_COVERAGE` 表示已识别范围内未发现差异；`REVIEW_NEEDED` 表示有变化需核对；`INSUFFICIENT` 表示零覆盖、未支持构造或其他覆盖问题。无保护项的单一类别显示 `NOT_CHECKED_NO_ITEMS`，不代表整个文档通过。严格模式同时拦截差异与覆盖不足。

报告保留重复次数，并提示部分数值重分配、引用移动和顺序变化。它不能可靠证明改写后的指标归属、引文支持关系或全文语义一致；句子大幅改写、相同句式重排及动态 TeX 仍需结合原稿进行语义复核。用户授权的格式转换或数值更正也可能产生提示，应解释原因。

## 稿件审计与长度

```sh
python3 -B <skill-root>/scripts/manuscript_audit.py draft.tex --checks abbreviations,claims --json
python3 -B <skill-root>/scripts/manuscript_audit.py abstract.txt --section abstract --limit-words 250 --strict
python3 -B <skill-root>/scripts/manuscript_audit.py highlights.txt --limit-chars 85 --per-line --strict
```

正文环境和文本格式命令的内容保留；数学、代码与注释按静态策略遮蔽，原文位置保持对应。未知或不完整构造报告覆盖限制。

- 缩写：启发式检查首次使用/定义及单次使用，不等于数学符号定义检查。
- 主张：在当前句子/分句中查找统计依据线索；其他段落的 p 值、标准差或置信区间不能替该主张作证。“当前材料未见依据”不表示作者未做检验。
- 文风与术语：提示可疑冗余和配置的英文用法差异，修改仍需判断原义。
- 时态：自动时态审计目前 **NOT RUN**；正常方法现在时与实验过去时混用不报错。显式请求 `--checks tense` 会报告未实现覆盖，严格模式退出 1。

词数按报告列出的英文词与 CJK 字符口径估算；字符上限含空格，逐行模式分别核对各行。它们不是所有投稿系统的统一计数算法。85 字符仅在目标要求适用时使用，政策范围见 [policy-sources.md](../skills/academic-writing-assistant/references/policy-sources.md)。

## 术语关系

```sh
python3 -B <skill-root>/scripts/terminology_checker.py draft.md --json
python3 -B <skill-root>/scripts/terminology_checker.py draft.md --map custom-terms.json --strict
```

内置词表区分等价写法、文风偏好和相关但不同概念。长词优先匹配，保留原文位置；相关概念只提示核对，不建议直接合并。作者确认的定义和用法优先于通用词表，词频不能代替作者的概念定义。`--map` 以自定义词表替换默认词表；格式和字段见 [terminology-map.zh-en.json](../skills/academic-writing-assistant/assets/terminology-map.zh-en.json)。不支持或不完整的输入会报告错误或覆盖不足。

## 章节与研究类型

```sh
python3 -B <skill-root>/scripts/structure_checker.py --section abstract draft.md --json
python3 -B <skill-root>/scripts/structure_checker.py --section method --research-type qualitative draft.md
```

章节支持 `abstract`、`introduction`、`related_work`、`method`、`experiment`、`discussion`、`conclusion`。研究类型为 `empirical`（默认）、`theoretical`、`review`、`qualitative`。关键词仅提示可能遗漏的要素，不能判断论证是否充分；理论、综述与定性研究不强制提供网络、训练或消融。

检查还识别待填写槽位。编号引文 `[12]` 等不是占位；占位检查不能保证全部缺失信息被找出。

## 仓库与独立安装包

```sh
# 在仓库根目录；依赖开发环境中的 PyYAML
python3 -B skills/academic-writing-assistant/scripts/skill_lint.py .
# 只检查独立 Skill，不依赖仓库 README、tests 或插件包装
python3 -B <skill-root>/scripts/skill_lint.py --package <skill-root>
```

仓库 lint 验证 YAML 类型/长度/目录名称、配置的必要文件、Logo 引用、插件结构和部分公开文案边界。普通 lint 只读公开/计划交付清单，忽略本地内部目录；它不能替代单独的安全与历史审查，也不能证明引用真实。

兼容入口 `section_audit.py` 与 `term_consistency_check.py` 继续转发到章节和术语检查器。完整参数以实际 `--help` 为准。
