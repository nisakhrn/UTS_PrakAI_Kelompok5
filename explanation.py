from acquisition import rules

# === FUNGSI WHY ===
def explain_why(gejala):
    found = False
    for rule in rules:
        if gejala in rule["if"]:
            print(f"\n WHY: Mengapa sistem menanyakan '{gejala}' ?")
            print(f"Karena gejala ini dibutuhkan untuk menentukan apakah {rule['then']}.\n")
            found = True
            break
    if not found:
        print(f"\nSistem tidak memiliki alasan khusus untuk gejala '{gejala}'.\n")

# === FUNGSI HOW ===
def explain_how(gejala_input):
    cocok = []
    gejala_input = [g.strip().lower() for g in gejala_input]

    for rule in rules:
        if all(g in gejala_input for g in rule["if"]):
            cocok.append(rule)

    if cocok:
        print("\n HOW: Bagaimana hasil diagnosis diperoleh:")
        for rule in cocok:
            print(f"- Karena gejala {rule['if']}, maka {rule['then']}.")
            print(f"  Penjelasan: {rule['explanation']}\n")
    else:
        print("\nTidak ditemukan rule yang cocok dengan gejala tersebut.\n")

# === MENU UTAMA ===
def menu_explanation_facility():
    while True:
        print("\n=== EXPLANATION FACILITY MENU ===")
        print("1. WHY (Mengapa gejala ini ditanyakan)")
        print("2. HOW (Bagaimana hasil diagnosis diperoleh)")
        print("0. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            gejala = input("Masukkan gejala yang ingin ditanyakan (contoh: ac tidak dingin): ").lower().strip()
            explain_why(gejala)
        elif pilih == "2":
            gejala_input = input("Masukkan daftar gejala (pisahkan dengan koma): ").lower().split(",")
            explain_how(gejala_input)
        elif pilih == "0":
            print("Keluar dari Explanation Facility...")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

# === JALANKAN PROGRAM ===
if __name__ == "__main__":
    menu_explanation_facility()
