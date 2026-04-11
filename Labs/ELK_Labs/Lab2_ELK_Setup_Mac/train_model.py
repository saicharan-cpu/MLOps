import logging
import json
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, confusion_matrix, precision_score, recall_score
import numpy as np

# Configure the logging module
logging.basicConfig(
    filename='training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load the Wine dataset
data = load_wine()
X, y = data.data, data.target
class_names = list(data.target_names)

logging.info(f"Dataset loaded: Wine Dataset — {len(X)} total samples, {len(class_names)} classes: {class_names}")
logging.info(f"Number of features: {X.shape[1]} — {list(data.feature_names)}")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

logging.info(f"Number of training samples: {len(X_train)}")
logging.info(f"Number of testing samples: {len(X_test)}")

# Scale features — important for Logistic Regression on Wine dataset
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
logging.info("Feature scaling applied: StandardScaler")

# Initialize the Logistic Regression model
model = LogisticRegression(max_iter=500, solver='lbfgs', multi_class='auto')

# Training
logging.info("Starting model training...")
model.fit(X_train, y_train)
logging.info("Model training completed.")

# Cross-validation score
cv_scores = cross_val_score(model, X_train, y_train, cv=5)
logging.info(f"Cross-validation accuracy (5-fold): mean={cv_scores.mean():.4f}, std={cv_scores.std():.4f}")

# Evaluate the model
predictions = model.predict(X_test)
score = model.score(X_test, y_test)
logging.info(f"Model accuracy on test data: {score:.4f}")

# Metrics
f1 = f1_score(y_test, predictions, average='weighted')
precision = precision_score(y_test, predictions, average='weighted')
recall = recall_score(y_test, predictions, average='weighted')
conf_matrix = confusion_matrix(y_test, predictions)

logging.info(f"F1 Score: {f1:.4f}")
logging.info(f"Precision (weighted): {precision:.4f}")
logging.info(f"Recall (weighted): {recall:.4f}")

# Per-class confusion matrix breakdown
tp = np.diag(conf_matrix)
tn = np.sum(conf_matrix) - (np.sum(conf_matrix, axis=0) + np.sum(conf_matrix, axis=1) - tp)
fp = np.sum(conf_matrix, axis=0) - tp
fn = np.sum(conf_matrix, axis=1) - tp

fp_rate = fp / (fp + tn)
fn_rate = fn / (fn + tp)

logging.info(f"True Positive (per class): {tp}")
logging.info(f"True Negative (per class): {tn}")
logging.info(f"False Positive (per class): {fp}")
logging.info(f"False Negative (per class): {fn}")
logging.info(f"False Positive Rate (per class): {np.round(fp_rate, 4)}")
logging.info(f"False Negative Rate (per class): {np.round(fn_rate, 4)}")

# Log model parameters
logging.info(f"Model coefficients shape: {model.coef_.shape}")
logging.info(f"Model intercept: {np.round(model.intercept_, 4)}")

# Summary log as JSON for easy parsing
summary = {
    "dataset": "wine",
    "accuracy": round(score, 4),
    "f1_score": round(f1, 4),
    "precision": round(precision, 4),
    "recall": round(recall, 4),
    "cv_mean_accuracy": round(cv_scores.mean(), 4),
    "cv_std": round(cv_scores.std(), 4)
}
logging.info(f"Training summary: {json.dumps(summary)}")
logging.info("=" * 60)