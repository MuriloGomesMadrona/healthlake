# 🏥 HealthLake — Predição de Readmissão Hospitalar

Pipeline de dados completo no Databricks Lakehouse para predição de readmissão hospitalar em 30 dias, usando dados públicos do dataset *Diabetes 130-US Hospitals*.

---

## Sobre o projeto

Este projeto simula um caso real de engenharia de dados em healthtech: dados brutos de internações hospitalares são ingeridos, limpos, validados e transformados em features para um modelo preditivo de machine learning.

**Problema:** dado o histórico de um paciente internado por diabetes, qual a probabilidade de ele ser readmitido em menos de 30 dias após a alta?

**Por que isso importa:** readmissões precoces custam bilhões ao sistema de saúde e indicam falhas no tratamento. Prever esse risco permite intervenções preventivas.

---

## Arquitetura

```
Fonte (CSV)
    │
    ▼
[Bronze] — dado bruto, imutável, salvo em Delta Lake
    │
    ▼
[Silver] — limpeza, tipagem, validação de qualidade
    │
    ▼
[Gold]   — feature engineering, tabela pronta para ML
    │
    ▼
[ML]     — treinamento XGBoost + tracking com MLflow
```

> Em produção, esta arquitetura usaria Auto Loader (ingestão incremental), Delta Live Tables (pipelines declarativos) e Unity Catalog (governança e lineage). Essas features foram omitidas por limitação do Databricks Community Edition.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Plataforma | Databricks Community Edition |
| Armazenamento | Delta Lake |
| Transformações | PySpark |
| Qualidade de dados | Great Expectations |
| Machine Learning | XGBoost + scikit-learn |
| Tracking de experimentos | MLflow |
| Testes | pytest |
| Linting | ruff |
| CI/CD | GitHub Actions |
| Gerenciamento de deps | Poetry |

---

## Dataset

**Diabetes 130-US Hospitals (1999–2008)**
- Fonte: [Kaggle](https://www.kaggle.com/datasets/jimschacko/diabetic-patients-readmission-prediction)
- ~100.000 registros de internações hospitalares
- Features: diagnósticos (CID), medicamentos, tempo de internação, número de procedimentos, etc.
- Target: `readmitted` — se o paciente voltou em `<30` dias, `>30` dias, ou `NO`

---

## Estrutura do repositório

```
healthlake/
├── data/
│   └── raw/                        # CSV original (não versionado)
├── notebooks/
│   ├── 01_bronze.py                # Ingestão do CSV → Delta
│   ├── 02_silver.py                # Limpeza e validação
│   ├── 03_gold.py                  # Feature engineering
│   └── 04_ml.py                    # Treinamento e MLflow
├── src/
│   ├── __init__.py
│   └── transformations/
│       ├── __init__.py
│       └── cleaning.py             # Funções PySpark reutilizáveis e testáveis
├── tests/
│   └── test_cleaning.py            # Testes unitários com pytest
├── .github/
│   └── workflows/
│       └── ci.yml                  # Lint + testes automáticos no push
├── .gitignore
├── pyproject.toml                  # Dependências via Poetry
└── README.md
```

---

## Como executar localmente (testes e linting)

### Pré-requisitos

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)

### Instalação

```bash
git clone https://github.com/seu-usuario/healthlake.git
cd healthlake
poetry install
```

### Rodar os testes

```bash
poetry run pytest tests/ -v
```

### Rodar o linter

```bash
poetry run ruff check src/ tests/
```

---

## Como executar no Databricks

### 1. Faça upload do dataset

No Databricks Community Edition:
1. Acesse **Data → Add Data → Upload File**
2. Faça upload do arquivo `diabetic_data.csv`
3. O arquivo ficará disponível em `/FileStore/tables/diabetic_data.csv`

### 2. Importe os notebooks

1. No menu lateral, clique em **Workspace**
2. Clique em **Import**
3. Importe cada arquivo `.py` da pasta `notebooks/` na ordem numérica

### 3. Anexe um cluster

1. Crie um cluster em **Compute → Create Cluster** (configurações padrão)
2. Abra cada notebook e selecione o cluster criado no topo da página

### 4. Execute na ordem

```
01_bronze.py → 02_silver.py → 03_gold.py → 04_ml.py
```

Cada notebook gera uma tabela Delta que o próximo consome. Não pule etapas.

---

## Resultados do modelo

| Métrica | Valor |
|---|---|
| AUC-ROC | *preencher após treinar* |
| F1-Score (classe <30d) | *preencher após treinar* |
| Acurácia | *preencher após treinar* |

Os experimentos ficam registrados no MLflow, acessível em **Experiments** no menu do Databricks.

---

## Decisões técnicas

**Por que PySpark e não pandas?**
Pandas carrega tudo na memória de uma máquina. PySpark distribui o processamento — padrão em ambientes de dados reais com volumes grandes. Mesmo em datasets pequenos, usar PySpark demonstra que o código escala.

**Por que separar `src/` dos notebooks?**
Notebooks são ótimos para exploração, mas péssimos para reuso e testes. Funções reutilizáveis vivem em `src/`, são importadas nos notebooks e testadas com pytest — assim como código de software convencional.

**Por que Delta Lake e não Parquet puro?**
Delta adiciona transações ACID, versionamento e schema enforcement sobre Parquet. É o padrão de fato em Databricks e a base do conceito de Lakehouse.

---

## Autor

Feito por [seu nome] como projeto de portfólio em engenharia de dados.
