# reporting.py
def simpan_hasil(gejala, hasil):
    with open("riwayat.txt", "a", encoding="utf-8") as file:
        file.write(f"Gejala: {gejala} -> Hasil: {hasil}\n")