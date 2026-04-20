import streamlit as st
import plotly.express as px
from segmentation import run_fcm
from visualization import plot_pie_cluster

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

    # RINGKASAN UMUM
    st.markdown("###Ringkasan Umum")

    total_pelanggan = result["username"].nunique()
    total_pesanan = len(df_all)
    total_omset = df_all["total_amount"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Silhouette Score", f"{silhouette:.3f}")
    col2.metric("Jumlah Pesanan", f"{total_pesanan:,}")
    col3.metric("Jumlah Pelanggan", f"{total_pelanggan:,}")
    col4.metric("Total Omset", f"Rp {int(total_omset):,}".replace(",", "."))

    st.divider()

    # ===============================
    # 2. PIE CHART
    # ===============================
    st.markdown("###Distribusi Cluster")

    fig, cluster_counts = plot_pie_cluster(result)

    col_chart, col_legend = st.columns([2,1])

    with col_chart:
        st.plotly_chart(fig, use_container_width=True)

    with col_legend:
        total = cluster_counts.sum()
        for i, val in cluster_counts.items():
            percent = (val / total) * 100
            st.write(f"Cluster {i} : {percent:.1f}% ({val} pelanggan)")

    st.divider()

    # ===============================
    # 3. DETAIL CLUSTER
    # ===============================
    st.markdown("###Detail Cluster")

    selected_cluster = st.selectbox(
        "Pilih Cluster",
        sorted(result["Cluster"].unique())
    )

    filtered = result[result["Cluster"] == selected_cluster]

    st.dataframe(
        filtered.style.format({
            "Monetary": lambda x: f"Rp {int(x):,}".replace(",", ".")
        }),
        use_container_width=True
    )

    st.divider()

    # ===============================
    # 4. DESKRIPSI & STRATEGI
    # ===============================
    st.markdown("###Deskripsi dan Strategi")

    for i in range(c_value):

        st.markdown(f"#### Cluster {i}")

        cluster_data = result[result["Cluster"] == i]

        if len(cluster_data) == 0:
            st.write("Tidak ada data.")
            continue

        avg = cluster_data[["Recency","Frequency","Monetary"]].mean()

        if avg["Frequency"] > result["Frequency"].mean() and avg["Monetary"] > result["Monetary"].mean():
            st.success("Pelanggan Loyal / High Value")
            st.write("- Loyalty program\n- Membership\n- Early access produk")

        elif avg["Recency"] > result["Recency"].mean():
            st.warning("Pelanggan Tidak Aktif / At Risk")
            st.write("- Promo reaktivasi\n- Diskon comeback\n- Reminder marketing")

        else:
            st.info("Pelanggan Potensial")
            st.write("- Upselling\n- Cross-selling\n- Bundling produk")