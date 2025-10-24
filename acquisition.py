# ==============================================
# Knowledge Acquisition (Tambah/Edit/Hapus Rule)
# ==============================================

# Basis Pengetahuan awal (contoh)
rules = [
    {
        "jika": ["ac tidak dingin", "kompresor tidak bunyi"],
        "maka": "freon habis atau kompresor rusak",
        "explanation": "Jika AC tidak dingin dan kompresor tidak bunyi, kemungkinan freon bocor atau kompresor rusak."
    },
    {
        "jika": ["unit indoor bocor air"],
        "maka": "saluran pembuangan tersumbat",
        "explanation": "Biasanya air bocor karena saluran pembuangan tersumbat oleh debu atau lendir."
    }
]


# --- Menampilkan Semua Rule ---
def tampil_rules():
    print("\nDaftar Rules Saat Ini:")
    if not rules:
        print("(Belum ada aturan di sistem.)")
    else:
        for i, rule in enumerate(rules, start=1):
            print(f"{i}. Jika {rule['jika']} Maka {rule['maka']}")
    print()


# --- Menambah Rule ---
def tambah_rule():
    print("\n=== Tambah Rule Baru ===")
    kondisi = input("Masukkan kondisi (pisahkan dengan koma): ").lower().split(",")
    kondisi = [k.strip() for k in kondisi]
    hasil = input("Masukkan hasil (maka): ").lower()
    penjelasan = input("Masukkan penjelasan: ")
    rules.append({"jika": kondisi, "maka": hasil, "explanation": penjelasan})
    print("Rule baru berhasil ditambahkan!")


# --- Mengedit Rule ---
def edit_rule():
    tampil_rules()
    if not rules:
        return
    try:
        idx = int(input("Masukkan nomor rule yang ingin diedit: ")) - 1
        if 0 <= idx < len(rules):
            print("Masukkan data baru (kosongkan jika tidak ingin diubah)")
            new_if = input("Kondisi baru (pisahkan dengan koma): ")
            new_then = input("Hasil baru: ")
            new_explanation = input("Penjelasan baru: ")

            if new_if:
                rules[idx]["jika"] = [x.strip() for x in new_if.split(",")]
            if new_then:
                rules[idx]["maka"] = new_then
            if new_explanation:
                rules[idx]["explanation"] = new_explanation
            print("Rule berhasil diperbarui!")
        else:
            print("Nomor rule tidak valid.")
    except ValueError:
        print("Masukkan angka yang valid.")


# --- Menghapus Rule ---
def hapus_rule():
    tampil_rules()
    if not rules:
        return
    try:
        idx = int(input("Masukkan nomor rule yang ingin dihapus: ")) - 1
        if 0 <= idx < len(rules):
            del rules[idx]
            print("Rule berhasil dihapus!")
        else:
            print("Nomor rule tidak valid.")
    except ValueError:
        print("Masukkan angka yang valid.")


# --- Antarmuka ---
def menu_knowledge_acquisition():
    while True:
        print("\n=== KNOWLEDGE ACQUISITION MENU ===")
        print("1. Tampilkan Semua Rule")
        print("2. Tambah Rule")
        print("3. Edit Rule")
        print("4. Hapus Rule")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampil_rules()
        elif pilihan == "2":
            tambah_rule()
        elif pilihan == "3":
            edit_rule()
        elif pilihan == "4":
            hapus_rule()
        elif pilihan == "0":
            print("Keluar dari KA...")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


# --- DEMO ---
if __name__ == "__main__":
    menu_knowledge_acquisition()
