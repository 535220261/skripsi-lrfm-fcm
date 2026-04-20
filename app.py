import streamlit as st
from sidebar import render_sidebar
from pages.beranda import show_beranda
from pages.upload import show_upload
from pages.clustering import show_clustering

st.set_page_config(page_title="Segmentasi Pelanggan Elleano", layout="wide")

# Sidebar
render_sidebar()

# Judul global
st.markdown(
    """
    <h2 style='color:#00000;'>
    Segmentasi Pelanggan Menggunakan Fuzzy C-Means dengan Model Length, Recency, Frequency dan Monetary
    </h2>
    """,
    unsafe_allow_html=True
)

st.divider()

# Routing halaman
page = st.session_state.get("page", "Beranda")

if page == "Beranda":
    show_beranda()

elif page == "Unggah Data File":
    show_upload()

elif page == "Hasil Clustering":
    show_clustering()