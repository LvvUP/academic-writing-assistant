# Task Router

Classify the user's academic writing request before drafting. If a request contains multiple tasks, handle them in a safe order: clarify source meaning, then revise or translate, then explain changes.

## Routing Table

| Task | Common user wording | Route to |
|---|---|---|
| Academic Polishing | 润色, 学术化, 更正式, 更像论文, polish, revise language | Polishing workflow |
| Academic Expansion | 扩写, 丰富, 补充背景, 加强逻辑, expand | Expansion workflow |
| Paragraph Merging | 合并, 整合, 多段变一段, merge | Merging workflow |
| CN to EN Translation | 翻译成英文, SCI 英文, English academic expression | CN to EN translation workflow |
| EN to CN Translation | 翻译成中文, 中文解释, academic Chinese translation | EN to CN translation workflow |
| Abstract Writing | 摘要, abstract | Abstract workflow |
| Introduction Writing | 引言, introduction, 研究背景, contribution | Introduction workflow |
| Related Work Organization | 相关工作, related work, literature review | Related work workflow |
| Method Section Writing | 方法, method, framework, algorithm | Method workflow |
| Experiment Section Writing | 实验, experiment, results, ablation | Experiment workflow |
| Discussion / Limitation / Future Work | 讨论, 局限, future work, conclusion | Discussion workflow |
| Reviewer Response Drafting | 审稿人, reviewer, rebuttal, response letter | Reviewer response workflow |
| Title Optimization | 标题, title, 题目优化 | Title optimization workflow |
| Terminology Consistency Checking | 术语, 统一表达, terminology consistency | Terminology workflow |
| Academic Naturalization | 降低机器翻译感, 更自然, academic naturalization | Naturalization workflow |
| Prompt Optimization | 优化 prompt, 学术写作提示词, prompt optimization | Prompt optimization workflow |

## Ambiguous Requests

If the user says "帮我改一下", infer the task from context:

- Source paragraph + "像论文": polishing.
- Source paragraph + "更完整": expansion.
- Two or more paragraphs + "整合": merging.
- Chinese source + "SCI": CN to EN translation unless the user asks for Chinese style.
- Reviewer comment included: reviewer response.

If the source text is missing, ask for it. If the research field is missing, infer from terms or proceed with general academic style and state the assumption.

## Multi-Step Requests

Use this order when multiple tasks are requested:

1. Identify field and terminology.
2. Preserve or clarify technical meaning.
3. Translate or revise.
4. Improve structure.
5. Add notes, uncertainty, and missing information.

Do not add literature, dataset names, metric values, or reviewer-response claims that the user did not provide.

