import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "wine_model.pkl")

def load_model():
    """Load the Wine model from disk"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict_data(X):
    """Predict Wine class for input X"""
    model = load_model()
    X = np.array(X)
    y_pred = model.predict(X)
    return y_pred
