# knowledge_base.py
import json

def load_knowledge_base(file_path="knowledge_base.json"):
    """
    Membaca file knowledge_base.json secara utuh.
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
    Mengambil bagian 'rules' dari knowledge base.
    Jika file tidak ditemukan atau rusak, gunakan aturan default.
    """
    data = load_knowledge_base()
    if data and 'rules' in data:
        return data['rules']

    print("⚠️ Gagal memuat aturan. Menggunakan aturan default...")
    return {
        "R1": {"IF": ["ac_tidak_dingin", "kompresor_tidak_berbunyi"], "THEN": "kerusakan_kompresor"},
        "R2": {"IF": ["ac_bocor_air"], "THEN": "saluran_drainase_tersumbat"}
    }


# --- CONTOH PENGGUNAAN ---
if __name__ == "__main__":
    print("--- Menjalankan Tes Cepat knowledge_base.py ---")

    kb_data = load_knowledge_base()

    if kb_data:
        print("✅ Berhasil memuat knowledge_base.json.")
        print(f"  -> Ditemukan {len(kb_data.get('gejala', []))} gejala.")
        print(f"  -> Ditemukan {len(kb_data.get('kerusakan', []))} kerusakan.")
        print(f"  -> Ditemukan {len(kb_data.get('rules', {}))} aturan.")

        aturan = get_rules()
        print(f"\n✅ Tes get_rules() berhasil, memuat {len(aturan)} aturan.")
    else:
        print("❌ Gagal memuat knowledge_base.json.")