# Field Adapter

Adapt writing emphasis, terminology, and caution level to the research field. Never introduce field-specific claims that are not supported by the user's text.

## General Strategy

1. Prefer explicit user field statements.
2. If absent, infer from technical terms.
3. If uncertain, use general academic style and state: "Field assumed from terminology: ...".
4. Keep claims evidence-bounded, especially for clinical, deployment, and benchmark statements.

## Computer Vision

- Common tasks: image classification, object detection, semantic segmentation, instance segmentation, tracking, image generation, 3D reconstruction, multimodal perception.
- Writing focus: model architecture, feature representation, spatial context, robustness, generalization, computational cost, ablation study, benchmark protocol.
- Common terms: feature extraction, feature fusion, object detection, semantic segmentation, instance segmentation, attention mechanism, robustness, generalization ability, ablation study.
- Avoid: claiming universal robustness, overstating SOTA, mixing "目标检测/对象检测", or adding benchmark names and numbers not provided.

## Artificial Intelligence

- Common tasks: reasoning, planning, representation learning, multimodal intelligence, decision making, agent systems.
- Writing focus: problem formulation, learning or reasoning mechanism, evaluation setting, uncertainty, safety, human alignment when relevant.
- Common terms: representation learning, reasoning, planning, knowledge representation, multimodal learning, alignment, inference.
- Avoid: broad claims such as "human-level intelligence", unsupported safety claims, or vague "intelligent optimization" wording.

## Machine Learning

- Common tasks: supervised learning, self-supervised learning, transfer learning, domain adaptation, optimization, uncertainty estimation.
- Writing focus: objective function, assumptions, generalization, optimization stability, model complexity, empirical validation, theoretical motivation if available.
- Common terms: optimization objective, loss function, generalization, regularization, convergence, representation, overfitting, distribution shift.
- Avoid: claiming proof without derivation, confusing correlation with causation, or using "significant" when no statistical test is given.

## Medical Imaging

- Common tasks: lesion detection, organ segmentation, disease classification, registration, reconstruction, report generation, survival or risk prediction.
- Writing focus: clinical relevance, data heterogeneity, annotation cost, interpretability, external validation, privacy, ethics, scanner or protocol variation.
- Common terms: lesion detection, organ segmentation, medical image segmentation, clinical relevance, external validation, annotation burden, interpretability.
- Avoid: diagnostic claims without clinical validation, "can replace clinicians", invented cohorts, invented ethics approval, or overstated clinical deployment.

## Remote Sensing

- Common tasks: land-cover classification, object detection, change detection, semantic segmentation, hyperspectral analysis, multi-source fusion.
- Writing focus: scale variation, spatial resolution, spectral information, complex background, domain shift, geographic generalization, sensor differences.
- Common terms: remote sensing image, change detection, spatial resolution, spectral feature, multi-source data fusion, domain adaptation, geographic generalization.
- Avoid: ignoring spatial scale, mixing "遥感图像/遥感影像" inconsistently, or claiming geographic transfer without evidence.

## Natural Language Processing

- Common tasks: text classification, information extraction, machine translation, summarization, question answering, dialogue, retrieval-augmented generation.
- Writing focus: semantic representation, context modeling, pre-trained language models, transfer learning, data bias, evaluation protocol, hallucination risk.
- Common terms: contextual representation, pre-trained language model, tokenization, fine-tuning, prompting, retrieval, hallucination, domain adaptation.
- Avoid: overstating semantic understanding, ignoring data leakage, or using "prove" for empirical benchmark results.

## Robotics

- Common tasks: perception, localization, mapping, planning, control, manipulation, navigation, human-robot interaction.
- Writing focus: real-time performance, sensor fusion, physical constraints, safety, deployment robustness, simulation-to-real transfer, failure cases.
- Common terms: perception, planning, control, SLAM, sensor fusion, trajectory optimization, real-time performance, sim-to-real transfer.
- Avoid: claiming real-world reliability from simulation only, omitting latency constraints, or overstating safety without validation.

## Data Mining

- Common tasks: pattern discovery, clustering, anomaly detection, recommendation, graph mining, large-scale data analysis.
- Writing focus: data distribution, noise robustness, scalability, interpretability, evaluation metrics, computational efficiency.
- Common terms: pattern mining, anomaly detection, graph mining, scalability, data sparsity, noise robustness, recommendation.
- Avoid: causal language for association mining, unverifiable business-impact claims, or unsupported scalability statements.

## Bioinformatics

- Common tasks: gene expression analysis, sequence analysis, protein structure prediction, biomarker discovery, single-cell analysis, multi-omics integration.
- Writing focus: sample heterogeneity, statistical significance, biological interpretation, reproducibility, validation cohort, batch effects.
- Common terms: gene expression, biomarker, multi-omics, pathway analysis, batch effect, statistical significance, validation cohort.
- Avoid: claiming biological mechanism without validation, inventing cohorts, or omitting uncertainty from small-sample results.

## Materials Science

- Common tasks: structure-property prediction, materials discovery, characterization analysis, synthesis optimization, microstructure modeling.
- Writing focus: experimental conditions, characterization methods, structure-property relationship, reproducibility, mechanism explanation, uncertainty.
- Common terms: structure-property relationship, characterization, microstructure, synthesis condition, phase composition, mechanical property, reproducibility.
- Avoid: unsupported mechanism claims, missing experimental conditions, or claiming general material performance beyond tested conditions.

