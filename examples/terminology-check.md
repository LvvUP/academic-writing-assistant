# 术语一致性检查示例

## Task

Terminology Consistency Checking

## User Input

```text
本文关注目标检测任务。与传统对象检测方法相比，所提出模型在复杂背景下具有更好的鲁棒性。与此同时，模型的稳健性仍需要在更多场景中验证。
```

## Expected Output

```markdown
## 建议统一术语

| 原始表达 | 建议统一表达 | 说明 |
|---|---|---|
| 目标检测 / 对象检测 | 目标检测 | 中文计算机视觉论文中通常使用“目标检测”。 |
| 鲁棒性 / 稳健性 | 鲁棒性 | 计算机视觉论文中“鲁棒性”更常见；若全文已统一使用“稳健性”，也可保留。 |

## 不建议混用

- 同一段落中不建议同时使用“目标检测”和“对象检测”。
- “鲁棒性”和“稳健性”应根据全文风格择一使用。

## 修订建议

将“对象检测”统一为“目标检测”，并将“稳健性”统一为“鲁棒性”或在全文中保持另一种一致表达。
```

## Script Example

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py examples/terminology-check.md
```

