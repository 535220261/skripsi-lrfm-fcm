import streamlit as st
import pandas as pd
from loaders import load_shopee, load_tiktok, load_lazada
from segmentation import calculate_lrfm, run_fcm

st.set_page_config(page_title="Segmentasi Pelanggan Elleano", layout="wide")

st.title("Aplikasi Segmentasi Pelanggan Elleano.id")
st.markdown("Implementasi Fuzzy C-Means dengan Model LRFM")

st.divider()

# ===============================
# UPLOAD SECTION
# ===============================

st.header("Upload Data Transaksi")

col1, col2, col3 = st.columns(3)

with col1:
    shopee_file = st.file_uploader("Upload Data Shopee", type=["xlsx"])

with col2:
    tiktok_file = st.file_uploader("Upload Data TikTok Shop", type=["xlsx"])

with col3:
    lazada_file = st.file_uploader("Upload Data Lazada", type=["xlsx"])

st.divider()

st.subheader("⚙️ Pengaturan Jumlah Cluster (C)")

c_value = st.slider(
    "Pilih jumlah cluster (C)",
    min_value=2,
    max_value=8,
    value=4
)

if st.button("Proses Segmentasi"):

    dataframes = []
    total_removed_return = 0

    if shopee_file:
        df_shopee, removed = load_shopee(shopee_file)
        dataframes.append(df_shopee)
        total_removed_return += removed

    if tiktok_file:
        df_tiktok, removed = load_tiktok(tiktok_file)
        dataframes.append(df_tiktok)
        total_removed_return += removed

    if lazada_file:
        df_lazada, removed = load_lazada(lazada_file)
        dataframes.append(df_lazada)
        total_removed_return += removed

    if dataframes:
        df_all = pd.concat(dataframes)

        lrfm = calculate_lrfm(df_all)
        result, silhouette = run_fcm(lrfm, n_clusters=c_value)

        # =============================
        # RINGKASAN DATA
        # =============================
        st.success("Segmentasi selesai!")

        st.markdown("### 📊 Ringkasan Praproses")
        st.write(f"Jumlah data setelah praproses: **{len(df_all):,} baris**")
        st.write(f"Jumlah data Retur/Refund yang dihapus: **{total_removed_return:,} baris**")
        st.write(f"Jumlah cluster (C): **{c_value}**")
        st.write(f"Silhouette Score: **{silhouette:.3f}**")

        # =============================
        # TOGGLE TAMPIL / SEMBUNYI TABEL
        # =============================
        with st.expander("Tabel LRFM (Klik untuk tampil/sembunyi)", expanded=False):
            st.dataframe(
                result.style.format({
                    "Monetary": lambda x: f"Rp {int(x):,}".replace(",", ".")
                })
            )
    else:
        st.warning("Upload minimal satu file marketplace.")