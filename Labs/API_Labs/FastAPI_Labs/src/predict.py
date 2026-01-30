import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "wine_model.pkl")

def predict_data(X):
    """
    Predict the class labels for the input Wine features.
    Args:
        X (list or np.ndarray): Input data (4 features) for which predictions are to be made.
    Returns:
        y_pred (numpy.ndarray): Predicted class labels (0, 1, 2)
    """
    model = joblib.load(MODEL_PATH)
    X = np.array(X)  # Ensure input is a NumPy array
    y_pred = model.predict(X)
    return y_pred
