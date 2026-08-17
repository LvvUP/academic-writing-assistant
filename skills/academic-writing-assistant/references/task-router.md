# Task Router

Read this when the request is ambiguous, bundles several tasks, or arrives as bare text with no instruction. Clear single-task requests can go straight to `writing-workflows.md`.

## Reading the request

Most requests are unambiguous once you look at what came with the text rather than only at the instruction.

| Signal in the message | Almost certainly |
|---|---|
| Chinese source + "SCI" / "投稿" / "英文" | CN→EN translation |
| Chinese source + "润色成英文" / "改成论文英文" | Translation **and** polishing at once — the single most common request. Translate as the spine, diagnose structure first, report as a translation |
| Reviewer's words quoted, or "审稿人" | Reviewer response — then check journal vs. conference |
| Two or more paragraphs + "整合" / "合并" | Merging |
| A word or character limit named | Compression to a limit |
| `\cite{}`, `\begin{}`, `$…$` in the text | LaTeX-aware editing — see `latex-and-formats.md` |
| A full section or whole paper | Consistency pass — see `consistency-pass.md` |
| "毕业论文" / "学位论文" / "开题" | Thesis conventions — see `style-guide-zh.md` |
| A journal or conference named | Set register from the venue; check its limits |
| "降 AI 率" / "降重" / "查重" | Redirect — see below |

## Ambiguous instructions

"帮我改一下" and "看看这段" are the most common inputs in practice. Infer from the text itself:

- Reads like a paper, has grammar problems → polishing
- Chinese text, user writes in Chinese, no direction stated → ask whether they want Chinese polishing or English translation. These produce completely different outputs, and guessing wrong wastes the whole response. This is one of the few questions worth asking up front.
- Reads fine but is short and thin → they may want expansion; check whether the gap is logical or they are chasing length
- Contains a reviewer's words → reviewer response, regardless of how it was introduced

When the task is clear but the field or venue is not, infer and label the inference. Do not ask.

## Bare text with no instruction

Users often paste a paragraph and nothing else. Default to polishing in the source language, keep it light, and offer the adjacent options in one line: "已按学术润色处理；如需译成英文或压缩到摘要字数，告诉我即可。"

Do not respond with only a question. A best-effort draft plus one question is strictly better than a question alone.

## Multiple tasks in one request

Order matters, because later steps depend on earlier ones being right.

1. Resolve meaning — ask about genuine ambiguity in the source
2. Fix content and structure — the argument, before the words
3. Translate or polish
4. Enforce consistency across the result
5. Compress to any limit
6. Report the ledger and queries

Compression comes last deliberately: cutting before the argument is settled removes the wrong things.

## Requests to redirect

**"降低 AI 率" / "绕过 AI 检测" / "降重" / "过查重".** Do not frame the work as evading a detector. Say so plainly, then do the thing that actually helps — because the underlying need is usually real. Text flagged as machine-generated is typically vague, uniformly weighted, and hedge-heavy, and fixing that is ordinary editing. For similarity checking, the legitimate fix is proper quotation, citation, and genuine rewriting of one's own summary of prior work, not word-substitution.

Be brief about the boundary and generous with the actual help. A lecture is not what the user came for.

**"帮我写一篇关于 X 的论文."** Writing an entire paper from a topic means inventing methods, experiments, and results. Explain what is missing and offer what is real: structure a draft from their actual work, or draft a specific section from material they provide.

**"帮我找几篇相关文献."** You cannot verify references that are not in front of you. Do not produce a list. Offer instead: a search strategy with the right query terms, a structural outline with `[citation needed]` slots, or work with references the user pastes in. See `citation-safety.md`.

## Then

Once routed, go to `writing-workflows.md` for the technique, `output-templates.md` for the shape, and run `quality-checklist.md` before answering.
