# Design

## Goal

Academic Writing Assistant turns scattered academic writing prompts into a structured Skill that can route tasks, adapt to fields, produce stable outputs, and preserve academic integrity.

## Architecture

- `SKILL.md`: concise trigger, principles, routing entry, and quality requirements.
- `references/`: detailed task routing, field adaptation, writing workflows, style guides, templates, and safety rules.
- `assets/`: terminology maps for deterministic checks.
- `scripts/`: lightweight, dependency-free helper scripts.
- `examples/`: safe usage examples.
- `evals/`: manual acceptance and pressure tests.
- `tests/`: automated checks for structure and scripts.

## Design Choices

1. Keep the core Skill short so agents load only essential instructions.
2. Put field-specific and task-specific detail in references for progressive disclosure.
3. Use explicit output templates to reduce inconsistent responses.
4. Include helper scripts only where deterministic checks are useful.
5. Treat academic integrity as a design constraint, not an appendix.

## Non-Goals

- It does not promise publication or review acceptance.
- It does not replace domain expert review.
- It does not generate verified references without source material.
- It does not judge scientific validity beyond user-provided evidence.

