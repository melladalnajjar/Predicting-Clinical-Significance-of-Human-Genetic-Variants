<h1 align="center">🔬 Predicting Clinical Significance of Human Genetic Variants</h1>

<p align="center">
A full data engineering + machine learning pipeline using MongoDB, PySpark, and MLlib  
to classify ClinVar genetic variants as <strong>Pathogenic</strong> or <strong>Benign</strong>.
</p>

---

## 📂 Project Overview

ClinVar is NCBI’s public archive of human genetic variants and their clinical significance.  
As stated in the project document:

> “ClinVar aggregates submissions from clinical labs, research groups, and expert panels worldwide.”

This project builds an end‑to‑end workflow to ingest, clean, analyze, and model ClinVar data  
to predict whether a variant is **Pathogenic** or **Benign** based on metadata such as:

- Gene symbol  
- Variant type  
- Chromosome location  
- Review status  
- Submitter count  
- Phenotype list  
- Origin  

The final output is a trained **Random Forest classifier** with full evaluation metrics.

---

## 📊 Dataset

### **Primary Dataset — variant_summary.txt.gz**
- **URL:** https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz  
- **Format:** TSV (120 MB compressed, ~1 GB raw)  
- **Rows:** ~2.5M  
- **Key Columns:**  
  `AlleleID`, `Type`, `GeneSymbol`, `ClinicalSignificance`,  
  `ReviewStatus`, `Chromosome`, `Start`, `Stop`, `PhenotypeList`,  
  `NumberSubmitters`, `Origin`, `Assembly`

### **Secondary Dataset — submission_summary.txt.gz**
> “Per‑submission details (~4M+ rows). Join key: VariationID.”

Used for per‑variant submission counts and date‑spread features.

### **Supplementary Dataset — gene_specific_summary.txt**
Gene‑level aggregates including:
- total submissions  
- pathogenic allele counts  
- conflict counts  

---

## 🧱 Project Pipeline

The project is divided into **three major phases**, each with its own notebook deliverable.

---

# 🗄️ Phase 1 — MongoDB Ingestion & Exploration

### **Tasks**
- Download TSV files  
- Load into MongoDB using Python `csv` module (no pandas)  
- Batch inserts of 5,000–10,000 documents  
- Perform exploratory queries using PyMongo aggregation pipelines

### **Required Queries**
- Total variant count  
- Distribution of variant types (`$group` on `Type`)  
- Variants per chromosome (`$group` + `$sort`)  

---

# ⚙️ Phase 2 — PySpark ETL & SparkSQL Analysis

### **Cleaning & Transformations**
- Replace dash placeholders with nulls  
- Filter to a single genome assembly  
- Drop rows missing chromosome or coordinates  
- Normalize `ClinicalSignificance` (e.g., map *Pathogenic/Likely pathogenic*)  
- Compute `variant_length = Stop - Start + 1`  
- Map `ReviewStatus` → numeric `review_score` (0–4)  
- Create binary label `is_pathogenic`  
- Join with:
  - gene‑level summary table  
  - submission summary table  

### **SparkSQL Analytical Questions**
1. Top 10 genes with most pathogenic variants  
2. Variant type distribution (pathogenic vs benign)  
3. Conflict resolution rates by gene  
4. Diseases with highest pathogenic variant proportion  

---

# 🤖 Phase 3 — Machine Learning (MLlib)

### **Model**
- Random Forest Classifier  
- Hyperparameter tuning using:
  - `CrossValidator`
  - `ParamGridBuilder`  
  - Distributed training on Spark  

### **Evaluation Metrics**
- AUC‑ROC  
- Accuracy  
- Precision  
- Recall  
- F1 Score  
- Confusion matrix  
- Feature importance  

---

## 📅 Deliverables & Timeline

| Week | Activity | Phase | Deliverable |
|------|----------|--------|-------------|
| 8 | MongoDB ingestion + PyMongo queries | Phase 1 | Notebook (.ipynb) |
| 11 | PySpark load, ETL, SparkSQL | Phase 2 | Notebook (.ipynb) |
| 12 | Feature engineering + ML | Phase 3 | Notebook (.ipynb) |
| 12 | Evaluation + Report | Final | PDF Report |

---

## 🧰 Tech Stack

- **MongoDB + PyMongo**  
- **PySpark + SparkSQL**  
- **MLlib (Random Forest)**  
- **Python (no pandas)**  
- **Jupyter Notebooks**  

---

## 📘 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourname/clinvar-variant-classifier.git
cd clinvar-variant-classifier
