import streamlit as st
import pandas as pd
from segmentation import run_fcm
from visualization import plot_pie_cluster

# LABEL CLUSTER OTOMATIS
def label_clusters(result):

    summary = result.groupby("Cluster").agg({
        "Length": "mean",
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    }).reset_index()

    # Ranking
    summary["L_rank"] = summary["Length"].rank(ascending=False)
    summary["R_rank"] = summary["Recency"].rank(ascending=True)
    summary["F_rank"] = summary["Frequency"].rank(ascending=False)
    summary["M_rank"] = summary["Monetary"].rank(ascending=False)

    summary["Score"] = (
        summary["L_rank"] +
        summary["R_rank"] +
        summary["F_rank"] +
        summary["M_rank"]
    )

    summary = summary.sort_values(
        "Score"
    ).reset_index(drop=True)

    label_order = [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "New Customers",
        "At Risk Customers",
        "About To Sleep",
        "High Spender Infrequent",
        "Lost Customers"
    ]

    summary["Label"] = label_order[:len(summary)]

    return summary[["Cluster", "Label"]]


# INTERPRETASI KUALITAS SEGMENTASI
def show_segmentation_quality(score):

    if score >= 0.5:

        st.success("""
Kualitas segmentasi sangat baik 👍

Karakteristik antar kelompok pelanggan terlihat jelas sehingga strategi pemasaran dapat dibuat lebih tepat sasaran.
""")

    elif 0.25 <= score < 0.5:

        st.info("""
Kualitas segmentasi cukup baik.

Pemisahan antar kelompok pelanggan sudah terlihat, namun masih dapat ditingkatkan.
""")

    elif 0 <= score < 0.25:

        st.warning("""
Kualitas segmentasi kurang optimal ⚠️

Karakteristik antar kelompok pelanggan masih cukup mirip sehingga hasil segmentasi kurang maksimal.
""")

    else:

        st.error("""
Kualitas segmentasi buruk ❌

Kemungkinan terjadi overlap antar kelompok pelanggan.
Disarankan mencoba jumlah cluster yang berbeda.
""")


# STRATEGI CLUSTER
def show_cluster_strategy(label):

    # CHAMPIONS
    if label == "Champions":

        st.success("Champions")

        st.markdown("""
### Karakteristik
- Sangat aktif bertransaksi
- Frekuensi pembelian sangat tinggi
- Kontribusi omzet terbesar
- Loyal dalam jangka panjang

### Interpretasi
Pelanggan paling bernilai bagi bisnis dengan kontribusi transaksi dan loyalitas tertinggi.

### Strategi Pemasaran
- Loyalty program premium
- Membership eksklusif
- Personalized marketing
- Referral reward
- Early access produk baru
""")

    # LOYAL
    elif label == "Loyal Customers":

        st.success("Loyal Customers")

        st.markdown("""
### Karakteristik
- Sering melakukan transaksi
- Loyalitas tinggi
- Kontribusi transaksi stabil

### Interpretasi
Pelanggan yang telah mempercayai brand dan cenderung melakukan repeat order secara konsisten.

### Strategi Pemasaran
- Retention campaign
- Point reward
- Bundling produk
- Exclusive offer
- Upselling produk premium
""")

    # POTENTIAL
    elif label == "Potential Loyalists":

        st.info("Potential Loyalists")

        st.markdown("""
### Karakteristik
- Pelanggan relatif baru
- Aktivitas transaksi mulai meningkat
- Potensi loyalitas tinggi

### Interpretasi
Memiliki peluang berkembang menjadi pelanggan loyal apabila diberikan pengalaman transaksi yang baik.

### Strategi Pemasaran
- Promo pembelian kedua
- Voucher repeat order
- Cross-selling
- Edukasi produk
- Follow up customer baru
""")

    # NEW
    elif label == "New Customers":

        st.info("New Customers")

        st.markdown("""
### Karakteristik
- Baru pertama kali bertransaksi
- Aktivitas pembelian masih rendah

### Interpretasi
Pelanggan baru yang masih berada pada tahap awal hubungan dengan bisnis.

### Strategi Pemasaran
- Welcome campaign
- First purchase discount
- Customer onboarding
- Edukasi produk
""")

    # AT RISK
    elif label == "At Risk Customers":

        st.warning("At Risk Customers")

        st.markdown("""
### Karakteristik
- Aktivitas transaksi mulai menurun
- Sudah cukup lama tidak bertransaksi

### Interpretasi
Pelanggan mulai kehilangan ketertarikan terhadap bisnis dan berisiko churn.

### Strategi Pemasaran
- Campaign reaktivasi
- Reminder marketing
- Diskon comeback customer
- Retargeting iklan
""")

    # ABOUT TO SLEEP
    elif label == "About To Sleep":

        st.warning("About To Sleep")

        st.markdown("""
### Karakteristik
- Aktivitas transaksi hampir berhenti
- Jarang melakukan pembelian

### Interpretasi
Pelanggan yang hampir tidak aktif dan berpotensi segera hilang.

### Strategi Pemasaran
- Flash sale khusus
- Promo terbatas waktu
- Voucher reaktivasi
- Broadcast campaign
""")

    # HIGH SPENDER
    elif label == "High Spender Infrequent":

        st.info("High Spender Infrequent")

        st.markdown("""
### Karakteristik
- Nilai transaksi tinggi
- Frekuensi pembelian rendah

### Interpretasi
Pelanggan dengan kontribusi monetary besar namun jarang bertransaksi.

### Strategi Pemasaran
- Cross-selling produk premium
- Personalized recommendation
- Exclusive bundle
- Priority service
""")

    # LOST
    else:

        st.error("Lost Customers")

        st.markdown("""
### Karakteristik
- Sangat jarang melakukan transaksi
- Nilai pembelian rendah
- Loyalitas rendah

### Interpretasi
Pelanggan dengan kontribusi paling rendah dan kemungkinan besar sudah tidak aktif.

### Strategi Pemasaran
- Campaign awareness otomatis
- Remarketing biaya rendah
- Promosi massal
- Branding media sosial
""")

