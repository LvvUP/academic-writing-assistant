# Citation Safety

## Core Rule

Never fabricate references, citations, authors, venues, publication years, paper titles, DOI values, arXiv IDs, or bibliographic metadata.

## When User Provides References

1. Use only the provided references.
2. Preserve citation numbering or author-year style when possible.
3. Do not add new references unless the user explicitly asks and reliable search or verified source content is available.
4. If a citation seems mismatched, flag it instead of silently correcting it.

## When User Does Not Provide References

If the user asks for Related Work or literature review but provides no references:

- write a citation-free structural draft;
- use placeholders such as `[related studies]`;
- or ask the user to provide references if specific citation support is required.

Do not generate plausible-looking fake references.

## Safe Phrases

Use:

- "Prior studies have explored..."
- "Existing methods can be broadly categorized into..."
- "A common limitation of this line of work is..."

Avoid unless verified:

- "Smith et al. (2021) proposed..."
- "This method has been widely validated in clinical practice..."
- "The dataset contains X samples..."

