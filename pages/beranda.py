import streamlit as st

def show_beranda():

    st.markdown("### Selamat Datang di Aplikasi Segmentasi Pelanggan")

    st.markdown(
        """
        <p style='font-size:14px; color:#495057;'>
        Aplikasi ini dirancang untuk membantu anda sebagai seller e-commerce untuk melakukan segmentasi pelanggan 
        menggunakan algoritma Fuzzy C-Means dengan model Length, Recency, Frequency dan Monetary.
        </p>
        """,
        unsafe_allow_html=True
    )