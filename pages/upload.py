import streamlit as st
import pandas as pd
from loaders import load_shopee, load_tiktok, load_lazada
from segmentation import calculate_lrfm

def show_upload():

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

    c_value = st.slider("Pilih jumlah cluster (C)", 2, 8, 4)

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

            # Simpan ke session_state untuk halaman clustering
            st.session_state["df_all"] = df_all
            st.session_state["lrfm"] = lrfm
            st.session_state["c_value"] = c_value
            st.session_state["total_removed_return"] = total_removed_return

            st.success("Data berhasil diproses. Silakan buka halaman 'Hasil Clustering'.")
        else:
            st.warning("Upload minimal satu file marketplace.")