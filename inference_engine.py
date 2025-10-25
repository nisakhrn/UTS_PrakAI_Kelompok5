# inference_engine.py
def infer(gejala_input, rules):
    hasil = []
    for kode, rule in rules.items():
        if all(g in gejala_input for g in rule["IF"]):
            hasil.append(rule["THEN"])
    return hasil