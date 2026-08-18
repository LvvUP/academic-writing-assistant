# 摘要写作示例（实验结果尚未就绪）

## Task

Abstract Writing

## Field

Computer Vision

## User Input

```text
请根据以下信息写一个英文摘要：

研究方向：小目标检测
问题：小目标特征弱，容易被复杂背景干扰
方法：加入上下文增强模块和多尺度特征融合模块
实验：目前还没有整理最终结果
```

## Expected Output

```markdown
## Abstract Draft

Small object detection remains difficult because small targets carry limited
visual evidence and are easily confounded by complex backgrounds. Existing
detectors typically lose these cues during downsampling. This work proposes a
detection framework combining a context enhancement module, which strengthens
surrounding semantic information, with a multi-scale feature fusion module,
which preserves representation across object scales. Experiments on
[请填写数据集名称] using [请填写评价指标] show that the method achieves
[请填写主要数值] compared with [请填写对比方法].

## 写作逻辑

- 问题 → 现有方法的具体不足 → 本文方法 → 实验验证 → 结论
- 结论句按"待实验数据确定"处理，未预设结果方向

## 缺失信息

- 数据集名称与规模
- 评价指标（mAP / AP50 / APs）
- 主要定量结果
- 对比方法
- 是否进行显著性检验（决定能否使用 significantly）

注意：以上占位符必须在投稿前替换。当前草稿中没有任何虚构数值。
```

## 说明

摘要是编造数值风险最高的场景——作者急于看到"完整"的摘要，而一个看起来合理的
mAP 数字几乎不会被察觉。占位符使用中文方括号，无法被误认为正文。
