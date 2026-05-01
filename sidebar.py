import streamlit as st

def render_sidebar():

    # =========================
    # STYLE
    # =========================
    st.sidebar.markdown("""
        <style>
        /* Label */
        .nav-label {
            color: #adb5bd;
            font-size: 12px;
            margin-bottom: 8px;
        }

        /* Dropdown styling */
        div[data-baseweb="select"] > div {
            background-color: #343a40 !important;
            border-radius: 10px !important;
            border: none !important;
            color: white !important;
        }

        /* Text dalam dropdown */
        div[data-baseweb="select"] span {
            color: white !important;
        }

        /* Dropdown list */
        ul[role="listbox"] {
            background-color: #343a40 !important;
        }

        li[role="option"] {
            color: white !important;
        }

        /* Highlight selected option */
        li[aria-selected="true"] {
            background-color: #6c757d !important;
        }

        </style>
    """, unsafe_allow_html=True)

    # INIT STATE
    if "page" not in st.session_state:
        st.session_state.page = "Beranda"

    # LABEL
    st.sidebar.markdown(
        "<div class='nav-label'>Navigasi Halaman</div>",
        unsafe_allow_html=True
    )

    # DROPDOWN MENU
    pages = ["Beranda", "Unggah Data File", "Hasil Clustering"]

    selected_page = st.sidebar.selectbox(
        label="",
        options=pages,
        index=pages.index(st.session_state.page)
    )

    # =========================
    # UPDATE STATE
    # =========================
    st.session_state.page = selected_page