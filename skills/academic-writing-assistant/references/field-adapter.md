# Field Adapter

Use these field notes as possible review questions, not claims about what every reviewer demands. Apply only what fits the research design and supplied material; a concern is a prompt to inspect evidence, not a reason to invent a limitation or predict acceptance.

Use the entries below to know what to watch for and what to flag. Never introduce a field-specific claim the user's text does not support — knowing what reviewers want is not permission to assert it on the author's behalf.

## Contents

- [Working without a listed field](#working-without-a-listed-field)
- [Computer vision](#computer-vision)
- [Machine learning and AI](#machine-learning-and-ai)
- [Natural language processing and LLMs](#natural-language-processing-and-llms)
- [Medical imaging and clinical research](#medical-imaging-and-clinical-research)
- [Remote sensing](#remote-sensing)
- [Robotics](#robotics)
- [Data mining and recommendation](#data-mining-and-recommendation)
- [Bioinformatics](#bioinformatics)
- [Materials science and chemistry](#materials-science-and-chemistry)
- [Social sciences, education, management](#social-sciences-education-management)

## Working without a listed field

The list is a set of presets, not a boundary. For any unlisted field, the same procedure works:

1. Prefer the user's stated field. Otherwise infer from terminology and say so in one line.
2. Select relevant checks from the research design and material; ask only when a missing convention would materially change the task.
3. Keep claims bounded to the evidence in front of you.
4. Use the author's definitions. Confirm two terms denote the same concept before suggesting normalization; frequency does not establish equivalence.

Follow supplied conventions rather than imposing empirical IMRaD; relevant distinctions include: pure mathematics (proof structure), law (citation systems), humanities (argumentative rather than IMRaD structure), qualitative social science (positionality, reflexivity).

## Computer vision

**Possible review questions:** unfair comparison (different backbone, different training budget, different input resolution), benchmark overfitting, missing ablations, claims of robustness with no corruption or distribution-shift testing, cherry-picked qualitative figures.

**Watch for:** "state-of-the-art" without naming the comparison set or date; robustness claimed from clean-benchmark results; efficiency claims with no FLOPs, parameters, or measured latency; ablations that change two things at once.

**Terminology:** feature extraction, feature fusion, object detection, semantic/instance segmentation, attention mechanism, backbone, ablation study, zero-shot, fine-tuning.

## Machine learning and AI

**Possible review questions:** unstated assumptions, generalization claims from a single dataset, missing seed variance and error bars, tuning the proposed method harder than the baselines, "theoretical justification" that does not connect to the algorithm actually implemented.

**Watch for:** "prove" applied to empirical results; "converges" without conditions; a statistical significance claim without an associated analysis in the available material; conflating theoretical assumptions with experimental conditions; claims of general-purpose capability from narrow benchmarks.

**Terminology:** objective function, generalization, regularization, convergence, distribution shift, sample complexity, inductive bias.

## Natural language processing and LLMs

**Possible review questions:** data contamination (test data in pretraining), prompt sensitivity presented as model capability, single-run results from a stochastic system, evaluation by an LLM judge without human validation, unfair inference-budget comparisons.

**Watch for:** claims of "understanding" or "reasoning" where the evidence is task performance; benchmark scores without decoding parameters, prompt, and version; missing contamination analysis for recent benchmarks; unstated model version — behavior shifts across releases, so a claim about "GPT-4" without a date is unreproducible.

**Terminology:** in-context learning, chain-of-thought, instruction tuning, RLHF, retrieval-augmented generation, hallucination, contamination, prompt sensitivity.

## Medical imaging and clinical research

The most consequential field for claim discipline. Overclaiming is not just a reviewing problem here — it can influence clinical practice.

**Possible review questions:** single-center data with no external validation, patient-level versus image-level data leakage, missing demographic breakdown, no comparison against clinician performance, class imbalance masked by accuracy, absent ethics statement.

**Consider when relevant to the actual claim and study design:**

- Diagnostic or prognostic claims whose stated scope exceeds the provided validation
- "clinically applicable," "can assist diagnosis," "reduces workload" without a study measuring it
- Any suggestion of replacing or matching clinicians without a reader study
- Internal validation reported as if it were external
- Correlation phrased as causation — especially frequent in Chinese-to-English translation of 导致
- Missing ethics approval, consent, or data-governance statements

**Terminology:** lesion detection, organ segmentation, external validation, inter-observer variability, sensitivity/specificity, DSC, AUC, retrospective/prospective, ground truth (prefer "reference standard" in clinical venues).

## Remote sensing

**Possible review questions:** geographic generalization from one region, temporal generalization from one season, sensor transfer, spatial autocorrelation between train and test tiles, class imbalance across land-cover types.

**Watch for:** performance claims that do not name the region, sensor, resolution, and acquisition period; "applicable to remote sensing images" as an unbounded claim; missing spatial resolution or band information; train/test splits that leak through spatially adjacent tiles — a common and often unnoticed flaw.

**Terminology:** remote sensing image (统一 vs 遥感影像), change detection, spatial/spectral resolution, multi-source fusion, land cover classification, domain adaptation, ground sample distance.

## Robotics

**Possible review questions:** simulation-only results presented as deployable, missing real-time and latency measurement, safety claims without failure analysis, small numbers of physical trials, unreported hardware.

**Watch for:** sim-to-real gap unacknowledged; "real-time" without a latency figure and a requirement to compare it against; success rates with no trial count; safety claims from limited testing.

**Terminology:** perception, SLAM, motion planning, trajectory optimization, sim-to-real transfer, sensor fusion, control frequency, success rate.

## Data mining and recommendation

**Possible review questions:** offline metrics presented as business impact, causal language for associational findings, scalability claimed but not measured, popularity bias, temporal leakage in splits.

**Watch for:** "increases user engagement" from an offline evaluation; "leads to" for correlational results; scalability claims without complexity analysis or a runtime curve; random splits where a temporal split is required.

**Terminology:** pattern mining, anomaly detection, graph representation learning, cold start, implicit feedback, CTR, scalability, sparsity.

## Bioinformatics

**Possible review questions:** multiple-testing correction, batch effects, small validation cohorts, biological interpretation unsupported by experiment, cross-validation without an independent cohort.

**Watch for:** "significant" without a correction method named; biomarker claims from a single cohort; mechanistic claims from correlational omics; missing batch-effect handling; sample sizes too small for the claims made.

**Terminology:** differential expression, batch effect, FDR correction, validation cohort, pathway enrichment, multi-omics integration, single-cell.

## Materials science and chemistry

**Possible review questions:** incomplete synthesis conditions, characterization insufficient to support a structural claim, mechanisms proposed without direct evidence, no reproducibility information, performance outside tested conditions.

**Watch for:** mechanism claims from indirect characterization; performance extrapolated beyond the tested temperature, pressure, or concentration range; missing synthesis parameters that make the work unreproducible; single-sample results with no repeats.

**Terminology:** structure-property relationship, characterization, microstructure, phase composition, synthesis conditions, cyclic stability.

## Social sciences, education, management

**Possible review questions:** causal claims from observational data, construct validity, sample representativeness, common method bias, preregistration status where relevant, generalizing from one cultural context.

**Watch for:** causal interpretations such as "affects" or "leads to" without stated identification assumptions and supporting evidence; sample described without demographics or recruitment method; effect sizes omitted in favor of p-values; unacknowledged single-country or single-institution scope.

**Terminology:** construct validity, mediation/moderation, common method variance, effect size, sampling frame, self-report bias.

Note the structural difference: many venues in these fields use theoretical framing, hypotheses, and limitations sections that operate differently from IMRaD. Follow the author's structure rather than imposing a science-paper shape.


These checks do not establish scientific validity. Do not infer absent ethics approval, unperformed tests or missing analyses merely because they are not present in the supplied excerpt. Preserve theoretical assumptions and qualitative evidence on their own terms.
