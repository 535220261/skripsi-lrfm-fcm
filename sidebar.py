import streamlit as st


def render_sidebar():

    st.sidebar.markdown("""
        <style>
        /* Hilangkan style default button */
        .stButton > button {
            border: none;
            background: none;
            padding: 0;
        }

        /* Custom button */
        .nav-btn {
            display: block;
            width: 100%;
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 12px;
            text-align: left;
            font-weight: 500;
            color: white;
            text-decoration: none;
        }

        /* Active */
        .active {
            background-color: #6c757d;
        }

        /* Non-active */
        .inactive {
            background-color: #343a40;
        }

        /* Hover effect halus */
        .nav-btn:hover {
            opacity: 0.85;
        }

        /* Label kecil */
        .nav-label {
            color: #adb5bd;
            font-size: 12px;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.sidebar.markdown("### 📊 Elleano Dashboard")

    # LABEL
    st.sidebar.markdown('<div class="nav-label">Navigasi</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-label">Pilih halaman</div>', unsafe_allow_html=True)

    # STATE HALAMAN
    if "page" not in st.session_state:
        st.session_state.page = "Beranda"

    def nav_button(label):
        is_active = st.session_state.page == label
        css_class = "nav-btn active" if is_active else "nav-btn inactive"

        if st.sidebar.button(label, key=label):
            st.session_state.page = label

        st.sidebar.markdown(
            f'<div class="{css_class}">{label}</div>',
            unsafe_allow_html=True
        )

    # MENU
    nav_button("Beranda")
    nav_button("Unggah Data File")
    nav_button("Hasil Clustering")