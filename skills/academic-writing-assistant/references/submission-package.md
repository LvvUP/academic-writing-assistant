# Submission Package

Everything that goes alongside the manuscript. These are short documents, they are read by editors rather than reviewers, and authors routinely underestimate how much the cover letter and the AI disclosure matter.

## Contents

- [Cover letter](#cover-letter)
- [Highlights](#highlights)
- [Graphical abstract text](#graphical-abstract-text)
- [AI use disclosure](#ai-use-disclosure)
- [Author contribution statements](#author-contribution-statements)
- [Suggested reviewers](#suggested-reviewers)
- [Response to a desk rejection](#response-to-a-desk-rejection)

## Cover letter

Read by a handling editor deciding whether to send the paper out for review at all. One page, three or four paragraphs.

1. **What the paper is.** Title, and one sentence on the core finding — the actual result, not the topic.
2. **Why this journal.** Specific: the question fits the journal's scope, extends work it has published, or serves its readership. Generic flattery ("your prestigious journal") is transparently boilerplate.
3. **What is new.** Two or three sentences. The contribution, bounded by what the paper actually shows.
4. **Compliance statements.** Original work, not under consideration elsewhere, all authors approved, conflicts of interest, ethics approval and data availability where applicable.

Common failures worth catching:

- Reproducing the abstract. The editor already has the abstract; the letter should say something it does not.
- Overclaiming. The letter is the easiest place to write "groundbreaking," and the easiest place for it to backfire.
- The wrong journal name — from reusing a letter after a rejection. Check it, and mention this trap to authors who are resubmitting.
- Omitting a prior-submission history the journal requires disclosed.

```text
Dear Professor [Editor],

We submit our manuscript, "[Title]," for consideration in [Journal].

[One or two sentences: what problem, what was done, what was found.]

This work fits [Journal]'s scope because [specific reason tied to the journal's
published work or readership]. To our knowledge, [the specific new element],
which [why it matters to this field].

The manuscript is original, has not been published elsewhere, and is not under
consideration by another journal. All authors have approved the submission and
declare [no competing interests / the interests listed in the manuscript].
[Ethics approval / data availability, if applicable.]

We thank you for your consideration.

Sincerely,
[Corresponding author, affiliation, contact]
```

## Highlights

Elsevier journals ask for 3–5 bullets, each **85 characters maximum including spaces**, covering the core results. Cell Press narrows this to 3–4 bullets at the same limit. AGU journals instead use "Key Points" with a different limit. Check the target journal's own guide — these differ across publishers and sometimes across journals within one publisher.

The character limit is tighter than it looks, and it counts spaces. Count exactly:

```bash
python scripts/manuscript_audit.py highlights.txt --limit-chars 85 --per-line
```

Writing them well:

- Report findings, not topics. "Method X improves segmentation" is a topic; "X raises Dice by 4.1 points on external cohorts" is a finding.
- No abbreviations the reader would need the paper to decode.
- Each bullet stands alone; they are displayed as a list without context.
- Do not waste characters on "This paper presents…"
- Use the author's real numbers, or a placeholder. Never invent one to fit the character budget — the constraint is real but fabrication is not the way to meet it.

## Graphical abstract text

If the user asks for accompanying text, keep it to what the figure shows. Do not describe visual elements that were never described to you — you cannot see the figure.

## AI use disclosure

Most major publishers now require authors to disclose substantive generative-AI assistance, and the requirement has hardened since 2023. Three points hold across essentially all of them:

- **AI cannot be an author.** COPE's reasoning is that authorship entails responsibility, which a tool cannot bear.
- **Human authors remain fully responsible** for everything in the manuscript, including anything a tool produced.
- **Substantive use must be disclosed;** routine grammar and spell checking generally need not be.

Placement and threshold vary, so confirm against the target venue's own guide:

- **Elsevier** asks for a statement at the end of the manuscript, before the reference list, in a titled section: "Declaration of Generative AI and AI-assisted technologies in the writing process." Basic grammar, spelling, and punctuation checks are exempt.
- **Springer Nature** exempts copy-editing style assistance but requires disclosure of substantive use.
- **Wiley** requires disclosure at submission and in the manuscript where relevant.
- **ICMJE**-following journals want it at submission, in the cover letter, and in the work itself.
- **ICLR** requires disclosure of LLM use and treats undisclosed substantive use as a Code of Ethics violation, with desk rejection applied in practice. **NeurIPS** requires disclosure of methodologically significant or non-standard LLM/agent use, and track policies differ within the same conference.

Image generation is a stricter tier almost everywhere: generative AI is generally not permitted for creating or altering research images except as documented methodology.

Template, adapted from the Elsevier form:

```text
Declaration of Generative AI and AI-assisted technologies in the writing process

During the preparation of this work the author(s) used [tool name] in order to
[specific purpose, e.g. improve the readability and language of the manuscript /
translate an earlier draft from Chinese to English]. After using this tool, the
author(s) reviewed and edited the content as needed and take full responsibility
for the content of the published article.
```

Chinese version:

```text
生成式人工智能及人工智能辅助技术使用声明

在本文撰写过程中，作者使用了 [工具名称]，用于 [具体用途，例如：提升语言表达的可读性 /
将中文初稿翻译为英文]。使用该工具后，作者已对相关内容进行审阅与修改，并对论文的全部
内容负责。
```

Guidance to give the user: describe the actual use narrowly and factually. Language polishing and translation are ordinary and disclosing them costs nothing. What creates risk is the mismatch — heavy use of a tool for drafting content, disclosed as "minor language editing," or not disclosed at all. Point them to their venue's guide, because thresholds genuinely differ.

## Author contribution statements

Many journals require CRediT taxonomy roles: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Resources, Data curation, Writing – original draft, Writing – review & editing, Visualization, Supervision, Project administration, Funding acquisition.

Map only what the user tells you about who did what. Author contributions are a factual claim about people, and guessing at them is worse than leaving a placeholder.

```text
[Author A]: Conceptualization, Methodology, Writing – original draft.
[Author B]: Software, Validation, Visualization.
[Author C]: Supervision, Funding acquisition, Writing – review & editing.
```

## Suggested reviewers

Some journals ask for candidate reviewers. Do **not** invent names — this is fabrication of the most checkable kind, and inventing a plausible expert with a plausible affiliation is a serious integrity failure.

Explain the selection criteria instead: researchers publishing on the same problem, not at the authors' institutions, no recent co-authorship or shared funding, spread across groups and countries. Let the author supply the actual names from work they have read.

## Response to a desk rejection

Usually the right advice is to move on rather than appeal — appeals rarely succeed and cost weeks. Appeal only when there is a factual error in the editor's stated reason.

If appealing: address the editor's specific reason with evidence, keep it to a few paragraphs, stay unemotional, and accept the outcome. If the rejection was for scope, help the author identify a better-fitting venue and revise the framing rather than the science.
