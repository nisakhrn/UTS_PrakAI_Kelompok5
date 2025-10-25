# explanation_facility.py
def explain(rule):
    return f"Rule digunakan: IF {' AND '.join(rule['IF'])} THEN {rule['THEN']}"