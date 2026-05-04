# Writing Workflows

Use these workflows to structure manuscript-ready drafts. Separate user-provided facts from suggested placeholders.

## Academic Polishing

1. Preserve claim scope, data, methods, and limitations.
2. Improve grammar, coherence, transitions, and academic tone.
3. Replace colloquial or promotional wording with objective expressions.
4. Return change notes and uncertainty notes.

## Academic Expansion

1. Identify the sentence-level logical gap: background, motivation, mechanism, implication, or transition.
2. Add only generic academic logic supported by the user's content.
3. Use placeholders for missing evidence.
4. Explain which ideas were added.

## Paragraph Merging

1. Identify repeated claims and overlapping concepts.
2. Keep one clear topic sentence.
3. Preserve necessary technical conditions.
4. Compress repetition and explain what was merged or removed.

## CN to EN Academic Translation

1. Translate meaning, not Chinese word order.
2. Preserve technical terms, logical relations, and hedging.
3. Prefer natural academic English.
4. Provide terminology choices when useful.

## EN to CN Academic Translation

1. Preserve technical terms and evidence boundaries.
2. Use formal Chinese academic expression.
3. Avoid casual explanations unless requested.
4. Provide key terminology notes.

## Abstract Writing

Use this structure:

1. Background.
2. Research problem.
3. Proposed method.
4. Experiments or validation.
5. Main conclusion.

Rules:

- Do not invent numerical results.
- If performance values are missing, use `[please add main quantitative results]`.
- Keep the abstract concise, information-dense, and evidence-bounded.

## Introduction Writing

Use this logic chain:

1. Broad research background.
2. Importance of the problem.
3. Limitations of existing methods.
4. Motivation for the proposed method.
5. Summary of the proposed method.
6. Main contributions.

Contribution style:

- Use 2-4 contribution points.
- Avoid "first", "best", or "state-of-the-art" unless verified.
- Tie each contribution to method design or evidence provided by the user.

## Related Work Organization

Choose one organization strategy:

- by method category;
- by research problem;
- by technical limitation;
- by chronological development only when history matters.

Rules:

- Do not invent references.
- If no references are provided, write a citation-free structure or ask for references.
- End with a transition that explains the current work's motivation without attacking prior work.

## Method Section Writing

Suggested structure:

1. Overview.
2. Problem formulation.
3. Model architecture or pipeline.
4. Module descriptions.
5. Loss function or optimization objective.
6. Training or inference procedure.
7. Complexity or implementation notes, if available.

Rules:

- Do not invent equations.
- Introduce symbols conservatively.
- Distinguish confirmed details from recommended additions.

## Experiment Section Writing

Suggested structure:

1. Dataset description.
2. Evaluation metrics.
3. Implementation details.
4. Comparison methods.
5. Main results.
6. Ablation studies.
7. Qualitative analysis or visualization.
8. Failure cases or limitations.

Rules:

- Do not invent metric values.
- Analyze only provided results.
- Use placeholders for missing numbers, datasets, baselines, or settings.

## Discussion, Limitation, and Future Work

Address:

- why the method may work;
- where it performs well based on provided evidence;
- where it may fail;
- limitations;
- future work.

Use cautious language such as "may", "suggest", "on the evaluated datasets", and "further validation is required".

## Reviewer Response Drafting

Use the dedicated `reviewer-response.md` reference. Always be polite, specific, and non-defensive. Do not claim that changes were made unless the user says so or asks for a proposed response.

## Title Optimization

Generate 3-5 candidates:

- descriptive title;
- method-focused title;
- problem-focused title;
- concise title.

Avoid exaggerated claims and unverified novelty.

## Academic Naturalization

Improve unnatural translation or stiff AI-like phrasing by making the text clearer, less repetitive, and more idiomatic. Do not frame this as evading detection.

## Prompt Optimization

Rewrite the user's academic writing prompt so it specifies:

- task type;
- field;
- language;
- desired output format;
- integrity constraints;
- what to preserve;
- what to flag as uncertain.

