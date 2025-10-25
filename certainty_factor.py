# certainty_factor.py
def hitung_cf(cf_rule, cf_user):
    """Menghitung Certainty Factor gabungan"""
    return round(cf_rule * cf_user, 2)