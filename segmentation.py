from sklearn.metrics import silhouette_score
from skfuzzy.cluster import cmeans
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

# HITUNG LRFM
def calculate_lrfm(df):

    # Pastikan order_date datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    snapshot_date = df["order_date"].max()

    lrfm = df.groupby("username").agg({
        "order_date": [
            lambda x: (snapshot_date - x.max()).days,  # Recency
            lambda x: (x.max() - x.min()).days         # Length
        ],
        "order_id": "count",
        "total_amount": "sum"
    })

    lrfm.columns = ["Recency", "Length", "Frequency", "Monetary"]
    lrfm = lrfm.reset_index()

    return lrfm

# FCM CLUSTERING
def run_fcm(
    lrfm,
    n_clusters=4,
    n_runs=10
):

    features = [
        "Recency",
        "Length",
        "Frequency",
        "Monetary"
    ]

    scaler = MinMaxScaler()

    scaled_data = scaler.fit_transform(
        lrfm[features]
    )

    best_result = None

    best_score = -1

    # ==================================
    # MULTIPLE RUNS
    # ==================================

    for _ in range(n_runs):

        cntr, u, _, _, _, _, _ = cmeans(
            scaled_data.T,
            c=n_clusters,
            m=2,
            error=0.005,
            maxiter=1000
        )

        labels = np.argmax(u, axis=0)

        silhouette = silhouette_score(
            scaled_data,
            labels
        )

        if silhouette > best_score:

            best_score = silhouette

            best_labels = labels

    # ==================================
    # FINAL RESULT
    # ==================================

    result = lrfm.copy()

    result["Cluster"] = best_labels

    return result, best_score

def find_best_cluster(
    lrfm,
    min_k=2,
    max_k=8,
    n_runs=10
):

    features = lrfm[[
        "Length",
        "Recency",
        "Frequency",
        "Monetary"
    ]]

    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(features)

    best_score = -1

    best_k = 2

    scores = []

    for k in range(min_k, max_k + 1):

        run_scores = []

        # ==================================
        # MULTIPLE RUNS
        # ==================================

        for _ in range(n_runs):

            cntr, u, _, _, _, _, _ = cmeans(
                scaled.T,
                c=k,
                m=2,
                error=0.005,
                maxiter=1000
            )

            labels = np.argmax(u, axis=0)

            score = silhouette_score(
                scaled,
                labels
            )

            run_scores.append(score)

        # ==================================
        # AVERAGE SILHOUETTE
        # ==================================

        avg_score = np.mean(run_scores)

        scores.append({
            "Cluster": k,
            "Average Score": avg_score
        })

        # ==================================
        # BEST CLUSTER
        # ==================================

        if avg_score > best_score:

            best_score = avg_score

            best_k = k

    score_df = pd.DataFrame(scores)

    return best_k, best_score, score_df