def hitung_cf(cf_rule, cf_user):
    """Menghitung Certainty Factor gabungan"""
    return round(cf_rule * cf_user, 2)


def calculate_cf(evidence_list, rules):
    """
    Menghitung nilai Certainty Factor (CF) berdasarkan evidence user & rule base.
    """
    cf_result = {}
    reasoning_trace = {}

    for rule_id, rule in rules.items():
        kondisi = rule["IF"]
        kesimpulan = rule["THEN"]
        cf_rule = rule.get("CF", 1.0)

        # Cek apakah semua kondisi rule terpenuhi oleh input user
        if all(gejala in evidence_list for gejala in kondisi):
            cf_user = 1.0  # anggap user yakin 100%
            cf_new = hitung_cf(cf_rule, cf_user)

            # Hitung CF gabungan jika kesimpulan sudah ada sebelumnya
            if kesimpulan in cf_result:
                cf_result[kesimpulan] = round(
                    cf_result[kesimpulan] + cf_new * (1 - cf_result[kesimpulan]), 3
                )
            else:
                cf_result[kesimpulan] = round(cf_new, 3)

            # Simpan reasoning trace (alur penalaran)
            if kesimpulan not in reasoning_trace:
                reasoning_trace[kesimpulan] = []
            reasoning_trace[kesimpulan].append(
                f"Rule {rule_id}: IF {' AND '.join(kondisi)} THEN {kesimpulan}"
            )

    # Urutkan hasil CF dari terbesar ke terkecil
    sorted_result = dict(sorted(cf_result.items(), key=lambda x: x[1], reverse=True))

    return sorted_result, reasoning_trace
