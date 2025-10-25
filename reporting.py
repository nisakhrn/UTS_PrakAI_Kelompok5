import json
from datetime import datetime

def simpan_riwayat(gejala, hasil):
    """Simpan hasil diagnosa ke file riwayat.txt"""
    data = {
        "tanggal": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "gejala": gejala,
        "hasil": hasil
    }
    try:
        with open("riwayat.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception as e:
        print("⚠️ Gagal menyimpan riwayat:", e)

def load_riwayat():
    """Membaca semua riwayat yang sudah tersimpan"""
    try:
        with open("riwayat.txt", "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []
