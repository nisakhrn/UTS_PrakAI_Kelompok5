# working_memory.py
# Working Memory untuk menyimpan fakta sementara

from datetime import datetime

class WorkingMemory:
    """
    Working Memory untuk menyimpan:
    - Fakta sementara dari user input
    - Hasil inferensi intermediate
    - Session data
    """
    
    def __init__(self):
        self.facts = []  # Fakta gejala yang dialami
        self.user_cf = {}  # CF untuk setiap fakta dari user
        self.intermediate_results = {}  # Hasil inferensi sementara
        self.session_data = {
            'start_time': None,
            'user_info': {},
            'consultation_id': None
        }
        self.history = []  # Riwayat perubahan
    
    def start_session(self, consultation_id=None, user_info=None):
        """Mulai session baru"""
        self.clear_all()
        self.session_data['start_time'] = datetime.now()
        self.session_data['consultation_id'] = consultation_id or self._generate_consultation_id()
        self.session_data['user_info'] = user_info or {}
        
        self._add_history('session_started', {
            'consultation_id': self.session_data['consultation_id'],
            'time': self.session_data['start_time']
        })
    
    def add_fact(self, symptom_id, cf_value=1.0):
        """
        Tambah fakta gejala
        
        Args:
            symptom_id: ID gejala
            cf_value: Certainty Factor dari user (0 to 1)
        """
        if symptom_id not in self.facts:
            self.facts.append(symptom_id)
            self.user_cf[symptom_id] = cf_value
            
            self._add_history('fact_added', {
                'symptom_id': symptom_id,
                'cf_value': cf_value
            })
            return True
        return False
    
    def remove_fact(self, symptom_id):
        """Hapus fakta gejala"""
        if symptom_id in self.facts:
            self.facts.remove(symptom_id)
            if symptom_id in self.user_cf:
                del self.user_cf[symptom_id]
            
            self._add_history('fact_removed', {
                'symptom_id': symptom_id
            })
            return True
        return False
    
    def update_cf(self, symptom_id, new_cf):
        """Update CF untuk gejala tertentu"""
        if symptom_id in self.facts:
            old_cf = self.user_cf.get(symptom_id, 1.0)
            self.user_cf[symptom_id] = new_cf
            
            self._add_history('cf_updated', {
                'symptom_id': symptom_id,
                'old_cf': old_cf,
                'new_cf': new_cf
            })
            return True
        return False
    
    def get_facts(self):
        """Ambil semua fakta"""
        return self.facts.copy()
    
    def get_user_cf(self):
        """Ambil CF user untuk semua fakta"""
        return self.user_cf.copy()
    
    def add_intermediate_result(self, key, value):
        """Simpan hasil inferensi intermediate"""
        self.intermediate_results[key] = {
            'value': value,
            'timestamp': datetime.now()
        }
        
        self._add_history('intermediate_result', {
            'key': key,
            'value': value
        })
    
    def get_intermediate_result(self, key):
        """Ambil hasil intermediate"""
        return self.intermediate_results.get(key, {}).get('value')
    
    def clear_facts(self):
        """Bersihkan semua fakta"""
        self.facts = []
        self.user_cf = {}
        self._add_history('facts_cleared', {})
    
    def clear_intermediate(self):
        """Bersihkan hasil intermediate"""
        self.intermediate_results = {}
        self._add_history('intermediate_cleared', {})
    
    def clear_all(self):
        """Bersihkan semua data"""
        self.facts = []
        self.user_cf = {}
        self.intermediate_results = {}
        self.history = []
    
    def get_session_info(self):
        """Ambil informasi session"""
        return self.session_data.copy()
    
    def get_history(self):
        """Ambil riwayat perubahan"""
        return self.history.copy()
    
    def get_state_summary(self):
        """Ambil ringkasan state working memory"""
        return {
            'total_facts': len(self.facts),
            'facts': self.facts,
            'user_cf': self.user_cf,
            'intermediate_results_count': len(self.intermediate_results),
            'session_id': self.session_data['consultation_id'],
            'session_duration': self._get_session_duration()
        }
    
    def _add_history(self, action, data):
        """Catat history perubahan"""
        self.history.append({
            'action': action,
            'data': data,
            'timestamp': datetime.now()
        })
    
    def _generate_consultation_id(self):
        """Generate ID konsultasi unik"""
        return f"CONS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _get_session_duration(self):
        """Hitung durasi session"""
        if self.session_data['start_time']:
            duration = datetime.now() - self.session_data['start_time']
            return duration.total_seconds()
        return 0
    
    def export_state(self):
        """Export state untuk penyimpanan"""
        return {
            'facts': self.facts,
            'user_cf': self.user_cf,
            'intermediate_results': self.intermediate_results,
            'session_data': {
                'consultation_id': self.session_data['consultation_id'],
                'start_time': self.session_data['start_time'].isoformat() if self.session_data['start_time'] else None,
                'user_info': self.session_data['user_info']
            },
            'history': [
                {
                    'action': h['action'],
                    'data': h['data'],
                    'timestamp': h['timestamp'].isoformat()
                } for h in self.history
            ]
        }
