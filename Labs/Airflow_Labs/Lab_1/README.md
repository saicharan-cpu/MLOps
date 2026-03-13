# Airflow lab

# Credit Card Customer Segmentation — Airflow Lab

## Overview
This lab builds a machine learning pipeline using **Apache Airflow** running inside **Docker**. The pipeline automates credit card customer segmentation using K-Means clustering, with the optimal number of clusters determined via the elbow method and validated using silhouette scoring.

---

## Project Structure
```
Lab_1/
├── dags/
│   ├── data/
│   │   ├── file.csv          # Credit card customer dataset
│   │   └── test.csv          # Test sample for cluster prediction
│   ├── model/                # Auto-created at runtime
│   │   ├── kmeans_creditcard.sav  # Saved optimal KMeans model
│   │   └── scaler.sav             # Saved MinMaxScaler
│   ├── src/
│   │   ├── __init__.py       # Makes src a Python module
│   │   └── lab.py            # Core ML logic
│   └── airflow.py            # Airflow DAG definition
├── logs/
├── plugins/
├── config/
├── .env
└── docker-compose.yaml
```

---

## Dataset
The dataset (`file.csv`) contains credit card customer behavioural data with 18 features including balance, purchases, cash advance, credit limit, payments, and payment frequency. The following 6 features are selected for clustering:

- `BALANCE` — Current account balance
- `PURCHASES` — Total purchases made
- `CREDIT_LIMIT` — Customer credit limit
- `PAYMENTS` — Total payments made
- `CASH_ADVANCE` — Cash withdrawn against credit
- `PRC_FULL_PAYMENT` — Percentage of months with full payment

---

## Pipeline (DAG)

The DAG named **`CreditCard_Customer_Segmentation`** consists of 4 sequential tasks:

```
load_data_task → data_preprocessing_task → build_save_model_task → load_model_task
```

### Task Breakdown

**1. `load_data_task`**
- Reads `file.csv` into a pandas DataFrame
- Serializes it using pickle + Base64 encoding for XCom compatibility

**2. `data_preprocessing_task`**
- Drops null rows
- Selects 6 features for clustering
- Applies `MinMaxScaler` to normalize data to [0, 1]
- Saves the scaler to `model/scaler.sav` for reuse on test data

**3. `build_save_model_task`**
- Trains KMeans models for k=2 to k=15
- Computes SSE (inertia) and silhouette score for each k
- Uses `KneeLocator` to find the optimal k via the elbow method
- Saves the optimal model (not the last-fitted) to `model/kmeans_creditcard.sav`

**4. `load_model_task`**
- Loads the saved optimal model and scaler
- Prints cluster centroids in original (unscaled) units
- Scales `test.csv` using the saved scaler before predicting
- Outputs the optimal cluster count, best silhouette score, and test sample's cluster assignment

---

## Improvements Over Original Lab

| Area | Original | This Lab |
|---|---|---|
| Features used | 3 | 6 |
| KMeans init | `random` | `k-means++` |
| k range | 1–49 | 2–15 |
| Model saved | Last loop iteration (k=49) | Optimal k only |
| Scaler on test data | Not applied ❌ | Saved and reused ✅ |
| Evaluation metric | Elbow only | Elbow + Silhouette score |
| Output | Optimal k printed | k + silhouette + centroids + test prediction |

---

## How to Run

### Prerequisites
- Docker Desktop installed and running (4GB+ RAM allocated)

### Steps

```bash
# 1. Create required folders
mkdir -p ./dags ./logs ./plugins ./config

# 2. Create .env file (Mac/Linux)
echo -e "AIRFLOW_UID=$(id -u)" > .env
# Windows: create .env manually with content: AIRFLOW_UID=50000

# 3. Initialize the database (first time only)
docker compose up airflow-init

# 4. Start Airflow
docker compose up
```

5. Open **http://localhost:8080** — login with `airflow2` / `airflow2`
6. Find `CreditCard_Customer_Segmentation` → toggle ON → click **Trigger DAG**
7. Go to **Graph** → click `load_model_task` → **Logs** to view results

### Stop Airflow
```bash
docker compose down
```

---

## Dependencies
Installed automatically inside Docker via `_PIP_ADDITIONAL_REQUIREMENTS`:
- `pandas`
- `scikit-learn`
- `kneed`

No local Python installation or virtual environment required.
