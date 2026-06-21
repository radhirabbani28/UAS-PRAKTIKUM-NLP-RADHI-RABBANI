"""
Entry point aplikasi: Simple Car Advisor (Streamlit version)
Jalankan dengan: streamlit run app.py
"""

import streamlit as st
from src.config import *  # load .env dan setup LangSmith
from src.graph import build_graph

# ============================================================
# Konfigurasi halaman
# ============================================================
st.set_page_config(
    page_title="Simple Car Advisor",
    page_icon="🚗",
    layout="centered",
)

# Cache graph supaya tidak dibangun ulang setiap interaksi
@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

# ============================================================
# Header
# ============================================================
st.title("🚗 Simple Car Advisor")
st.markdown(
    "Asisten rekomendasi mobil bekas berbasis **LangChain + LangGraph + LangSmith**. "
    "Ceritakan budget dan kebutuhanmu, sistem akan merekomendasikan mobil yang paling cocok."
)

st.divider()

# ============================================================
# Form Input
# ============================================================
with st.form("car_advisor_form"):
    user_input = st.text_area(
        "Ceritakan kebutuhanmu:",
        placeholder="Contoh: budget 150 juta, buat keluarga, irit BBM",
        height=100,
    )
    submitted = st.form_submit_button("🔍 Cari Rekomendasi", use_container_width=True)

# ============================================================
# Proses & Tampilkan Hasil
# ============================================================
if submitted:
    if not user_input.strip():
        st.warning("Mohon isi kebutuhan kamu terlebih dahulu.")
    else:
        with st.spinner("Sedang menganalisis kebutuhan dan mencari mobil terbaik..."):
            try:
                result = graph.invoke({"user_input": user_input})

                # Simpan ke session state supaya tidak hilang saat re-render
                st.session_state["result"] = result

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
                st.session_state["result"] = None

# Tampilkan hasil jika ada
if st.session_state.get("result"):
    result = st.session_state["result"]

    st.divider()
    st.subheader("📋 Ringkasan Kebutuhan")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Budget", f"Rp{result['budget']:,}".replace(",", "."))
    with col2:
        st.metric("Kebutuhan", result["kebutuhan"])

    st.subheader("💬 Rekomendasi")
    st.info(result["rekomendasi_akhir"])

    st.subheader("🏆 Mobil Pilihan Terbaik")
    for i, mobil in enumerate(result["ranking"], start=1):
        with st.container(border=True):
            st.markdown(f"**#{i}. {mobil['merek']} {mobil['model']}**")
            st.caption(f"ID Mobil: {mobil['id']}")
            st.write(f"📝 {mobil['alasan_singkat']}")

    # Detail kandidat mentah (opsional, untuk transparansi)
    with st.expander("🔎 Lihat semua kandidat yang difilter (sebelum ranking)"):
        st.json(result["kandidat"])

# ============================================================
# Sidebar: Info Proyek
# ============================================================
with st.sidebar:
    st.header("ℹ️ Tentang Proyek")
    st.markdown("""
    Proyek UAS Natural Language Processing (NLP) yang menggunakan:

    - **LangChain** — prompt template & chain untuk ekstraksi kebutuhan, ranking, dan penulisan rekomendasi
    - **LangGraph** — alur kerja sistem sebagai graph 4 node
    - **LangSmith** — tracing & monitoring tiap pemanggilan LLM

    LLM: Groq (Llama 3.3 70B) — gratis & cepat.
    """)
    st.divider()
    st.caption("Cek tracing lengkap di [smith.langchain.com](https://smith.langchain.com)")