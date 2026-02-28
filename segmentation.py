from fcmeans import FCM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
import numpy as np
import pandas as pd


# ==============================
# HITUNG LRFM
# ==============================
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

    lrfm.columns = ["Length", "Recency", "Frequency", "Monetary"]
    lrfm = lrfm.reset_index()

    return lrfm


# ==============================
# FCM CLUSTERING
# ==============================
def run_fcm(lrfm, n_clusters=4):

    features = ["Recency", "Length", "Frequency", "Monetary"]
    
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(lrfm[features])

    fcm = FCM(n_clusters=n_clusters, random_state=42)
    fcm.fit(scaled_data)

    membership = fcm.u

    # Hard label untuk evaluasi
    labels = np.argmax(membership, axis=1)

    silhouette = silhouette_score(scaled_data, labels)

    lrfm["Cluster"] = labels

    return lrfm, silhouette