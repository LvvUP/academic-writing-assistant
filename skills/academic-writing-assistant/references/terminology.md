# Terminology

Two related jobs: choosing the right English term for a Chinese one, and keeping one term used consistently through a draft.

## Choosing the term

The right English term is the one the field's papers actually use — not the most literal translation, and not the most general one.

Three failure modes:

**Over-literal.** 图像增强 is "image enhancement" in a signal-processing context, but "data augmentation" when it refers to training-time transformations. The Chinese phrase is the same; the English terms are not interchangeable and using the wrong one confuses reviewers about what was done.

**Over-general.** 网络 → "network" loses information where "architecture," "model," or "backbone" is meant.

**Invented compound.** Literal assembly produces plausible-sounding terms that no one in the field uses ("feature merging" where "feature fusion" is standard). Fluent but immediately non-native.

When a term is ambiguous, put both options in the terminology table with the distinguishing context, and let the author choose. They know which one they mean; you are inferring.

## Common CN→EN pairs

| 中文 | English | 注意 |
|---|---|---|
| 目标检测 | object detection | 不用 target detection |
| 语义分割 | semantic segmentation | |
| 实例分割 | instance segmentation | |
| 特征提取 | feature extraction | |
| 特征融合 | feature fusion | 不用 feature merging |
| 多尺度特征 | multi-scale features | |
| 注意力机制 | attention mechanism | |
| 鲁棒性 | robustness | |
| 泛化能力 | generalization ability / generalization | 英文中常直接用 generalization |
| 消融实验 | ablation study | 不用 ablation experiment |
| 对比实验 | comparative experiments / comparison with baselines | |
| 评价指标 | evaluation metric | |
| 骨干网络 | backbone | |
| 下游任务 | downstream task | |
| 预训练 | pre-training | |
| 微调 | fine-tuning | |
| 数据增强 | data augmentation | 与 image enhancement 区分 |
| 过拟合 | overfitting | |
| 端到端 | end-to-end | |
| 医学图像分割 | medical image segmentation | |
| 病灶检测 | lesion detection | |
| 外部验证 | external validation | 临床论文中的关键区分 |
| 遥感图像 | remote sensing image | |
| 变化检测 | change detection | |
| 空间分辨率 | spatial resolution | |
| 域适应 | domain adaptation | |
| 显著性 | saliency（视觉）/ significance（统计） | 两者不可混用，误用会造成实质性歧义 |
| 精度 | accuracy / precision | 中文"精度"歧义；precision 是特定指标，需按语境确定 |
| 性能 | performance | |
| 实时 | real-time | 有明确技术含义，需延迟数据支撑 |
| 有效性 | effectiveness | |
| 先进性 | 通常不直译；改为具体优势 | "advancement" 在英文中读作空洞主张 |

Two entries deserve extra care. **显著性** collapses two unrelated concepts — a saliency map and statistical significance — and mistranslation produces a claim the author never made. **精度** maps to both "accuracy" and "precision," which are different metrics; when the source is ambiguous, ask rather than pick.

## Consistency within a draft

One concept, one term. See `consistency-pass.md` for the full procedure.

Common Chinese variant pairs that should not be mixed within one manuscript:

- 目标检测 / 对象检测
- 语义分割 / 语义划分
- 鲁棒性 / 稳健性
- 泛化能力 / 泛化性能
- 医学图像分割 / 医学影像分割
- 遥感图像 / 遥感影像
- 变化检测 / 变更检测
- 优化目标 / 目标函数
- 训练集 / 训练数据集

Normalize to the author's dominant usage. Where both are standard in the field (遥感图像 vs 遥感影像 genuinely are), consistency matters more than the choice, and the choice belongs to the author.

Do check whether the draft distinguishes two nearby terms deliberately before normalizing. 优化目标 and 目标函数 can be used deliberately for different things — the training objective versus the mathematical function — and flattening that distinction damages the paper.

## Script

```bash
python scripts/terminology_checker.py draft.md
```

Rule-based scanning against the bundled map. It reports co-occurring variants; it does not judge which is correct, and it does not detect the harder problem of one term used for two concepts. Treat the output as a list to review, not a set of edits to apply.

Extend coverage by editing `assets/terminology-map.zh-en.json`, or point at a custom map with `--map`.
