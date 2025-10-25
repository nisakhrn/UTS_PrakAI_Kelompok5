# working_memory.py
working_memory = []

def add_fact(fact):
    if fact not in working_memory:
        working_memory.append(fact)

def get_memory():
    return working_memory

def reset_memory():
    working_memory.clear()
