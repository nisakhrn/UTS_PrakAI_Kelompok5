# knowledge_base.py
import json

def get_rules():
    try:
        with open("knowldge_base.json", "r", encoding="utf-8") as f:
            rules = json.load(f)
            return rules
    except FileNotFoundError:
        print("⚠️ File rules.json tidak ditemukan. Menggunakan aturan default...")
        return {
            "R1": {"IF": ["ac_tidak_dingin", "kompresor_tidak_berbunyi"], "THEN": "kerusakan_kompresor"},
            "R2": {"IF": ["ac_bocor_air"], "THEN": "saluran_drainase_tersumbat"}
        }

if __name__ == "__main__":
    import json
    print(json.dumps(get_rules(), indent=4, ensure_ascii=False))
