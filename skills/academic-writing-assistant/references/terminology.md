# Terminology Consistency

## Goal

Ensure consistent academic terminology across Chinese and English paper drafts.

## Common CN to EN Terms

| 中文 | English |
|---|---|
| 目标检测 | object detection |
| 语义分割 | semantic segmentation |
| 实例分割 | instance segmentation |
| 特征提取 | feature extraction |
| 特征融合 | feature fusion |
| 多尺度特征 | multi-scale features |
| 注意力机制 | attention mechanism |
| 鲁棒性 | robustness |
| 泛化能力 | generalization ability |
| 消融实验 | ablation study |
| 对比实验 | comparative experiment |
| 评价指标 | evaluation metric |
| 医学图像分割 | medical image segmentation |
| 病灶检测 | lesion detection |
| 遥感图像 | remote sensing image |
| 变化检测 | change detection |

## Common Inconsistencies

Avoid mixing within the same manuscript unless intentionally defined:

- 目标检测 / 对象检测
- 语义分割 / 语义划分
- 鲁棒性 / 稳健性
- 泛化能力 / 泛化性能
- 特征融合 / 融合特征 / 多特征融合
- 医学图像分割 / 医学影像分割
- 遥感图像 / 遥感影像

When inconsistency is found, recommend one standard term and explain why. If the paper has already consistently used a variant, recommend preserving consistency rather than forcing a different term.

## Script

Run the bundled checker:

```bash
python skills/academic-writing-assistant/scripts/terminology_checker.py path/to/draft.md
```

It performs transparent rule-based scanning only. It does not replace expert review.

