# knowledge_base.py

def load_knowledge_base(file_path="knowledge_base.json"):
    """
    Membaca file knowledgebase.json secara utuh.
    Mengembalikan seluruh data (gejala, kerusakan, rules, dll.)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except FileNotFoundError:
        print(f"⚠️ File '{file_path}' tidak ditemukan.")
        return None
    except json.JSONDecodeError:
        print(f"⚠️ Gagal mem-parsing '{file_path}'. File mungkin rusak.")
        return None

def get_rules():
    """
    Fungsi spesifik untuk mengambil 'rules' saja.
    Ini tetap dipertahankan agar inference_engine lama tetap berfungsi.
    """
    data = load_knowledge_base()
    if data and 'rules' in data:
        return data['rules']
    
    # Fallback jika file/key tidak ada
    print("⚠️ Gagal memuat aturan. Menggunakan aturan default...")
    return {
        "R1": {"IF": ["ac_tidak_dingin"], "THEN": "kerusakan_kompresor"},
        "R2": {"IF": ["ac_bocor_air"], "THEN": "saluran_drainase_tersumbat"}
    }

# --- CONTOH PENGGUNAAN ---
if __name__ == "__main__":
    # Tes cepat untuk memastikan file bisa dibaca
    print("--- Menjalankan Tes Cepat knowledge_base.py ---")
    
    kb_data = load_knowledge_base()
    
    if kb_data:
        print(f"✅ Berhasil memuat knowledgebase.json.")
        print(f"  -> Ditemukan {len(kb_data.get('gejala', []))} gejala.")
        print(f"  -> Ditemukan {len(kb_data.get('kerusakan', []))} kerusakan.")
        print(f"  -> Ditemukan {len(kb_data.get('rules', {}))} aturan.")
        
        # Tes get_rules()
        aturan = get_rules()
        print(f"\n✅ Tes get_rules() berhasil, memuat {len(aturan)} aturan.")
    else:
        print("❌ Gagal memuat knowledgebase.json.")
