# Predicting-Clinical-Significance-of-Human-Genetic-Variants
ClinVar is NCBI’s public archive of human genetic variants and their clinical significance. It aggregates submissions from clinical labs, research groups, and expert panels worldwide.
Predicting Clinical Significance
of Human Genetic Variants
1. Dataset
ClinVar is NCBI’s public archive of human genetic variants and their clinical significance. It
aggregates submissions from clinical labs, research groups, and expert panels worldwide.
Primary: variant_summary.txt.gz
URL https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.
gz
Format / Size TSV, gzipped (~120 MB compressed, ~1 GB raw)
Records ~2.5 M+ rows
Key Columns AlleleID, Type, GeneSymbol, ClinicalSignificance, ReviewStatus,
Chromosome, Start, Stop, PhenotypeList, NumberSubmitters, Origin,
Assembly
Secondary: submission_summary.txt.gz
Per-submission details (~4 M+ rows). Join key: VariationID. Enables per-variant submission counts
and date-spread calculations.
Supplementary: gene_specific_summary.txt
Gene-level aggregates: total submissions, pathogenic allele counts, conflict counts. Small lookup
table for enriching variants during SparkSQL joins.
All files: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/
2. Project Question
Given a genetic variant’s metadata (gene, variant type, chromosome, review status, submitter
count, origin, phenotype), can we predict whether it is Pathogenic or Benign?
This mirrors real clinical bioinformatics: labs routinely discover unclassified variants (VUS) and need
scalable automated triage. Students build a full pipeline from raw ingestion through ML prediction.
3. Pipeline Phases
No pandas is used anywhere in this project.
Phase 1 — MongoDB Ingestion & Exploration
Load raw data into MongoDB and perform document-oriented exploratory analysis.
Ingestion
You need to download the TSV and load it into MongoDB using Python’s csv module (no pandas).
Batch inserts of ~5,000–10,000 documents at a time for performance:
Exploratory Queries (PyMongo)
You need to perform at the following queries using PyMongo aggregation pipelines:
• Total variant count
• Distribution of variant types ($group on Type)
• Variants per chromosome ($group on Chromosome, $sort)
Phase 2 — Load into PySpark, ETL & Analysis (PySpark + SparkSQL)
Read data from MongoDB into Spark, clean and preprocess it, join with gene info data, and perform
advanced ETL transformations
Cleaning & Transformations
• Replace dash placeholders with nulls and cast data types
• Filter to a single genome assembly to remove duplicates
• Drop rows where Chromosome, Start, or Stop are null
• Clean ClinicalSignificance: strip whitespace; map compound labels like 'Pathogenic/Likely
pathogenic' to simplified categories using regexp_replace or when/otherwise
• Compute variant length as a derived feature: variant_length = Stop - Start + 1
• Map ReviewStatus to numeric review_score (0–4 scale)
• Create is_pathogenic: 1 for 'Pathogenic', 0 for 'Benign'; drop VUS and ambiguous rows for
ML
• Join with genes table on GeneSymbol for gene-level pathogenic/conflict counts
• Join with submissions on VariationID for per-variant submission stats
SparkSQL Analytical Questions
1. Top 10 genes with the most pathogenic variants
2. Variant type distribution: pathogenic vs. benign
3. Conflict resolution rates by gene (JOIN genes; filter conflicts > 0; compute pathogenic
ratio)
4. Diseases with highest pathogenic variant proportion
Phase 3 — Machine Learning (MLlib)
Use Random Forest Classifier to build a classification model to predict whether a variant is
Pathogenic or Benign based on its features.
● Include a CrossValidator with a ParamGridBuilder to perform distributed hyperparameter
tuning (e.g., tuning the maxDepth or numTrees of the Random Forest).
Model Evaluation
• AUC-ROC (BinaryClassificationEvaluator)
• Accuracy, Precision, Recall, F1 (MulticlassClassificationEvaluator)
• Confusion matrix (groupBy predicted vs. actual)
• Feature importance from the trained Random Forest model
4. Deliverables & Timeline
Week Activity Phase Deliverable
8 Download, MongoDB load,
PyMongo queries
Phase 1: MongoDB Notebook (.ipynb)
11 Load into PySpark, verify
schemas, Cleaning, ETL,
SparkSQL queries
Phase 2: Spark Load
and ETL
Notebook (.ipynb)
12 Feature eng., ML pipeline,
training
Phase 3: ML Notebook (.ipynb)
12 Evaluation, report writing Final Report (PDF)
