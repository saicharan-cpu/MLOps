# ELK Stack - ML Training Log Monitor (Wine Dataset)

This lab demonstrates how to monitor machine learning model training using the **ELK Stack** (Elasticsearch, Logstash, Kibana). A Logistic Regression model is trained on the Wine dataset, and all training metrics are captured as structured logs and shipped to Elasticsearch for visualization in Kibana. Make sure you have the ELK stack downloaded as per the instructions given prior.

---

## What I Modified

Compared to the original Iris-based script, I made the following changes:

- **Switched dataset** from Iris to the **Wine dataset** — 178 samples, 13 chemical features, 3 wine cultivar classes
- **Added `StandardScaler`** for feature normalization — Logistic Regression is sensitive to feature scale, and Wine features vary wildly in magnitude (e.g. alcohol % vs. proline levels in the hundreds)
- **Increased `max_iter` to 500** — Wine's higher-dimensional feature space needs more iterations to converge
- **Logged feature names** alongside dataset info for better traceability
- **Added `dataset` key to JSON summary** to distinguish runs across different datasets
- **Logged coefficient shape** instead of raw values — 3 classes × 13 features produces a large matrix that clutters logs

---

## Project Structure

```
Lab2_ELK_Setup_Mac/
├── train.py              # ML training script
├── training.log          # Generated log file (after running train.py)
├── logstash.conf         # Logstash pipeline configuration
└── README.md
```

---

## Prerequisites

- Elasticsearch 9.x running on `https://localhost:9200`
- Kibana running on `http://localhost:5601`
- Logstash 9.x installed
- Python 3.x with the following packages:

```bash
pip install scikit-learn numpy
```

---

## How to Run

### Step 1 — Generate the training log

```bash
cd /Users/<your-username>/Documents/MLOPS/MLOps/Labs/ELK_Labs/Lab2_ELK_Setup_Mac
python3 train.py
```

This creates `training.log` in the same directory.

### Step 2 — Start Elasticsearch

```bash
cd ~/Downloads/elasticsearch-9.3.2/bin
./elasticsearch
```

### Step 3 — Start Logstash

```bash
cd ~/Downloads/logstash-9.3.2/bin
./logstash -f /path/to/Lab2_ELK_Setup_Mac/logstash.conf
```

### Step 4 — Verify data in Elasticsearch

```bash
curl -k -u elastic:<your-password> https://localhost:9200/logstash-training/_count
```

### Step 5 — View in Kibana

1. Open `http://localhost:5601`
2. Go to **Stack Management → Data Views**
3. Create a data view with index pattern `logstash-training*` and timestamp `@timestamp`
4. Go to **Discover** and select the `logstash-training` data view
5. Set the time filter to **Today**

---

## Dataset — Wine

| Property | Value |
|---|---|
| Samples | 178 |
| Features | 13 (alcohol, malic acid, ash, etc.) |
| Classes | 3 (class_0, class_1, class_2) |
| Task | Multiclass classification |

---

## Metrics Logged

| Metric | Description |
|---|---|
| Accuracy | Overall test set accuracy |
| F1 Score | Weighted F1 across all classes |
| Precision | Weighted precision across all classes |
| Recall | Weighted recall across all classes |
| CV Accuracy | 5-fold cross-validation mean ± std |
| TP / TN / FP / FN | Per-class confusion matrix values |
| FPR / FNR | Per-class false positive/negative rates |
| Coefficients shape | Shape of learned weight matrix |
| Intercept | Learned model bias terms |

---

## Troubleshooting

**Logistic Regression convergence warning**
The script uses `max_iter=500` which should be sufficient. If you still see warnings, increase it further or try `solver='saga'`.

**Logstash crashes with `StringIndexOutOfBoundsException`**
Rename the logstash folder:
```bash
mv ~/Downloads/logstash-9.3.2 ~/logstash
```

**Kibana shows no data in Discover**
Set the time filter to "Today" or "Last 15 minutes".

**Elasticsearch connection refused**
Use `https://` not `http://` and include credentials in the Logstash output config.
