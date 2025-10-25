import streamlit as st
import json
import time
from datetime import datetime
import os

# ============================================================
# KONFIGURASI DASAR
# ============================================================
st.set_page_config(
    page_title="AC Expert System",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS inline tambahan agar sidebar selalu tampil & tidak bisa di-hide
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        transform: none !important;
        visibility: visible !important;
        opacity: 1 !important;
        transition: none !important;
    }
    [data-testid="stSidebarCollapseControl"],
    button[data-testid="baseButton-headerNoPadding"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD CSS EKSTERNAL
# ============================================================
def load_css(file_name="style.css"):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ File CSS '{file_name}' tidak ditemukan.")

load_css()

# ============================================================
# FUNGSI PEMBACA JSON
# ============================================================
def load_knowledge_base():
    with open("knowledge_base.json", "r", encoding="utf-8") as f:
        return json.load(f)

kb = load_knowledge_base()

SYMPTOMS = {g["kode"]: g["deskripsi"] for g in kb["gejala"]}
RULES = kb["rules"]
SOLUSI = {s["kode_kerusakan"]: s for s in kb["solusi"]}
KERUSAKAN = {k["kode"]: k for k in kb["kerusakan"]}

# ============================================================
# SESSION STATE
# ============================================================
if "menu" not in st.session_state:
    st.session_state.menu = "home"
if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []
if "result" not in st.session_state:
    st.session_state.result = None
if "selected_history" not in st.session_state:
    st.session_state.selected_history = None

# ============================================================
# FUNGSI PENYIMPANAN RIWAYAT
# ============================================================
def save_history(symptoms, result):
    if not result:
        return
    history_entry = {
        "id": f"{int(time.time())}",
        "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "symptoms": symptoms,
        "result": result
    }
    try:
        if os.path.exists("riwayat.txt"):
            with open("riwayat.txt", "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except:
        data = []

    data.append(history_entry)
    with open("riwayat.txt", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_history():
    if os.path.exists("riwayat.txt"):
        with open("riwayat.txt", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">💠 AC Expert</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Sistem Diagnosis AC Split</div>', unsafe_allow_html=True)

    if st.button("🏠 Beranda", use_container_width=True):
        st.session_state.menu = "home"
        st.rerun()
    if st.button("🩺 Diagnosa", use_container_width=True):
        st.session_state.menu = "diagnosa"
        st.rerun()
    if st.button("📘 Knowledge Base", use_container_width=True):
        st.session_state.menu = "knowledge"
        st.rerun()
    if st.button("🕓 Riwayat Diagnosa", use_container_width=True):
        st.session_state.menu = "history"
        st.rerun()

# ============================================================
# MENU: BERANDA
# ============================================================
if st.session_state.menu == "home":
    st.markdown('<h1 class="page-title">💠 Selamat Datang di AC Expert System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Sistem pakar untuk membantu mendiagnosis kerusakan pada AC Split.</p>', unsafe_allow_html=True)

    total_rules = len(RULES)
    total_history = len(load_history())
    avg_cf = round(sum(r["CF"] for r in RULES.values()) / total_rules, 2) if total_rules > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>📘</h3>
            <h2>{total_rules}</h2>
            <p>Jumlah Knowledge Base</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>🩺</h3>
            <h2>{total_history}</h2>
            <p>Jumlah Diagnosa</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>📊</h3>
            <h2>{avg_cf}</h2>
            <p>Rata-rata CF</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# MENU: DIAGNOSA
# ============================================================
if st.session_state.menu == "diagnosa":
    st.markdown('<h2 class="page-title">🩺 Diagnosa Kerusakan AC Split</h2>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Pilih gejala yang kamu alami untuk menemukan kemungkinan kerusakan.</p>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, (kode, nama) in enumerate(SYMPTOMS.items()):
        with cols[i % 2]:
            is_selected = kode in st.session_state.selected_symptoms
            label = f"✅ {nama}" if is_selected else nama
            if st.button(label, key=kode, use_container_width=True,
                         type="primary" if is_selected else "secondary"):
                if is_selected:
                    st.session_state.selected_symptoms.remove(kode)
                else:
                    st.session_state.selected_symptoms.append(kode)
                st.rerun()

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Mulai Diagnosis", use_container_width=True, type="primary"):
            if not st.session_state.selected_symptoms:
                st.warning("❗ Pilih minimal satu gejala terlebih dahulu.")
            else:
                st.info("🔍 Menganalisis gejala...")
                time.sleep(1)
                hasil = []
                for rid, rule in RULES.items():
                    if all(k in st.session_state.selected_symptoms for k in rule["IF"]):
                        hasil.append(rule["THEN"])
                st.session_state.result = list(set(hasil))
                save_history(st.session_state.selected_symptoms, st.session_state.result)
                st.success("✅ Diagnosis selesai & tersimpan ke riwayat!")
                st.rerun()
    with col2:
        if st.button("Reset", use_container_width=True):
            st.session_state.selected_symptoms = []
            st.session_state.result = None
            st.rerun()

    if st.session_state.result:
        st.markdown("### 🔎 Hasil Diagnosis")
        for kode in st.session_state.result:
            kerusakan = KERUSAKAN[kode]
            solusi = SOLUSI.get(kode, {})
            st.markdown(f"""
            <div class="result-card">
                <h4>{kerusakan['nama']}</h4>
                <p><b>Deskripsi:</b> {kerusakan['deskripsi']}</p>
                <p><b>Tingkat Kesulitan:</b> {kerusakan['tingkat_kesulitan'].title()}</p>
                <p><b>Rekomendasi Teknisi:</b> {kerusakan['rekomendasi_teknisi'].title()}</p>
                <h5>Langkah Perbaikan:</h5>
                <ul>
                    {''.join(f'<li>{s}</li>' for s in solusi.get('langkah_perbaikan', []))}
                </ul>
                <p class="peringatan"><b>⚠️ Peringatan:</b> {solusi.get('peringatan', '-')}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# MENU: KNOWLEDGE BASE
# ============================================================
elif st.session_state.menu == "knowledge":
    st.markdown('<h2 class="page-title">📘 Knowledge Base</h2>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Aturan dan hubungan antara gejala dan jenis kerusakan.</p>', unsafe_allow_html=True)
    for rid, rule in RULES.items():
        then_code = rule["THEN"]
        ker = KERUSAKAN.get(then_code, {})
        st.markdown(f"""
        <div class="rule-card">
            <h4>Rule {rid}</h4>
            <p><b>IF:</b> {', '.join(rule['IF'])}</p>
            <p><b>THEN:</b> {ker.get('nama', then_code)}</p>
            <p><b>CF:</b> {rule['CF']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# MENU: RIWAYAT
# ============================================================
elif st.session_state.menu == "history":
    # Jika belum memilih detail
    if st.session_state.selected_history is None:
        st.markdown('<h2 class="page-title">🕓 Riwayat Diagnosa</h2>', unsafe_allow_html=True)
        st.markdown('<p class="page-subtitle">Daftar diagnosis yang telah dilakukan.</p>', unsafe_allow_html=True)

        history = load_history()
        if not history:
            st.info("Belum ada riwayat diagnosis yang tersimpan 💾")
        else:
            for item in reversed(history[-20:]):
                with st.container():
                    cols = st.columns([4, 1])
                    with cols[0]:
                        st.markdown(f"""
                        <div class="history-card">
                            <div class="history-header">
                                <span>{item['timestamp']}</span>
                                <b>Diagnosis #{item['id']}</b>
                            </div>
                            <div class="tag-container">
                                {''.join(f'<span class="tag">{SYMPTOMS.get(g, g)}</span>' for g in item['symptoms'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with cols[1]:
                        if st.button("Lihat Detail", key=item['id'], use_container_width=True):
                            st.session_state.selected_history = item
                            st.rerun()

    # Jika sudah klik "Lihat Detail"
    else:
        detail = st.session_state.selected_history
        st.markdown(f"<h2 class='page-title'>🧾 Detail Diagnosis #{detail['id']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='page-subtitle'>Tanggal: {detail['timestamp']}</p>", unsafe_allow_html=True)

        st.write("**Gejala yang Dipilih:** " + ", ".join(SYMPTOMS.get(g, g) for g in detail['symptoms']))

        for kode in detail['result']:
            kerusakan = KERUSAKAN[kode]
            solusi = SOLUSI.get(kode, {})
            st.markdown(f"""
            <div class="result-card">
                <h4>{kerusakan['nama']}</h4>
                <p><b>Deskripsi:</b> {kerusakan['deskripsi']}</p>
                <p><b>Tingkat Kesulitan:</b> {kerusakan['tingkat_kesulitan'].title()}</p>
                <p><b>Rekomendasi Teknisi:</b> {kerusakan['rekomendasi_teknisi'].title()}</p>
                <h5>Langkah Perbaikan:</h5>
                <ul>
                    {''.join(f'<li>{s}</li>' for s in solusi.get('langkah_perbaikan', []))}
                </ul>
                <p class="peringatan"><b>⚠️ Peringatan:</b> {solusi.get('peringatan', '-')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Kembali ke Daftar Riwayat", use_container_width=True, type="secondary"):
            st.session_state.selected_history = None
            st.rerun()
