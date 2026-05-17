import streamlit as st
import pandas as pd

from loaders import (
    load_shopee,
    load_tiktok,
    load_lazada
)

from segmentation import (
    calculate_lrfm,
    run_fcm
)

# MENCARI JUMLAH CLUSTER TERBAIK
def find_best_cluster(
    lrfm,
    min_cluster=2,
    max_cluster=8
):

    best_score = -1
    best_cluster = 2

    scores = []

    for k in range(min_cluster, max_cluster + 1):

        try:

            _, silhouette = run_fcm(
                lrfm,
                n_clusters=k
            )

            scores.append({
                "Jumlah Cluster": k,
                "Kualitas Segmentasi": round(
                    silhouette,
                    3
                )
            })

            if silhouette > best_score:

                best_score = silhouette
                best_cluster = k

        except Exception:

            pass

    score_df = pd.DataFrame(scores)

    return (
        int(best_cluster),
        float(best_score),
        score_df
    )

# HALAMAN UPLOAD
def show_upload():

    st.header("Upload Data Transaksi")

    st.markdown("""
Upload file transaksi marketplace yang diekspor langsung dari dashboard seller center.

Sistem akan:
- Membersihkan data transaksi
- Menghapus data retur/cancel
- Menghitung nilai LRFM
- Melakukan segmentasi pelanggan otomatis
""")

    st.divider()

    # UPLOAD FILE
    col1, col2, col3 = st.columns(3)

    # SHOPEE
    with col1:

        shopee_file = st.file_uploader(
            "Upload Data Shopee",
            type=["xlsx"],
            help="""
Gunakan file export transaksi Shopee Seller Center (.xlsx)
"""
        )

    # TIKTOK
    with col2:

        tiktok_file = st.file_uploader(
            "Upload Data TikTok Shop",
            type=["csv"],
            help="""
Gunakan file export transaksi TikTok Shop (.csv)
"""
        )

    # LAZADA
    with col3:

        lazada_file = st.file_uploader(
            "Upload Data Lazada",
            type=["xlsx"],
            help="""
Gunakan file export transaksi Lazada (.xlsx)
"""
        )

    st.divider()

    # PENGATURAN CLUSTER

    st.markdown("### Pengaturan Segmentasi")

    cluster_mode = st.radio(
        "Metode Penentuan Jumlah Cluster",
        [
            "Otomatis (Rekomendasi Sistem)",
            "Manual"
        ],
        help="""
Mode otomatis akan mencari jumlah cluster terbaik berdasarkan kualitas segmentasi.
Mode manual digunakan untuk kebutuhan eksperimen atau analisis lanjutan.
"""
    )

    # MANUAL
    if cluster_mode == "Manual":

        c_value = st.slider(
            "Jumlah Cluster",
            min_value=2,
            max_value=8,
            value=4
        )

        st.caption("""
Jumlah cluster ditentukan secara manual oleh pengguna.

Semakin banyak cluster:
- Segmentasi menjadi lebih detail
- Namun belum tentu menghasilkan kualitas segmentasi terbaik
""")

    # OTOMATIS

    else:

        c_value = None

        st.caption("""
Sistem akan mencoba beberapa jumlah cluster dan memilih hasil segmentasi terbaik secara otomatis.
""")

    st.divider()

    # PROSES SEGMENTASI

    if st.button(
        "Proses Segmentasi",
        use_container_width=True
    ):

        dataframes = []

        total_removed_return = 0

        # ==================================
        # LOAD SHOPEE
        # ==================================

        if shopee_file:

            try:

                df_shopee, removed = (
                    load_shopee(shopee_file)
                )

                dataframes.append(df_shopee)

                total_removed_return += removed

            except ValueError as e:

                st.error(f"""
❌ Terjadi kesalahan pada file Shopee

{str(e)}
""")

                st.stop()

            except Exception:

                st.error("""
❌ File Shopee gagal diproses

Pastikan:
- File merupakan export dari Website Shopee Seller Center
- Format file adalah .xlsx
- File tidak rusak/corrupt
""")

                st.stop()

        # LOAD TIKTOK
        if tiktok_file:

            try:

                df_tiktok, removed = (
                    load_tiktok(tiktok_file)
                )

                dataframes.append(df_tiktok)

                total_removed_return += removed

            except ValueError as e:

                st.error(f"""
❌ Terjadi kesalahan pada file TikTok Shop

{str(e)}
""")

                st.stop()

            except Exception:

                st.error("""
❌ File TikTok Shop gagal diproses

Pastikan:
- File merupakan export dari Website TikTok Shop
- Format file adalah .csv
- File tidak rusak/corrupt
""")

                st.stop()

        # LOAD LAZADA

        if lazada_file:

            try:

                df_lazada, removed = (
                    load_lazada(lazada_file)
                )

                dataframes.append(df_lazada)

                total_removed_return += removed

            except ValueError as e:

                st.error(f"""
❌ Terjadi kesalahan pada file Lazada

{str(e)}
""")

                st.stop()

            except Exception:

                st.error("""
❌ File Lazada gagal diproses

Pastikan:
- File merupakan export  dari Website Lazada Seller Center
- Format file adalah .xlsx
- File tidak rusak/corrupt
""")

                st.stop()

        # VALIDASI FILE KOSONG

        if len(dataframes) == 0:

            st.warning("""
Silakan upload minimal 1 file marketplace terlebih dahulu.
""")

            st.stop()

        # GABUNGKAN DATA

        try:

            df_all = pd.concat(
                dataframes,
                ignore_index=True
            )

        except Exception:

            st.error("""
❌ Terjadi kesalahan saat menggabungkan dataset marketplace.
""")

            st.stop()

        # VALIDASI DATA KOSONG

        if len(df_all) == 0:

            st.error("""
❌ Dataset tidak memiliki data transaksi yang dapat diproses.
""")

            st.stop()

        # MARKETPLACE DIGUNAKAN

        used_platforms = (
            df_all["marketplace"]
            .dropna()
            .unique()
        )

        # PERIODE DATASET

        try:

            min_date = pd.to_datetime(
                df_all["order_date"]
            ).min()

            max_date = pd.to_datetime(
                df_all["order_date"]
            ).max()

            dataset_period = (
                f"{min_date.strftime('%d %B %Y')} "
                f"- "
                f"{max_date.strftime('%d %B %Y')}"
            )

        except Exception:

            dataset_period = (
                "Periode tidak dapat dibaca"
            )

        # HITUNG LRFM
        try:

            lrfm = calculate_lrfm(df_all)

        except Exception:

            st.error("""
❌ Gagal menghitung nilai LRFM.

Kemungkinan:
- Format data tidak sesuai
- Terdapat data transaksi tidak valid
- Kolom tanggal / nominal bermasalah
""")

            st.stop()

        # VALIDASI LRFM
        if len(lrfm) == 0:

            st.error("""
❌ Tidak ada data pelanggan yang dapat dihitung.
""")

            st.stop()

        # CLUSTER OTOMATIS
        if cluster_mode == (
            "Otomatis (Rekomendasi Sistem)"
        ):

            with st.spinner(
                "Mencari jumlah cluster terbaik..."
            ):

                (
                    best_cluster,
                    best_score,
                    score_df
                ) = find_best_cluster(lrfm)

                c_value = int(best_cluster)

            st.success(f"""
Jumlah cluster terbaik berhasil ditemukan.

Jumlah Cluster:
{c_value}

Kualitas Segmentasi:
{best_score:.3f}
""")

            st.markdown(
                "#### Evaluasi Jumlah Cluster"
            )

            st.dataframe(
                score_df,
                use_container_width=True
            )

        # INFORMASI DATASET
        st.info(f"""
Marketplace yang diproses:
{', '.join(used_platforms)}

Periode dataset:
{dataset_period}

Jumlah transaksi:
{len(df_all):,}

Data retur/cancel dibersihkan:
{total_removed_return:,}
""")

        # SESSION STATE
        st.session_state["df_all"] = df_all

        st.session_state["lrfm"] = lrfm

        st.session_state["c_value"] = int(c_value)

        st.session_state[
            "total_removed_return"
        ] = total_removed_return

        st.session_state[
            "used_platforms"
        ] = used_platforms

        st.session_state[
            "dataset_period"
        ] = dataset_period

        st.session_state[
            "processing_done"
        ] = True

    # NAVIGASI
    if st.session_state.get(
        "processing_done"
    ):

        st.success(
            "Data berhasil diproses ✅"
        )

        if st.button(
            "➡️ Lihat Hasil Clustering",
            use_container_width=True
        ):

            st.session_state.page = (
                "Hasil Clustering"
            )

            st.rerun()