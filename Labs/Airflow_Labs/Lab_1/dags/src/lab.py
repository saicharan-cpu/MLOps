import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
import pickle
import os
import base64


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _encode(obj) -> str:
    """Pickle an object and return a Base64 ASCII string (XCom-safe)."""
    return base64.b64encode(pickle.dumps(obj)).decode("ascii")

def _decode(b64: str):
    """Decode a Base64 ASCII string back into the original object."""
    return pickle.loads(base64.b64decode(b64))


# ─── Task 1: Load Data ────────────────────────────────────────────────────────

def load_data() -> str:
    """
    Loads credit card customer data from file.csv.
    Returns Base64-encoded pickled DataFrame (XCom-safe).
    """
    path = os.path.join(os.path.dirname(__file__), "../data/file.csv")
    df = pd.read_csv(path)
    print(f"[load_data] Loaded {len(df)} rows, {len(df.columns)} columns.")
    print(df.head())
    return _encode(df)


# ─── Task 2: Preprocess Data ──────────────────────────────────────────────────

def data_preprocessing(data_b64: str) -> str:
    """
    - Drops nulls
    - Selects 6 features (vs original 3) for richer clustering
    - Scales with MinMaxScaler
    Returns Base64-encoded pickled numpy array.
    """
    df = _decode(data_b64)
    df = df.dropna()

    features = [
        "BALANCE",
        "PURCHASES",
        "CREDIT_LIMIT",
        "PAYMENTS",
        "CASH_ADVANCE",
        "PRC_FULL_PAYMENT",
    ]
    X = df[features]

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    scaler_path = os.path.join(os.path.dirname(__file__), "../model/scaler.sav")
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    print(f"[data_preprocessing] Scaler saved. Scaled shape: {X_scaled.shape}")
    return _encode(X_scaled)


# ─── Task 3: Build & Save Model ───────────────────────────────────────────────

def build_save_model(data_b64: str, filename: str) -> dict:
    """
    - Fits KMeans for k=2..15, collects SSE + silhouette scores
    - Finds optimal k via elbow method
    Returns JSON-safe dict with sse, optimal_k, silhouette_scores.
    """
    X = _decode(data_b64)

    kmeans_kwargs = {
        "init": "k-means++",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    sse = []
    sil_scores = []

    for k in range(2, 16):
        km = KMeans(n_clusters=k, **kmeans_kwargs)
        labels = km.fit_predict(X)
        sse.append(km.inertia_)
        sil_scores.append(float(silhouette_score(X, labels)))

    # Find elbow on SSE
    kl = KneeLocator(range(2, 16), sse, curve="convex", direction="decreasing")
    optimal_k = int(kl.elbow) if kl.elbow else 4
    best_model = KMeans(n_clusters=optimal_k, **kmeans_kwargs)
    best_model.fit(X)

    output_dir = os.path.join(os.path.dirname(__file__), "../model")
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, filename), "wb") as f:
        pickle.dump(best_model, f)

    print(f"[build_save_model] Optimal k={optimal_k}, model saved.")
    print(f"  SSE values:        {[round(s, 2) for s in sse]}")
    print(f"  Silhouette scores: {[round(s, 4) for s in sil_scores]}")

    return {
        "sse": sse,
        "optimal_k": optimal_k,
        "silhouette_scores": sil_scores,
    }


def load_model_elbow(filename: str, model_info: dict) -> dict:
    """
    - Loads the saved optimal model
    - Prints silhouette score + cluster centroids in original scale
      (original fed raw unscaled values into a scaled model — bug fixed)
    Returns JSON-safe dict with test cluster assignment and quality metrics.
    """
    model_dir = os.path.join(os.path.dirname(__file__), "../model")
    features = [
        "BALANCE",
        "PURCHASES",
        "CREDIT_LIMIT",
        "PAYMENTS",
        "CASH_ADVANCE",
        "PRC_FULL_PAYMENT",
    ]

    with open(os.path.join(model_dir, filename), "rb") as f:
        model = pickle.load(f)

    with open(os.path.join(model_dir, "scaler.sav"), "rb") as f:
        scaler = pickle.load(f)

    optimal_k  = model_info["optimal_k"]
    sil_scores = model_info["silhouette_scores"]
    best_sil   = max(sil_scores)

    print(f"\n{'='*55}")
    print(f"  OPTIMAL NUMBER OF CLUSTERS : {optimal_k}")
    print(f"  BEST SILHOUETTE SCORE      : {best_sil:.4f}  (k={sil_scores.index(best_sil) + 2})")
    print(f"{'='*55}\n")

    centroids_original = scaler.inverse_transform(model.cluster_centers_)
    centroid_df = pd.DataFrame(centroids_original, columns=features)
    centroid_df.index.name = "CLUSTER"
    print("[Cluster Centroids — Original Scale]")
    print(centroid_df.round(2).to_string())
    print()

    test_path = os.path.join(os.path.dirname(__file__), "../data/test.csv")
    test_df = pd.read_csv(test_path)
    test_scaled = scaler.transform(test_df[features])
    pred = int(model.predict(test_scaled)[0])

    print(f"[Test Sample]")
    print(test_df[features].iloc[[0]].to_string(index=False))
    print(f"  → Assigned to Cluster: {pred}\n")

    result = {
        "optimal_k": optimal_k,
        "test_cluster": pred,
        "best_silhouette": round(best_sil, 4),
    }
    print(f"[Final Result] {result}")
    return result