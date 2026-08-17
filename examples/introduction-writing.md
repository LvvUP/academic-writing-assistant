# 引言写作示例

## Task

Introduction Writing

## Field

Natural Language Processing

## User Input

```text
帮我写引言。方向是中文医疗文本的实体识别。现有方法在通用领域效果好，
但医疗领域标注数据少。我们用了一个基于提示的半监督方法。
```

## Expected Output

```markdown
## Introduction Draft

Named entity recognition underpins downstream clinical applications such as
[请补充你面向的下游任务，例如结构化病历或临床决策支持]. While recent models
perform strongly on general-domain Chinese text, clinical text differs in
vocabulary, abbreviation conventions, and document structure
[citation needed: 说明领域差异的工作].

The core obstacle is annotation. Clinical entity labeling requires domain
expertise and is constrained by privacy regulations, so labeled corpora remain
far smaller than their general-domain counterparts
[citation needed: 报告标注成本或数据规模的工作]. Approaches that assume
abundant supervision therefore transfer poorly to this setting.

This work addresses that gap with a prompt-based semi-supervised method that
[请补充方法的核心机制：提示如何构造、无标注数据如何利用].

The contributions are:
1. [请补充：你做了什么，而不是它有什么性质]
2. [请补充]
3. [请补充]

## 写作逻辑

- 重要性一句带过，不做教科书式综述
- gap 具体到"标注稀缺"这一可辩护的技术原因，而非泛泛的"效果不好"
- gap 必须与贡献对应——这是引言最常见的结构性失败

## 缺失信息

- 下游应用场景
- 提示构造方式与无标注数据的使用机制
- 参考文献（未提供，故使用 [citation needed] 而非编造引用）
- 贡献点需由你提供：每条应是"做了什么"，而不是"具有新颖性"
```

## 说明

用户没有提供参考文献，因此引言中出现的是 `[citation needed]` 占位符而不是
看起来合理的引用。这是相关工作与引言类任务的核心约束：虚构文献在格式上完全
正常，极易被带进投稿稿件。
