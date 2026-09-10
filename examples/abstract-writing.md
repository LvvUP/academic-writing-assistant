# 摘要写作示例：结果尚未就绪

以下为合成任务，不代表真实研究。

## User Input

```text
请根据以下信息写一个英文摘要，仅输出正文：
研究方向：小目标检测
问题：小目标特征弱，容易被复杂背景干扰
方法：加入上下文增强模块和多尺度特征融合模块
实验：还未完成
```

## Expected Output

```text
Small object detection is challenging because small objects have weak features
and are easily affected by complex backgrounds. This study uses a context
enhancement module and a multi-scale feature fusion module. Experimental
evaluation remains incomplete.
```

## 验收要点

- 可按给定问题与模块名称起草；不推测既有方法下采样丢失特征或模块已改善语义。
- 没有数据集、指标、数值和结果方向的编造。
- 不用 Experiments show that 把未完成实验写成已发生结论。
- 即使只输出正文，也保留作者已明确的未完成状态；不能仅省略结果句。
- 若输入只说“没有提供结果材料”，只能标明材料待补，不能照搬本例的未完成断言。

## 同一规则用于分析工作稿

以下也是合成任务。作者给定：“综述关注远程教学中的同伴反馈，采用主题综合；文献筛选已结束，综合分析尚未完成。请只写一段中文摘要工作稿。”

可输出：“本综述关注远程教学中的同伴反馈，采用主题综合方法。文献筛选已结束，综合分析尚未完成。”

这里保留的是已知的分析状态，不补造综合结论，也不要求该综述开展实验。
