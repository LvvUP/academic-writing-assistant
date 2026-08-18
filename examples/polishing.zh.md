# 中文论文段落润色示例

## Task

Academic Polishing

## Field

Medical Imaging

## User Input

```text
我是做医学影像分割的，请帮我把下面这段话润色成 SCI 论文风格：

我们的方法可以减少标注困难的问题，而且分割结果比较好，对小病灶也有帮助。
```

## Expected Output

```markdown
## 修改后文本

The proposed method alleviates the annotation burden in medical image
segmentation and improves the delineation of small lesions compared with the
evaluated baselines. [请补充数据集、评价指标与具体数值]

## 改动台账

L1（语法/冠词/时态）：共 3 处，未逐条列出。

| # | 原文 | 修改后 | 层级 | 原因 |
|---|---|---|---|---|
| 1 | 减少标注困难的问题 | alleviates the annotation burden | L2 | 名词化压缩，语义未变 |
| 2 | 分割结果比较好 | improves the delineation ... compared with the evaluated baselines | L3 | "比较好"没有对照对象。英文论文中的性能表述需说明与谁比较，否则审稿人必然追问 |

## 需确认

- 使用了哪些数据集与评价指标（Dice / IoU / HD95）？
- "现有方法"具体指哪些 baseline？
- 标注负担的降低是否有量化口径（标注时长 / 像素量 / 样本数）？
```

## 说明

注意输出中**没有编造任何数值**来把句子补完整。缺失信息以醒目占位符呈现，L3 改动给出了理由，作者据此可以判断是否接受。
