# 引言写作示例

## Task

Introduction Writing

## Field

Natural Language Processing

## User Input

```text
请根据以下信息帮我组织 introduction 的写作思路：

方向：面向专业领域问答的检索增强生成
问题：模型容易生成没有依据的回答；专业术语和上下文依赖强
方法：加入术语约束和证据重排模块
贡献：希望强调回答可靠性和证据一致性
```

## Expected Output

```markdown
## Draft

Domain-specific question answering requires models to generate responses that are not only fluent but also grounded in reliable evidence. This requirement is particularly important in specialized domains, where terminology is precise and answers often depend on context-specific knowledge. Although retrieval-augmented generation provides a practical way to incorporate external evidence, generated responses may still contain unsupported statements when retrieved passages are noisy or insufficiently aligned with the question.

To address this issue, this study proposes a retrieval-augmented generation framework with terminology constraints and evidence reranking. The terminology constraints are designed to improve the consistency of domain-specific expressions, while the evidence reranking module aims to prioritize passages that are more relevant to the user's question. This design seeks to improve the reliability and evidence consistency of generated answers.

## Writing Logic

- Establishes the broad importance of domain-specific question answering.
- Identifies the reliability problem in retrieval-augmented generation.
- Introduces the proposed modules as a response to that problem.
- Avoids claiming improved performance before experimental results are provided.

## Missing Information

- Target domain.
- Dataset or evaluation benchmark.
- Evaluation metrics for reliability and evidence consistency.
- Quantitative results.
```

