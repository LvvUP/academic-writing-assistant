# 中译英示例

## Task

CN to EN Academic Translation

## Field

Remote Sensing

## User Input

```text
请将以下中文段落翻译成适合 SCI 论文的英文表达，并给出术语表：

针对遥感图像中目标尺度变化大、背景复杂的问题，本文提出一种多尺度特征融合方法，
该方法具有重要的理论意义和应用价值。
```

## Expected Output

```markdown
## English Translation

To address the large scale variation and complex backgrounds in remote sensing
images, this study proposes a multi-scale feature fusion method.

## 术语选择

| 中文 | English | 说明 |
|---|---|---|
| 遥感图像 | remote sensing images | 遥感领域标准表述 |
| 目标尺度变化 | scale variation | 比 target scale change 更符合领域惯例 |
| 多尺度特征融合 | multi-scale feature fusion | 通用表述；不用 feature merging |

## 翻译说明

- 删除了"具有重要的理论意义和应用价值"（L3）。这类表述在中文论文中是惯例性
  收尾，直译为 "has important theoretical significance and application value"
  在英文中会被读作缺乏支撑的宏大主张。若希望保留这层意思，建议改为具体陈述，
  例如该方法适用于哪类实际任务——需要你补充。
- 保留了"针对……问题"的问题-方法逻辑结构，主张强度未改变。
- 未添加任何数据集、指标或性能表述。

## 需确认

- 尺度变化针对的目标类型（车辆 / 建筑 / 船舶）？具体化能提升标题与摘要的检索性。
```

## 说明

中文论文的惯例性收尾（"具有重要意义"、"随着……的快速发展"、"众所周知"）直译
到英文后会变成审稿人敏感的空泛主张。这类改动属于 L3，需要说明——多数作者并不
知道这个短语在英文里不成立。
