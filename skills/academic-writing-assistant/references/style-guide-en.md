# English Academic Style Guide

Written primarily for editing English manuscripts by Chinese-native authors, since that is this Skill's main use. The interference-pattern section is the highest-value part: these errors are systematic rather than random, so recognizing the pattern fixes many instances at once and teaches the author something reusable.

## Contents

- [Register](#register)
- [Interference patterns](#interference-patterns)
- [Hedging](#hedging)
- [Sentence construction](#sentence-construction)
- [Word choice](#word-choice)
- [Connectives](#connectives)
- [Articles](#articles)
- [Venue variation](#venue-variation)

## Register

Academic English is precise, not ornate. The most common misconception among authors polishing their own work is that longer words and heavier constructions sound more scholarly. They do the opposite — they read as translated, or as padding.

Aim for: specific verbs, concrete subjects, claims bounded by evidence, sentences that carry one idea each.

Avoid: nominalizations that hide the verb, stacked prepositional phrases, intensifiers with no evidential content, and ceremonial phrasing that survives from Chinese convention.

## Interference patterns

These come from Chinese structure and appear in almost every draft. Fixing them systematically transforms a manuscript.

### 1. Ceremonial openers

`随着……的快速发展` → "With the rapid development of deep learning, …"

Standard in Chinese, near-meaningless in English, and it occupies the most valuable sentence in the paper. Open with the specific problem instead.

> ❌ With the rapid development of computer vision technology, object detection has attracted increasing attention from researchers.
> ✅ Detecting small objects in aerial imagery remains unreliable at ground sample distances below 0.5 m.

### 2. Significance ceremony

`具有重要的理论意义和应用价值` → "has important theoretical significance and application value"

In Chinese this is conventional framing. In English it reads as an unsupported grand claim, and reviewers register it as inflation. Replace with the specific implication or cut entirely. Flag as L3 — authors are often surprised, since the phrase felt neutral to them.

### 3. Nominalization

Chinese uses `进行/实现/开展 + noun` naturally. Translated literally it buries the verb.

| Heavy | Direct |
|---|---|
| perform the processing of the images | process the images |
| carry out an analysis of the results | analyze the results |
| achieve the improvement of accuracy | improve accuracy |
| conduct the training of the model | train the model |
| make a comparison with | compare with |

### 4. Hedge stacking

`往往会在一定程度上有所提升` → "may to some extent potentially improve somewhat"

Chinese tolerates layered hedges; English reads them as evasion or as a non-native marker. One hedge, chosen deliberately, is stronger than four.

### 5. Connective chains

由于……因此……从而……进而 maps to a chain of English connectives that produces one exhausting sentence. Break into two or three sentences and keep only the connectives that carry real logical weight.

### 6. Topic-comment structure

Chinese fronts the topic; English wants subject-verb early.

> ❌ For the problem of insufficient labeled data in medical image segmentation, a semi-supervised framework is proposed in this paper.
> ✅ We propose a semi-supervised framework that addresses the scarcity of labeled data in medical image segmentation.

### 7. Missing articles

Chinese has no articles, making this the single most frequent grammatical error. It is L1 work, applied at volume — no need to enumerate each fix.

### 8. Countability

`research`, `literature`, `evidence`, `equipment`, `software`, `information`, `progress`, `work` are uncountable. "Many researches" and "the literatures" are immediate non-native markers. Use "many studies," "the literature."

### 9. "Respectively" misuse

Correct: "A and B achieved 91.2% and 88.7%, respectively." Not a general-purpose "separately" or a sentence-opener.

### 10. Overusing "effectively"

`有效地` attaches to almost any verb in Chinese. In English, "effectively improves" adds no information and reads as filler — plus "effectively" ambiguously means "in effect." Usually just delete it.

## Hedging

The load-bearing zone. See `fidelity-protocol.md` for the strength ladder.

Calibrate to the section: introductions and discussions hedge; method sections describe what was done without hedging ("The encoder extracts features," not "The encoder may extract features"); results report what happened.

Hedge the interpretation, not the observation. "Accuracy increased by 3.2 points" is a fact and needs no hedge. "This increase suggests the module captures finer detail" is an interpretation and does.

## Sentence construction

- One main idea per sentence. Chinese comma-splicing carries longer chains than English does.
- Given information first, new information last — this is what makes paragraphs flow, more than any connective.
- Keep subject and verb close; long intervening clauses lose the reader.
- Parallel structure in lists, especially contribution bullets.
- Vary length deliberately. Uniform 25-word sentences are a strong machine-text signal.
- Passive voice is fine when the actor is irrelevant or obvious ("Images were resized to 224×224"). It is not a virtue in itself, and modern venues generally accept "we."

## Word choice

| Weak | Better |
|---|---|
| very good / very important | strong, substantial — or state the magnitude |
| a lot of experiments | extensive experiments |
| get better features | learn more discriminative features |
| solve the problem | address the problem |
| the result is not good | performance degrades |
| make the model better | improve the model's [specific property] |
| has big value | [state the specific implication] |
| prove (from experiments) | demonstrate, indicate, provide evidence for |
| obvious improvement | consistent improvement, a 3.2-point gain |
| study on / research on X | investigate X |

Verbs that carry precise meaning in academic English: demonstrate, indicate, suggest, reveal, mitigate, alleviate, address, investigate, evaluate, validate, formulate, characterize, quantify, outperform, degrade, converge.

## Connectives

Overuse is a machine-text marker and a translation artifact. Most well-ordered paragraphs need few — good information order does the work.

- **Addition**: Moreover, Furthermore, In addition — do not open consecutive paragraphs with these
- **Contrast**: However, In contrast, Nevertheless — "However" mid-sentence after a comma is a comma splice; use a semicolon or a new sentence
- **Cause**: Therefore, Consequently, As a result — note that "Thus" and "Hence" are heavier and less common in modern prose
- **Concession**: Although, While, Despite

Never open with "Besides" (colloquial in this position) or "On the other hand" without a preceding "On the one hand."

## Articles

The compressed rule, since this is where most errors land:

- First mention of a countable singular: "a" / "an"
- Subsequent mention, or uniquely identified: "the"
- Generic plural: usually no article — "Neural networks require large datasets"
- Specific plural: "the" — "The networks used in this study"
- Named datasets and methods: usually no article ("on ImageNet"), but "the ImageNet dataset"
- Sections, figures, tables with numbers: no article ("in Section 3," "Table 2 reports")
- Superlatives and ordinals: "the" — "the best performance," "the first stage"

## Venue variation

Adjust rather than applying one house style:

- **CS conferences** (CVPR, NeurIPS, ACL): first person normal, present tense for method, compact, results-forward.
- **IEEE Transactions**: more formal, fuller methodological detail, more passive constructions.
- **Medical and clinical journals**: strict structured abstracts, heavy hedging, causal language tightly controlled, CONSORT/STROBE-style reporting conventions.
- **Nature/Science family**: short, broad-audience framing, minimal jargon in the opening, strict word limits.
- **Chinese-published English journals**: often expect a more formal register than Western CS venues.

When the venue is unknown, use a neutral formal register and say which assumption you made.
