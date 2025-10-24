# search_filter.py
def cari_riwayat(kata):
    hasil = []
    try:
        with open("riwayat.txt", "r", encoding="utf-8") as file:
            for line in file:
                if kata.lower() in line.lower():
                    hasil.append(line.strip())
    except FileNotFoundError:
        hasil.append("Belum ada riwayat tersimpan.")
    return hasil