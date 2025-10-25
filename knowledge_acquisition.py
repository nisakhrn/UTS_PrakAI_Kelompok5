# knowledge_acquisition.py
import json

def tambah_rule(kode, gejala, hasil):
    try:
        with open("rules.json", "r", encoding="utf-8") as f:
            rules = json.load(f)
    except FileNotFoundError:
        rules = {}

    rules[kode] = {"IF": gejala, "THEN": hasil}

    with open("rules.json", "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=4, ensure_ascii=False)

    print(f"✅ Rule {kode} berhasil ditambahkan.")