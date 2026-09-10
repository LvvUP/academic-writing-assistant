# Terminology

术语一致性先判断是否同一概念，再考虑表达统一。词表提供候选，不提供科学定义的最终裁决。

## Selection

优先作者定义、用户给定术语表和本次实际读取的领域材料。模糊术语可给少量候选与适用语境；没有支持时不声称“英文只能这样写”。方法名称或引用中固定写法保持原样。

## Consistency

同一概念存在表达变体时，可建议使用作者主用形式；真正改变概念则为 L3，需材料支持。尤其保留这些可能有意义的区别：

- feature fusion / feature aggregation / feature merging；
- 泛化能力 / 泛化性能；
- 外部验证 / 外部测试；
- gold standard / reference standard / ground truth；
- spatial resolution / ground sample distance；
- 优化目标 / 目标函数；
- 预训练模型 / 预训练语言模型。

这些不是永久不能互译的禁用对；是否等义取决于实际定义与上下文。不要仅凭共现、使用频次或推荐字段自动替换。

## Script

```text
python3 -B <skill-root>/scripts/terminology_checker.py <稿件路径>
```

脚本根据 `assets/terminology-map.zh-en.json` 报告配置词项的共现。它不判断两词是否同义，也不完整检测一词多义。自定义词表可通过 `--map` 提供，仍须结合材料复核。输入路径在用户任务上下文中解析，默认资源随安装包定位。
