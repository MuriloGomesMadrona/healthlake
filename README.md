# 🏥 HealthLake — Hospital Readmission Prediction

Full data pipeline on Databricks Lakehouse for predicting hospital readmission within 30 days, using public data from the *Diabetes 130-US Hospitals* dataset.

---

## About

This project simulates a real-world data engineering scenario in healthtech: raw hospital admission records are ingested, cleaned, validated, and transformed into features for a predictive machine learning model.

**Problem:** given the medical history of a diabetic patient, what is the probability of readmission within 30 days of discharge?

**Why it matters:** early readmissions cost billions to healthcare systems and indicate failures in treatment. Predicting this risk enables preventive interventions.

---

## Architecture

```
Source (CSV)
    │
    ▼
[Bronze] — raw data, immutable, saved as Delta Lake
    │
    ▼
[Silver] — cleaning, typing, data quality validation
    │
    ▼
[Gold]   — feature engineering, ML-ready table
    │
    ▼
[ML]     — XGBoost training + MLflow tracking
```

> In production, this architecture would use Auto Loader (incremental ingestion), Delta Live Tables (declarative pipelines), and Unity Catalog (governance and lineage). These features were omitted due to Databricks Community Edition limitations.

---

## Stack

| Layer | Technology |
|---|---|
| Platform | Databricks Community Edition |
| Storage | Delta Lake |
| Transformations | PySpark |
| Data Quality | Manual assertions with PySpark |
| Machine Learning | XGBoost + scikit-learn |
| Experiment Tracking | MLflow |
| Testing | pytest |
| Linting | ruff |
| CI/CD | GitHub Actions |
| Dependency Management | Poetry |

---

## Dataset

**Diabetes 130-US Hospitals (1999–2008)**
- Source: [Kaggle](https://www.kaggle.com/datasets/saurabhtayal/diabetic-patients-readmission-prediction)
- ~100,000 hospital admission records
- Features: diagnoses (ICD codes), medications, time in hospital, number of procedures, etc.
- Target: `readmitted` — whether the patient returned in `<30` days, `>30` days, or `NO`

---

## Repository Structure

```
healthlake/
├── data/
│   └── raw/                        # Original CSV (not versioned)
├── notebooks/
│   ├── 01_bronze.py                # CSV ingestion → Delta
│   ├── 02_silver.py                # Cleaning and validation
│   ├── 03_gold.py                  # Feature engineering
│   └── 04_ml.py                    # Training and MLflow
├── src/
│   ├── __init__.py
│   └── transformations/
│       ├── __init__.py
│       └── cleaning.py             # Reusable and testable PySpark functions
├── tests/
│   └── test_cleaning.py            # Unit tests with pytest
├── .github/
│   └── workflows/
│       └── ci.yml                  # Lint + tests on every push
├── .gitignore
├── pyproject.toml                  # Dependencies via Poetry
└── README.md
```

---

## How to Run Locally (tests and linting)

### Prerequisites

- Python 3.13+
- Java 17+
- [Poetry](https://python-poetry.org/docs/#installation)

### Setup

```bash
git clone https://github.com/MuriloGomesMadrona/healthlake.git
cd healthlake
poetry install
```

### Run tests

```bash
poetry run pytest tests/ -v
```

### Run linter

```bash
poetry run ruff check src/ tests/
```

---

## How to Run on Databricks

### 1. Upload the dataset

1. Go to **Catalog → Create Volume** named `healthlake`
2. Upload `diabetic_data.csv` and `IDs_mapping.csv` to the volume
3. Files will be available at `/Volumes/workspace/default/healthlake/`

### 2. Import the notebooks

1. In the sidebar, click **Workspace**
2. Click **Import**
3. Import each `.py` file from the `notebooks/` folder in numerical order

### 3. Run in order

```
01_bronze.py → 02_silver.py → 03_gold.py → 04_ml.py
```

Each notebook generates a Delta table consumed by the next. Do not skip steps.

---

## Model Results

| Metric | Value |
|---|---|
| AUC-ROC | 0.6340 |
| F1-Score (class <30d) | 0.2520 |
| Accuracy | 0.65 |
| Recall (class <30d) | 0.52 |

Experiments are tracked in MLflow, accessible under **Experiments** in the Databricks sidebar.

---

## Technical Decisions

**Why PySpark instead of pandas?**
Pandas loads everything into a single machine's memory. PySpark distributes processing — the standard in real data environments with large volumes. Even on small datasets, using PySpark demonstrates that the code scales.

**Why separate `src/` from notebooks?**
Notebooks are great for exploration but poor for reuse and testing. Reusable functions live in `src/`, are imported into notebooks, and tested with pytest — just like conventional software code.

**Why Delta Lake instead of plain Parquet?**
Delta adds ACID transactions, versioning, and schema enforcement on top of Parquet. It is the de facto standard in Databricks and the foundation of the Lakehouse concept.

---

## Author

Built by Murilo Gomes Madrona as a data engineering portfolio project.
