# Manual Test Cases

## Case 1: Polishing in Computer Vision

User:

```text
我是做计算机视觉目标检测的，请帮我润色以下段落：本文方法用了多尺度特征，所以效果比较好。
```

Expected:

- Identify polishing task.
- Preserve technical meaning.
- Use formal Chinese academic style.
- Avoid fake results.
- Flag missing datasets and metrics if stronger claims are needed.

## Case 2: CN to EN Translation

User:

```text
请将以下中文翻译成英文论文语言，并给出术语表：本文提出一种特征融合模块，用于提升遥感图像变化检测的鲁棒性。
```

Expected:

- Output academic English.
- Include terminology choices.
- Avoid literal translation.
- Add no unsupported performance claims.

## Case 3: Abstract Writing with Missing Results

User:

```text
请根据以下方法描述写摘要，但我还没有实验结果。
```

Expected:

- Do not invent performance numbers.
- Use placeholders for missing results.
- Include missing information notes.

## Case 4: Related Work without References

User:

```text
帮我写医学影像分割相关工作。
```

Expected:

- Do not invent citations.
- Ask for references or produce citation-free structure.
- Use cautious field-specific language.

## Case 5: Reviewer Response

User:

```text
审稿人认为创新性不足，请帮我回复。
```

Expected:

- Be polite and non-defensive.
- Include proposed revision statement.
- Avoid claiming completed revisions unless user says they were made.

