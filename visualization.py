import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA


# ==============================
# VISUALISASI PCA CLUSTER
# ==============================
def plot_clusters(lrfm):

    features = ["Recency", "Length", "Frequency", "Monetary"]

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(lrfm[features])

    pca = PCA(n_components=2)
    components = pca.fit_transform(scaled)

    lrfm["PCA1"] = components[:, 0]
    lrfm["PCA2"] = components[:, 1]

    plt.figure(figsize=(8,6))
    sns.scatterplot(
        data=lrfm,
        x="PCA1",
        y="PCA2",
        hue="Cluster",
        palette="Set2"
    )

    plt.title("Visualisasi Cluster Pelanggan (PCA 2D)")
    plt.legend()
    st.pyplot(plt)
    plt.close()


# ==============================
# DISTRIBUSI JUMLAH CUSTOMER
# ==============================
def plot_cluster_distribution(lrfm):

    plt.figure(figsize=(6,4))
    sns.countplot(data=lrfm, x="Cluster", palette="Set2")

    plt.title("Distribusi Jumlah Pelanggan per Cluster")
    st.pyplot(plt)
    plt.close()


# ==============================
# RINGKASAN LRFM PER CLUSTER
# ==============================
def cluster_summary(lrfm):

    summary = lrfm.groupby("Cluster")[[
        "Recency", "Length", "Frequency", "Monetary"
    ]].mean().round(2)

    st.subheader("📈 Rata-rata LRFM per Cluster")
    st.dataframe(summary)

    return summary


# ==============================
# REKOMENDASI STRATEGI PEMASARAN
# ==============================
def marketing_recommendation(summary):

    st.subheader("🎯 Rekomendasi Strategi Pemasaran")

    mean_recency = summary["Recency"].mean()
    mean_frequency = summary["Frequency"].mean()
    mean_monetary = summary["Monetary"].mean()

    for cluster_id, row in summary.iterrows():

        st.markdown(f"### Cluster {cluster_id}")

        if row["Recency"] < mean_recency and \
           row["Frequency"] > mean_frequency and \
           row["Monetary"] > mean_monetary:

            st.success("Tipe: High Value / Loyal Customer")
            st.write("""
            - Program loyalty reward
            - Early access produk baru
            - Membership eksklusif
            """)

        elif row["Recency"] > mean_recency and \
             row["Frequency"] < mean_frequency:

            st.warning("Tipe: At Risk / Tidak Aktif")
            st.write("""
            - Promo reaktivasi
            - Diskon comeback
            - Email reminder
            """)

        elif row["Frequency"] > mean_frequency:

            st.info("Tipe: Aktif Potensial")
            st.write("""
            - Cross-selling
            - Upselling
            - Bundling produk
            """)

        else:
            st.write("""
            Tipe: Pelanggan Baru / Potensial
            - Edukasi produk
            - Retargeting ads
            - Promo ringan
            """)

            # ==============================
# PIE CHART DISTRIBUSI CLUSTER (PLOTLY)
# ==============================
import plotly.express as px

def plot_pie_cluster(lrfm):

    cluster_counts = lrfm["Cluster"].value_counts().sort_index()

    fig = px.pie(
        values=cluster_counts.values,
        names=[f"Cluster {i}" for i in cluster_counts.index],
        title="Distribusi Pelanggan per Cluster"
    )

    return fig, cluster_counts