# working_memory.py
import json
from datetime import datetime

class WorkingMemory:
    def __init__(self, session_id=None):
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.facts = set()  # Fakta yang diketahui
        self.conclusions = []  # Kesimpulan yang ditemukan
        self.reasoning_trace = []  # Jejak penalaran
        self.timestamp = datetime.now()
        
    def add_fact(self, fact):
        """Tambahkan fakta ke working memory"""
        self.facts.add(fact)
        self.reasoning_trace.append(f"[FACT ADDED] {fact}")
        
    def remove_fact(self, fact):
        """Hapus fakta dari working memory"""
        if fact in self.facts:
            self.facts.remove(fact)
            self.reasoning_trace.append(f"[FACT REMOVED] {fact}")
            
    def add_conclusion(self, conclusion):
        """Tambahkan kesimpulan"""
        self.conclusions.append(conclusion)
        self.reasoning_trace.append(f"[CONCLUSION ADDED] {conclusion['diagnosis']} (CF: {conclusion['confidence']})")
        
    def get_facts(self):
        """Dapatkan semua fakta sebagai set"""
        return self.facts.copy()
        
    def has_fact(self, fact):
        """Cek apakah fakta ada"""
        return fact in self.facts
        
    def log_reasoning(self, message):
        """Catat langkah penalaran"""
        self.reasoning_trace.append(message)
        
    def save_to_file(self, filename=None):
        """Simpan working memory ke file"""
        if not filename:
            filename = f"wm_{self.session_id}.json"
            
        data = {
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat(),
            'facts': list(self.facts),
            'conclusions': self.conclusions,
            'reasoning_trace': self.reasoning_trace
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def load_from_file(self, filename):
        """Load working memory dari file"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.session_id = data['session_id']
        self.timestamp = datetime.fromisoformat(data['timestamp'])
        self.facts = set(data['facts'])
        self.conclusions = data['conclusions']
        self.reasoning_trace = data['reasoning_trace']
        
    def display_status(self):
        """Tampilkan status working memory"""
        print(f"\n--- WORKING MEMORY STATUS [{self.session_id}] ---")
        print(f"Facts: {list(self.facts)}")
        print(f"Conclusions: {len(self.conclusions)}")
        print(f"Reasoning Steps: {len(self.reasoning_trace)}")
        print("---" + "-" * (30 + len(self.session_id)))