import streamlit as st
import plotly.express as px
from segmentation import run_fcm
from visualization import plot_pie_cluster
import pandas as pd

# 🔥 FUNGSI LABEL CLUSTER
def label_clusters(result):

    summary = result.groupby("Cluster").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    }).reset_index()

    # Ranking (semakin kecil Recency = semakin baik)
    summary["R_rank"] = summary["Recency"].rank(ascending=True)
    summary["F_rank"] = summary["Frequency"].rank(ascending=False)
    summary["M_rank"] = summary["Monetary"].rank(ascending=False)

    # Total score
    summary["Score"] = summary["R_rank"] + summary["F_rank"] + summary["M_rank"]

    # Urutkan dari terbaik ke terburuk
    summary = summary.sort_values("Score").reset_index(drop=True)

    n = len(summary)

    labels = []

    for i in range(n):

        if i == 0:
            labels.append("High Value Customer")

        elif i <= n * 0.3:
            labels.append("Loyal Customer")

        elif i <= n * 0.6:
            labels.append("Potential Customer")

        elif i <= n * 0.85:
            labels.append("At Risk Customer")

        else:
            labels.append("Low Value Customer")

    summary["Label"] = labels

    return summary[["Cluster", "Label"]]

# 🔥 MAIN PAGE
def show_clustering():

    # VALIDASI DATA
    if "lrfm" not in st.session_state:
        st.warning("Silakan proses data terlebih dahulu di halaman 'Unggah Data File'.")
        return

    lrfm = st.session_state["lrfm"]
    c_value = st.session_state["c_value"]
    df_all = st.session_state["df_all"]

    # RUN FCM
    result, silhouette = run_fcm(lrfm, n_clusters=c_value)

    # 🔥 TAMBAH LABEL CLUSTER
    cluster_labels = label_clusters(result)
    result = result.merge(cluster_labels, on="Cluster", how="left")

    # 1. RINGKASAN UMUM
    st.markdown("### Ringkasan Umum")

    total_pelanggan = result["username"].nunique()
    total_pesanan = len(df_all)
    total_omset = df_all["total_amount"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Silhouette Score",
        f"{silhouette:.3f}",
        help="""
    Indikator ketepatan pengelompokan (rentang -1 hingga 1). Semakin mendekati 1, perbedaan karakteristik antar kelompok semakin jelas dan akurat.
    """
    )

    col2.metric(
        "Jumlah Pesanan",
        f"{total_pesanan:,}",
        help="Total volume transaksi dengan status 'Selesai' dari data yang diproses."
    )

    col3.metric(
        "Jumlah Pelanggan",
        f"{total_pelanggan:,}",
        help="Jumlah pelanggan unik berdasarkan username. Satu pelanggan dihitung satu kali meskipun melakukan beberapa kali transaksi."
    )

    col4.metric(
        "Total Omset",
        f"Rp {int(total_omset):,}".replace(",", "."),
        help="Akumulasi nilai pendapatan bruto (Monetary) dari seluruh pesanan selesai sebelum dikurangi biaya operasional."
    )

    st.divider()

    # 2. PIE CHART
    st.markdown("### Distribusi Cluster")

    fig, cluster_counts = plot_pie_cluster(result)

    col_chart, col_legend = st.columns([2, 1])

    with col_chart:
        st.plotly_chart(fig, use_container_width=True)

    with col_legend:
        total = cluster_counts.sum()
        for i, val in cluster_counts.items():
            percent = (val / total) * 100
            st.write(f"Cluster {i} : {percent:.1f}% ({val} pelanggan)")

    largest_cluster = cluster_counts.idxmax()
    largest_count = cluster_counts.max()

    largest_label = cluster_labels[
        cluster_labels["Cluster"] == largest_cluster
    ]["Label"].values[0]

    st.markdown("### Insight Utama")

    st.info(
        f"""
    Cluster dengan jumlah pelanggan terbanyak adalah **Cluster {largest_cluster}**
    sebanyak **{largest_count} pelanggan**. Segment ini termasuk kategori **{largest_label}**, yang berarti:
    """
    )

    # Strategi otomatis
    if largest_label == "High Value Customer":
        st.success("Mayoritas pelanggan adalah pelanggan bernilai tinggi.")
        st.write("- Fokus retention & loyalty program")

    elif largest_label == "Loyal Customer":
        st.success("Mayoritas pelanggan sudah loyal.")
        st.write("- Tingkatkan engagement & repeat order")

    elif largest_label == "Potential Customer":
        st.info("Mayoritas pelanggan masih berpotensi berkembang.")
        st.write("- Dorong upselling & bundling")

    elif largest_label == "At Risk Customer":
        st.warning("Banyak pelanggan mulai tidak aktif.")
        st.write("- Jalankan campaign reaktivasi")

    else:
        st.error("Mayoritas pelanggan bernilai rendah.")
        st.write("- Fokus akuisisi & branding")

    st.divider()

    # 4. DESKRIPSI & STRATEGI
    st.markdown("### Deskripsi dan Strategi")

    for i in range(c_value):

        st.markdown(f"#### Cluster {i}")

        cluster_data = result[result["Cluster"] == i]

        if len(cluster_data) == 0:
            st.write("Tidak ada data.")
            continue

        label = cluster_labels[cluster_labels["Cluster"] == i]["Label"].values[0]

        if label == "High Value Customer":
            st.success(label)
            st.write("- Loyalty program\n- Membership\n- Early access produk")

        elif label == "Loyal Customer":
            st.success(label)
            st.write("- Retention campaign\n- Exclusive offer")

        elif label == "Potential Customer":
            st.info(label)
            st.write("- Upselling\n- Cross-selling\n- Bundling produk")

        elif label == "At Risk Customer":
            st.warning(label)
            st.write("- Promo reaktivasi\n- Diskon comeback\n- Reminder marketing")

        else:
            st.error(label)
            st.write("- Campaign awareness\n- Branding ulang")

    st.divider()

        # 3. DETAIL CLUSTER
    st.markdown("### Detail Cluster")

    selected_cluster = st.selectbox(
        "Pilih Cluster",
        sorted(result["Cluster"].unique())
    )

    filtered = result[result["Cluster"] == selected_cluster]

    st.dataframe(
        filtered[["username", "Recency", "Frequency", "Monetary", "Cluster", "Label"]]
        .style.format({
            "Monetary": lambda x: f"Rp {int(x):,}".replace(",", ".")
        }),
        use_container_width=True
    )