# MAIN PAGE
def show_clustering():
    # VALIDASI SESSION

    if "lrfm" not in st.session_state:

        st.warning("""
Silakan proses data terlebih dahulu pada halaman Upload Data.
""")

        return

    # SESSION DATA

    lrfm = st.session_state["lrfm"]

    c_value = st.session_state["c_value"]

    df_all = st.session_state["df_all"]

    used_platforms = st.session_state.get(
        "used_platforms",
        []
    )

    dataset_period = st.session_state.get(
        "dataset_period",
        "-"
    )

    # RUN FCM
    with st.spinner(
        "Melakukan segmentasi pelanggan..."
    ):

        result, silhouette = run_fcm(
            lrfm,
            n_clusters=c_value
        )

    # LABELING
    cluster_labels = label_clusters(result)

    result = result.merge(
        cluster_labels,
        on="Cluster",
        how="left"
    )

    # RINGKASAN UMUM
    st.markdown("## Ringkasan Hasil Segmentasi")

    total_pelanggan = result["username"].nunique()

    total_pesanan = len(df_all)

    total_omset = df_all["total_amount"].sum()

    col1, col2, col3, col4 = st.columns(4)

    # KUALITAS
    with col1:

        st.metric(
            "Kualitas Segmentasi",
            f"{silhouette:.3f}"
        )

    # PESANAN
    col2.metric(
        "Jumlah Pesanan",
        f"{total_pesanan:,}"
    )

    # PELANGGAN
    col3.metric(
        "Jumlah Pelanggan",
        f"{total_pelanggan:,}"
    )

    # OMSET
    col4.metric(
        "Total Omset",
        f"Rp {int(total_omset):,}".replace(",", ".")
    )

    # INTERPRETASI
    show_segmentation_quality(silhouette)

    st.info(f"""
Marketplace diproses:
{', '.join(used_platforms)}

Periode dataset:
{dataset_period}

Jumlah cluster digunakan:
{c_value}
""")

    st.divider()

    # DISTRIBUSI CLUSTER
    st.markdown("## Distribusi Segmentasi")

    fig, cluster_counts = plot_pie_cluster(
        result
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # DESKRIPSI CLUSTER
    st.markdown("## Deskripsi dan Strategi Cluster")

    clusters = sorted(
        result["Cluster"].unique()
    )

    for idx in range(0, len(clusters), 2):

        col1, col2 = st.columns(2)

        # KOLOM 1
        with col1:

            cluster_id = clusters[idx]

            label = cluster_labels[
                cluster_labels["Cluster"] == cluster_id
            ]["Label"].values[0]

            with st.expander(
                f"Cluster {cluster_id} - {label}"
            ):

                show_cluster_strategy(label)

        # KOLOM 2
        if idx + 1 < len(clusters):

            with col2:

                cluster_id = clusters[idx + 1]

                label = cluster_labels[
                    cluster_labels["Cluster"] == cluster_id
                ]["Label"].values[0]

                with st.expander(
                    f"Cluster {cluster_id} - {label}"
                ):

                    show_cluster_strategy(label)

    st.divider()

    # DETAIL CLUSTER
    st.markdown("## Detail Data Pelanggan")

    selected_cluster = st.selectbox(
        "Pilih Cluster",
        sorted(result["Cluster"].unique())
    )

    filtered = result[
        result["Cluster"] == selected_cluster
    ]

    st.dataframe(
        filtered[
            [
                "username",

                "Length",
                "Recency",
                "Frequency",
                "Monetary",

                "Cluster",
                "Label"
            ]
        ].rename(columns={

            "Length":
            "Length\n(Lama Berlangganan)",

            "Recency":
            "Recency\n(Jarak Transaksi Terakhir)",

            "Frequency":
            "Frequency\n(Frekuensi Transaksi)",

            "Monetary":
            "Monetary\n(Total Nilai Transaksi)"
        }).style.format({

            "Monetary":
            lambda x: f"Rp {int(x):,}".replace(",", ".")

        }),
        use_container_width=True
    )