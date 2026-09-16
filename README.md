# 🧪 QC & Batch Release Analytics – Vaccine/Biologics Assay Data

<p align="center">
  <img src="https://img.shields.io/badge/Python-Data%20Analysis-blue?logo=python" />
  <img src="https://img.shields.io/badge/SQL-Data%20Analysis-orange?logo=postgresql" />
  <img src="https://img.shields.io/badge/Pharmaceutical-QC-green" />
  <img src="https://img.shields.io/badge/Statistics-Analysis-purple" />
</p>

<p align="center">
  <b>Pharmaceutical QC Data Analysis using Python, SQL & Statistical Analysis</b>
</p>
A synthetic dataset of **50 vaccine/biologics batches** was created to simulate a batch-level analytical QC workflow. The dataset contains results for four assays:

- **HCP** – Host Cell Protein (ng/mL)
- **HCD** – Host Cell DNA (ng/mL)
- **BCA** – Protein concentration (µg/mL)
- **D-Antigen** – D-Ag (DU/mL)

The analysis focuses on data cleaning, validation, specification checks, OOS identification, statistical analysis, outlier detection, and batch-level classification.

> **Note:** The dataset is synthetic and created for educational and portfolio purposes. It does not contain confidential or proprietary pharmaceutical data.

---
## 🔬 Project Overview

This project demonstrates a **pharmaceutical quality control (QC) analytics workflow** using a synthetic vaccine/biologics batch dataset.

The analysis focuses on multiple analytical assays used to evaluate batch quality and demonstrates how laboratory assay results can be transformed into structured QC insights using **Python, SQL, statistical analysis, and data visualization**.

The project covers:

> **Data Cleaning → Validation → Specification Checks → OOS Identification → Batch Classification → Statistical Analysis → Outlier Detection → Visualization**

---

## 🎯 Objectives

- Analyze assay results across pharmaceutical batches
- Validate and clean QC assay data
- Apply specification limits to identify **Out-of-Specification (OOS)** results
- Determine overall batch status based on assay-level results
- Calculate descriptive statistics
- Analyze variability using **Standard Deviation and CV%**
- Identify potential statistical outliers
- Examine assay distributions and skewness
- Generate visualizations to support QC data interpretation

---

## 🧬 Dataset

The dataset contains **50 synthetic vaccine/biologics batches** and four analytical assays.

| Assay | Description | Unit |
|---|---|---|
| **HCP** | Host Cell Protein | ng/mL |
| **HCD** | Host Cell DNA | ng/mL |
| **BCA** | Protein Concentration | µg/mL |
| **D-Antigen** | D-Antigen Assay | DU/mL |

### Dataset Structure

Each row represents **one batch**, while each assay column represents an analytical measurement.

```text
Batch_ID
│
├── HCP
├── HCD
├── BCA
├── D-Antigen
│
├── HCP_Status
├── HCD_Status
├── BCA_Status
├── D_Ag_Status
│
└── Overall_Status
---

## 🔄 Analytical Workflow

```text
🧪 Synthetic QC Dataset
          │
          ▼
🧹 Data Cleaning & Validation
          │
          ▼
📏 Specification Checks
          │
          ▼
⚠️ OOS Identification
          │
          ▼
📦 Batch-Level Classification
          │
          ▼
📊 Descriptive Statistics
          │
          ▼
🚨 Outlier Detection
          │
          ▼
📈 Distribution Analysis
          │
          ▼
💡 QC Data Interpretation

🛠️ Tools & Technologies
<p align="center"> <img src="https://img.shields.io/badge/Python-Pandas%20%7C%20NumPy%20%7C%20Matplotlib-blue?logo=python" /> <img src="https://img.shields.io/badge/SQL-Data%20Querying-orange?logo=postgresql" /> <img src="https://img.shields.io/badge/Excel-Data%20Handling-green?logo=microsoftexcel" /> </p>
