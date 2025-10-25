"""
Sistem Pakar Diagnosis AC Split Residensial - Premium UI
Author: Your Name
"""

import streamlit as st
from datetime import datetime
import time

# Import modul-modul yang sudah ada
try:
    from knowledge_base import get_rules
    from inference_engine import infer
    from working_memory import add_fact, get_memory, reset_memory
    from explanation_facility import explain
    from reporting import simpan_hasil
    from search_filter import cari_riwayat
    MODULES_LOADED = True
except ImportError as e:
    st.error(f"⚠️ Error loading modules: {e}")
    MODULES_LOADED = False

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="AC Expert System",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PREMIUM CSS STYLING ====================
# PERUBAHAN 1: Fungsi untuk load file CSS eksternal
def load_premium_css(file_name="style.css"):
    """Membaca file CSS eksternal dan meng-inject-nya ke Streamlit."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ File CSS '{file_name}' tidak ditemukan. Pastikan file ada di folder yang sama.")

# Panggil fungsinya
load_premium_css()

# ==================== DATA GEJALA ====================
GEJALA_DATA = {
    "ac_tidak_dingin": {
        "label": "❄️ AC Tidak Dingin",
        "deskripsi": "AC menyala tapi udara yang keluar tidak dingin",
        "icon": "❄️"
    },
    "kompresor_tidak_berbunyi": {
        "label": "🔇 Kompresor Tidak Berbunyi",
        "deskripsi": "Kompresor tidak mengeluarkan suara saat AC menyala",
        "icon": "🔇"
    },
    "ac_bocor_air": {
        "label": "💧 AC Bocor Air",
        "deskripsi": "Ada air yang menetes dari unit indoor AC",
        "icon": "💧"
    },
    "ac_mengeluarkan_bau_tidak_sedap": {
        "label": "👃 AC Berbau Tidak Sedap",
        "deskripsi": "AC mengeluarkan bau tidak enak saat dinyalakan",
        "icon": "👃"
    },
    "ac_tidak_menyala": {
        "label": "⚡ AC Tidak Menyala",
        "deskripsi": "AC sama sekali tidak bisa dinyalakan",
        "icon": "⚡"
    },
    "arus_kompresor_tinggi": {
        "label": "📊 Arus Kompresor Tinggi",
        "deskripsi": "Kompresor mengonsumsi arus listrik berlebih",
        "icon": "📊"
    },
    "tegangan_abnormal": {
        "label": "⚠️ Tegangan Abnormal",
        "deskripsi": "Tegangan listrik tidak sesuai standar",
        "icon": "⚠️"
    },
    "evaporator_tersumbat": {
        "label": "🚫 Evaporator Tersumbat",
        "deskripsi": "Evaporator kotor atau tersumbat",
        "icon": "🚫"
    },
    "tegangan_listrik_tidak_stabil": {
        "label": "⚡ Tegangan Listrik Tidak Stabil",
        "deskripsi": "Listrik naik-turun tidak stabil",
        "icon": "⚡"
    }
}

# ==================== HERO HEADER ====================
st.markdown("""
    <div class="hero-header">
        <h1>❄️ AC Expert System</h1>
        <p>Diagnosis Pintar untuk AC Anda dengan Teknologi AI</p>
        <span class="hero-badge">🚀 Powered by Forward Chaining</span>
    </div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.markdown("## 🧭 Navigasi")
    menu = st.radio(
        "",
        ["🔍 Diagnosa", "📘 Basis Pengetahuan", "📁 Riwayat Diagnosis"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
        ### ℹ️ Tentang Sistem
        
        Sistem pakar ini menggunakan metode **Forward Chaining** untuk diagnosis otomatis.
        
        **✨ Fitur Unggulan:**
        - 🎯 Akurasi Tinggi
        - ⚡ Diagnosis Cepat
        - 📊 Analisis Detail
        - 💾 Riwayat Tersimpan
        - 🔍 Pencarian Mudah
    """)
    
    st.markdown("---")
    st.markdown(f"### 📅 {datetime.now().strftime('%d %B %Y')}")
    st.markdown(f"### 🕐 {datetime.now().strftime('%H:%M:%S')}")

# ==================== MENU: DIAGNOSA ====================
if menu == "🔍 Diagnosa":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🩺 Pilih Gejala</h2>', unsafe_allow_html=True)
        
        gejala_options = list(GEJALA_DATA.keys())
        gejala_labels = [GEJALA_DATA[g]["label"] for g in gejala_options]
        
        selected_labels = st.multiselect(
            "Pilih semua gejala yang Anda alami:",
            gejala_labels,
            help="💡 Pilih minimal 1 gejala untuk memulai diagnosis"
        )
        
        gejala_input = [
            key for key, data in GEJALA_DATA.items() 
            if data["label"] in selected_labels
        ]
        
        if gejala_input:
            # PERUBAHAN 2: Ganti inline style dengan CSS class
            st.markdown(f"""
                <div class="selected-count-box">
                    <h4>✅ {len(gejala_input)} Gejala Terpilih</h4>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📋 Lihat Detail Gejala", expanded=False):
                for g in gejala_input:
                    st.markdown(f"""
                        <div class="symptom-pill">
                            {GEJALA_DATA[g]['icon']} {GEJALA_DATA[g]['label']}
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        diagnosa_btn = st.button("🔍 MULAI DIAGNOSIS", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">💡 Panduan</h2>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-box">
                <h4>📝 Cara Menggunakan:</h4>
                <ol style="margin: 0; padding-left: 1.5rem;">
                    <li><strong>Pilih gejala</strong> yang sesuai</li>
                    <li><strong>Klik tombol</strong> diagnosis</li>
                    <li><strong>Baca hasil</strong> analisis</li>
                    <li><strong>Ikuti</strong> rekomendasi</li>
                </ol>
            </div>
            
            <div class="info-box" style="background: linear-gradient(135deg, #fff9e6 0%, #fff3d1 100%); border-left-color: #f39c12;">
                <h4 style="color: #d68910;">⚡ Tips Pro:</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Pilih <strong>semua gejala</strong> yang relevan</li>
                    <li>Semakin <strong>detail</strong>, hasil lebih akurat</li>
                    <li>Periksa AC sebelum diagnosis</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proses Diagnosis
    if diagnosa_btn:
        if not gejala_input:
            st.error("❌ **Silakan pilih minimal 1 gejala!**")
        elif not MODULES_LOADED:
            st.error("❌ **Modul sistem tidak dapat dimuat!**")
        else:
            with st.spinner("🔄 Menganalisis gejala Anda..."):
                time.sleep(1.5)  # Simulasi loading
                reset_memory()
                for gejala in gejala_input:
                    add_fact(gejala)
                
                rules = get_rules()
                hasil = infer(get_memory(), rules)
            
            st.markdown("---")
            st.markdown('<h2 class="section-header">📋 Hasil Diagnosis</h2>', unsafe_allow_html=True)
            
            if hasil:
                st.balloons()
                
                for idx, diagnosis in enumerate(hasil, 1):
                    st.markdown(f"""
                        <div class="result-card">
                            <h3>🎯 Diagnosis #{idx}: {diagnosis.replace('_', ' ').title()}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    for rule_code, rule in rules.items():
                        if rule.get("THEN") == diagnosis:
                            penjelasan = explain(rule)
                            st.info(f"📝 **Penjelasan Lengkap:**\n\n{penjelasan}")
                            
                            with st.expander("🔍 Detail Teknis", expanded=False):
                                st.markdown(f"**Kode Rule:** `{rule_code}`")
                                st.markdown("**Kondisi Terpenuhi:**")
                                for kondisi in rule.get("IF", []):
                                    if kondisi in GEJALA_DATA:
                                        st.markdown(f"✓ {GEJALA_DATA[kondisi]['label']}")
                                    else:
                                        st.markdown(f"✓ {kondisi.replace('_', ' ').title()}")
                            break
                    
                    simpan_hasil(gejala_input, diagnosis)
                
                st.success("✅ **Diagnosis berhasil disimpan ke riwayat!**")
                
            else:
                st.warning("""
                    ### ⚠️ Tidak Ditemukan Diagnosis
                    
                    **Kemungkinan:**
                    - Kombinasi gejala tidak ada dalam database
                    - Perlu pemeriksaan teknisi profesional
                    
                    **Rekomendasi:**
                    - Tambahkan gejala lain yang lebih spesifik
                    - Hubungi teknisi AC bersertifikat
                """)

# ==================== MENU: BASIS PENGETAHUAN ====================
elif menu == "📘 Basis Pengetahuan":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">📚 Knowledge Base Rules</h2>', unsafe_allow_html=True)
    
    if not MODULES_LOADED:
        st.error("❌ Tidak dapat memuat basis pengetahuan.")
    else:
        rules = get_rules()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📜 Total Rules", len(rules))
        with col2:
            total_kondisi = sum(len(rule.get("IF", [])) for rule in rules.values())
            st.metric("📊 Total Kondisi", total_kondisi)
        with col3:
            unique_diagnosis = len(set(rule.get("THEN", "") for rule in rules.values()))
            st.metric("🎯 Jenis Diagnosis", unique_diagnosis)
        
        st.markdown("---")
        
        for rule_code, rule in rules.items():
            with st.expander(f"📌 **{rule_code}**: {rule.get('THEN', '').replace('_', ' ').title()}", expanded=False):
                st.markdown("**IF (Kondisi):**")
                for kondisi in rule.get("IF", []):
                    st.markdown(f"- ✓ `{kondisi}`")
                
                st.markdown(f"**THEN (Kesimpulan):**")
                st.success(f"→ **{rule.get('THEN', '').replace('_', ' ').title()}**")
                
                try:
                    penjelasan = explain(rule)
                    st.info(f"💡 {penjelasan}")
                except:
                    pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== MENU: RIWAYAT ====================
elif menu == "📁 Riwayat Diagnosis":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🔎 Pencarian Riwayat</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        kata_kunci = st.text_input(
            "🔍 Masukkan kata kunci:",
            placeholder="Contoh: bocor, kompresor, tidak dingin...",
            help="Cari dalam riwayat diagnosis"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        cari_btn = st.button("🔍 CARI", use_container_width=True)
    
    if kata_kunci and cari_btn:
        if not MODULES_LOADED:
            st.error("❌ Modul pencarian tidak tersedia.")
        else:
            with st.spinner("🔄 Mencari riwayat..."):
                time.sleep(0.8)
                hasil = cari_riwayat(kata_kunci)
            
            st.markdown("---")
            
            if hasil:
                st.success(f"✅ Ditemukan **{len(hasil)} hasil** untuk: *'{kata_kunci}'*")
                
                for idx, record in enumerate(hasil, 1):
                    with st.expander(f"📄 Riwayat #{idx} - {record[:50]}...", expanded=(idx <= 3)):
                        st.code(record, language="text")
            else:
                st.warning(f"⚠️ Tidak ditemukan riwayat dengan kata kunci: **'{kata_kunci}'**")
    
    elif not kata_kunci and cari_btn:
        st.warning("⚠️ Silakan masukkan kata kunci!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PREMIUM FOOTER ====================
st.markdown("""
    <div class="premium-footer">
        <h3>❄️ AC Expert System</h3>
        <p><strong>Sistem Pakar Diagnosis AC Split Residensial</strong></p>
        <p>Menggunakan Forward Chaining AI • Akurat & Cepat</p>
        <p style="margin-top: 1rem; color: #999; font-size: 0.9rem;">
            © 2024 • Hak Cipta Kelompok 5
        </p>
    </div>
""", unsafe_allow_html=True)