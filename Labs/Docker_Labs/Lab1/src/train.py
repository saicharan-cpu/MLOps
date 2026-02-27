import os
import joblib
import numpy as np
import pandas as pd

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "wine_model.pkl")


def load_data():
    """
    Load dataset (using Wine dataset instead of Iris to make it different)
    """
    data = load_wine()

    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target)

    print(f"Dataset loaded with shape: {X.shape}")

    return X, y


def train_model(X_train, y_train):
    """
    Train Random Forest model
    """
    print("Training model...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("Training complete")

    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    """
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"Model Accuracy: {accuracy:.4f}")

    return accuracy


def save_model(model):
    """
    Save trained model
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"Model saved at {MODEL_PATH}")


def run_training_pipeline():
    """
    Complete ML pipeline
    """

    # Load data
    X, y = load_data()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

    # Save model
    save_model(model)