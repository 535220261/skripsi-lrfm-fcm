import streamlit as st

def show_beranda():

    # HEADER
    st.markdown("## Selamat Datang di Aplikasi Segmentasi Pelanggan")

    st.markdown(
        """
        <style>
        .adaptive-text {
            color: #000000;
            text-align: justify;
            font-size: 16px;
        }

        @media (prefers-color-scheme: dark) {
            .adaptive-text {
                color: #FFFFFF;
            }
        }
        </style>

        <p class='adaptive-text'>
        Aplikasi ini dirancang untuk membantu seller e-commerce dalam melakukan analisis segmentasi pelanggan 
        menggunakan algoritma <b>Fuzzy C-Means (FCM)</b> dengan model <b>LRFM (Length, Recency, Frequency, Monetary)</b>.
        </p>

        <p class='adaptive-text'>
        Segmentasi pelanggan digunakan untuk mengelompokkan pelanggan berdasarkan perilaku transaksi sehingga 
        pemilik bisnis dapat memahami karakteristik pelanggan dan menentukan strategi pemasaran yang lebih tepat sasaran.
        </p>

        <p class='adaptive-text'>
        Data transaksi yang digunakan dapat berasal dari marketplace seperti Shopee, TikTok Shop, dan Lazada 
        yang diekspor langsung dari dashboard seller center.
        </p>

        <p class='adaptive-text'>
        Aplikasi ini membantu seller untuk:
        <br>• Memahami karakteristik pelanggan
        <br>• Menentukan strategi pemasaran yang lebih tepat sasaran
        <br>• Mengidentifikasi pelanggan potensial dan pelanggan berisiko churn
        <br>• Meningkatkan loyalitas pelanggan
        <br>• Mendukung pengambilan keputusan bisnis berbasis data
        </p>
        """,
        unsafe_allow_html=True
    )

    # QUICK LINK
    st.markdown("### Navigasi Cepat")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("[📘 Penjelasan Komponen](#penjelasan-komponen)")

    with col2:
        st.markdown("[⚙️ Quick Guide Penggunaan](#quick-guide-penggunaan-aplikasi)")

    st.divider()

    # PENJELASAN KOMPONEN
    st.markdown("### Penjelasan Komponen")

    with st.expander("📘 Lihat Penjelasan Komponen LRFM & Silhouette Score"):

        st.markdown("""
### Length (L)
Mengukur lamanya hubungan pelanggan dengan bisnis berdasarkan rentang waktu transaksi pertama hingga transaksi terakhir.

### Recency (R)
Mengukur seberapa baru pelanggan melakukan transaksi terakhir. 
Semakin kecil nilai Recency, semakin aktif pelanggan tersebut.

### Frequency (F)
Mengukur seberapa sering pelanggan melakukan transaksi dalam periode tertentu.

### Monetary (M)
Mengukur total nilai transaksi atau kontribusi pendapatan yang diberikan pelanggan kepada bisnis.

---
### Silhouette Score
Silhouette Score digunakan untuk mengukur kualitas hasil clustering. 
Semakin mendekati nilai 1, maka kualitas segmentasi pelanggan semakin baik.

| Nilai Silhouette Score | Interpretasi |
|---|---|
| > 0.70 | Cluster sangat baik dan terpisah jelas |
| 0.50 – 0.70 | Cluster baik |
| 0.25 – 0.50 | Cluster cukup baik |
| < 0.25 | Cluster kurang optimal |
| < 0 | Cluster buruk atau overlap |
""")

    st.divider()

    # QUICK GUIDE
    st.markdown("### Quick Guide Penggunaan Aplikasi")

    with st.expander("⚙️ Lihat Panduan Penggunaan Aplikasi"):

        st.markdown("""
#### 1. Upload File Dataset
- Masuk ke halaman **Unggah Data File**
- Upload file transaksi dari marketplace:
  - Shopee
  - TikTok Shop
  - Lazada
- Minimal upload 1 file marketplace
- Gunakan file hasil ekspor langsung dari seller center marketplace

---
#### 2. Tentukan Jumlah Cluster
- Pilih jumlah cluster (C) sesuai kebutuhan
- Semakin besar jumlah cluster, segmentasi pelanggan akan semakin detail
- Namun, jumlah cluster yang besar belum tentu menghasilkan kualitas clustering yang baik

---
#### 3. Proses Segmentasi
- Klik tombol **Proses Segmentasi**
- Sistem akan:
  - Membersihkan data transaksi
  - Menghapus data retur dan cancel
  - Menghitung nilai LRFM
  - Melakukan clustering menggunakan algoritma Fuzzy C-Means

---
#### 4. Analisis Hasil Cluster
Pada halaman hasil clustering, sistem akan menampilkan:
- Silhouette Score
- Distribusi cluster
- Label segmentasi pelanggan
- Karakteristik cluster
- Strategi pemasaran
- Insight bisnis berdasarkan perilaku pelanggan
""")