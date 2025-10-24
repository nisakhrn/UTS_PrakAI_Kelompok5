# inference_engine.py
from knowledge_base import load_knowledge_base, get_rules
from working_memory import WorkingMemory  # NEW
import json

def validate_facts_consistency(user_facts, list_gejala, working_memory):
    """Validasi konsistensi fakta dari user"""
    gejala_dict = {g['kode']: g for g in list_gejala}
    valid_facts = user_facts.copy()
    removed_facts = []
    
    for fact in user_facts:
        base_fact = fact.split('::')[0]
        gejala_data = gejala_dict.get(base_fact, {})
        excludes_list = gejala_data.get('excludes', [])
        
        for excluded_fact in excludes_list:
            if excluded_fact in valid_facts:
                if fact in valid_facts:
                    valid_facts.remove(fact)
                    removed_facts.append((fact, excluded_fact))
                    working_memory.log_reasoning(f"⚠️ Fact '{fact}' removed - conflicts with '{excluded_fact}'")
                break
    
    for removed, conflicting in removed_facts:
        print(f"⚠️  Peringatan: Gejala '{removed}' dikeluarkan karena bertentangan dengan '{conflicting}'")
    
    return valid_facts

def run_forward_chaining(working_memory, all_rules, kb=None):
    """Menjalankan inference engine menggunakan Working Memory"""
    
    known_facts = working_memory.get_facts()
    working_memory.log_reasoning("--- Forward Chaining Started ---")
    working_memory.log_reasoning(f"Initial Facts: {list(known_facts)}")
    
    for rule_code, rule_data in all_rules.items():
        required_facts = set(rule_data['IF'])
        
        working_memory.log_reasoning(f"[Checking Rule {rule_code}]")
        working_memory.log_reasoning(f"Rule: IF {list(required_facts)} THEN {rule_data['THEN']}")
        
        if known_facts.issuperset(required_facts):
            conclusion = rule_data['THEN']
            confidence = rule_data.get('CF', 1.0)
            
            result = {
                'diagnosis': conclusion,
                'confidence': confidence,
                'rule_used': rule_code,
                'based_on_facts': list(required_facts)
            }
            working_memory.add_conclusion(result)
            
            working_memory.log_reasoning(f"✅ RULE FIRED: {rule_code}")
            working_memory.log_reasoning(f"Conclusion: {conclusion} (CF: {confidence})")
        else:
            missing_facts = required_facts - known_facts
            working_memory.log_reasoning(f"❌ RULE FAILED: Missing facts {list(missing_facts)}")
    
    working_memory.log_reasoning("--- Forward Chaining Completed ---")
    
    # Apply exclusions
    if kb and 'kerusakan' in kb:
        working_memory.conclusions = check_exclusions(working_memory.conclusions, 
                                                    {k['kode']: k for k in kb['kerusakan']})
    
    # Sort by confidence
    working_memory.conclusions.sort(key=lambda x: x['confidence'], reverse=True)
    
    return working_memory

def check_exclusions(conclusions, all_kerusakan):
    """Memeriksa dan menghapus kesimpulan yang saling eksklusif"""
    valid_conclusions = []
    
    for conclusion in conclusions:
        kode_kerusakan = conclusion['diagnosis']
        kerusakan_data = all_kerusakan.get(kode_kerusakan, {})
        excludes_list = kerusakan_data.get('excludes', [])
        
        has_conflict = False
        for valid_conc in valid_conclusions:
            if valid_conc['diagnosis'] in excludes_list:
                has_conflict = True
                break
        
        if not has_conflict:
            valid_conclusions.append(conclusion)
    
    return valid_conclusions

if __name__ == "__main__":
    print("Memuat Knowledge Base...")
    kb = load_knowledge_base()
    
    if not kb:
        print("Gagal memuat knowledge base. Program berhenti.")
    else:
        # Initialize Working Memory
        wm = WorkingMemory()
        
        list_gejala = kb.get('gejala', [])
        all_rules = kb.get('rules', {})
        all_kerusakan = {k['kode']: k for k in kb.get('kerusakan', [])}
        
        if not list_gejala or not all_rules:
            print("Knowledge base tidak lengkap.")
        else:
            print("--- Selamat Datang di Sistem Pakar Diagnosis AC ---")
            
            user_facts = [] 
            
            # Collect user input
            for gejala in list_gejala:
                kode = gejala['kode']
                pertanyaan = gejala['pertanyaan']
                tipe = gejala.get('tipe', 'boolean') 

                if tipe == 'boolean':
                    jawaban = input(f"\n(?) {pertanyaan} (y/n): ").strip().lower()
                    if jawaban == 'y':
                        user_facts.append(kode)
                        wm.add_fact(kode)  # Add to working memory
                
                elif tipe == 'multiple_choice':
                    print(f"\n(?) {pertanyaan}")
                    opsi_list = gejala.get('opsi', [])
                    for i, opsi in enumerate(opsi_list):
                        print(f"  {i+1}. {opsi}")
                    
                    jawaban_angka = int(input(f"  Pilih nomor (1-{len(opsi_list)}): "))
                    
                    if jawaban_angka > 0:
                        pilihan_terpilih = opsi_list[jawaban_angka - 1]
                        if pilihan_terpilih != "tidak ada bau":
                            fact_code = f"{kode}::{pilihan_terpilih}"
                            user_facts.append(fact_code)
                            wm.add_fact(fact_code)  # Add to working memory

            print("\n--- Validasi Konsistensi Fakta ---")
            validated_facts = validate_facts_consistency(user_facts, list_gejala, wm)
            
            # Update working memory dengan fakta yang sudah divalidasi
            wm.facts = set(validated_facts)
            
            print("\n--- Proses Inferensi Dimulai ---")
            wm = run_forward_chaining(wm, all_rules, kb)
            
            # Tampilkan Working Memory status
            wm.display_status()
            
            # Save working memory untuk analisis
            wm.save_to_file()
            print(f"Working Memory disimpan di: wm_{wm.session_id}.json")
            
            print("\n--- HASIL DIAGNOSIS ---")
            if wm.conclusions:
                for i, conclusion in enumerate(wm.conclusions, 1):
                    kode_kerusakan = conclusion['diagnosis']
                    kerusakan_info = all_kerusakan.get(kode_kerusakan, {})
                    nama_kerusakan = kerusakan_info.get('nama', 'Tidak diketahui')
                    
                    print(f"\n{i}. {nama_kerusakan} (Keyakinan: {conclusion['confidence']*100:.1f}%)")
                    print(f"   Aturan: {conclusion['rule_used']}")
                
                best = wm.conclusions[0]
                best_info = all_kerusakan.get(best['diagnosis'], {})
                print(f"\n🎯 DIAGNOSIS UTAMA: {best_info.get('nama', best['diagnosis'])}")
                
            else:
                print("Tidak ada diagnosis yang dapat disimpulkan.")