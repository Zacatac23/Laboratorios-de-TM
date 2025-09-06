"""
dfa_classes.py - Clases para representar DFAs (Autómatas Finitos Deterministas)
"""

from collections import defaultdict

class DFAState:
    """Representa un estado en el DFA"""
    
    def __init__(self, state_id, is_final=False, nfa_states=None):
        self.id = state_id
        self.is_final = is_final
        self.transitions = {}  # symbol -> single state
        self.nfa_states = nfa_states or set()  # Estados del NFA que representa
    
    def add_transition(self, symbol, state):
        """Agrega una transición desde este estado"""
        self.transitions[symbol] = state
    
    def get_transition_for_symbol(self, symbol):
        """Obtiene el estado alcanzable con un símbolo específico"""
        return self.transitions.get(symbol)
    
    def get_all_symbols(self):
        """Obtiene todos los símbolos de transición"""
        return set(self.transitions.keys())
    
    def __str__(self):
        return f"DFAState {self.id}{'(F)' if self.is_final else ''}"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, DFAState) and self.id == other.id

class DFA:
    """Representa un DFA completo"""
    
    def __init__(self, start_state, final_states=None):
        self.start_state = start_state
        self.final_states = final_states or set()
        self.states = set()
        self.alphabet = set()
        self._collect_info()
    
    def _collect_info(self):
        """Recolecta información sobre estados y alfabeto"""
        visited = set()
        stack = [self.start_state]
        
        while stack:
            state = stack.pop()
            if state in visited:
                continue
            
            visited.add(state)
            self.states.add(state)
            
            # Recolectar alfabeto y estados siguientes
            for symbol, next_state in state.transitions.items():
                self.alphabet.add(symbol)
                if next_state not in visited:
                    stack.append(next_state)
        
        # Actualizar estados finales
        self.final_states = {s for s in self.states if s.is_final}
    
    def get_alphabet(self):
        """Obtiene el alfabeto del DFA"""
        return self.alphabet.copy()
    
    def simulate(self, input_string):
        """Simula el DFA con una cadena de entrada"""
        print(f"\n🔄 SIMULANDO DFA CON CADENA: '{input_string}'")
        print("=" * 50)
        
        current_state = self.start_state
        print(f"Estado inicial: {current_state.id}")
        
        # Procesar cada símbolo
        for i, symbol in enumerate(input_string):
            print(f"\nPaso {i+1}: Procesando símbolo '{symbol}'")
            print(f"Estado actual: {current_state.id}")
            
            # Obtener siguiente estado
            next_state = current_state.get_transition_for_symbol(symbol)
            
            if next_state is None:
                print(f"❌ No hay transición con '{symbol}' - RECHAZADA")
                return False
            
            current_state = next_state
            print(f"Siguiente estado: {current_state.id}")
        
        # Verificar aceptación
        is_accepted = current_state.is_final
        
        print(f"\n🎯 RESULTADO:")
        if is_accepted:
            print(f"✅ ACEPTADA - Estado final: {current_state.id}")
        else:
            print(f"❌ RECHAZADA - Estado no final: {current_state.id}")
        
        return is_accepted
    
    def simulate_step_by_step(self, input_string):
        """Simulación detallada que retorna información de cada paso"""
        steps = []
        current_state = self.start_state
        
        steps.append({
            'step': 0,
            'symbol': None,
            'state': current_state,
            'description': 'Estado inicial'
        })
        
        for i, symbol in enumerate(input_string):
            next_state = current_state.get_transition_for_symbol(symbol)
            
            if next_state is None:
                steps.append({
                    'step': i + 1,
                    'symbol': symbol,
                    'state': None,
                    'description': f'Sin transición para {symbol}'
                })
                break
            
            current_state = next_state
            steps.append({
                'step': i + 1,
                'symbol': symbol,
                'state': current_state,
                'description': f'Transición con {symbol}'
            })
        
        return {
            'steps': steps,
            'accepted': current_state.is_final if current_state else False,
            'final_state': current_state
        }
    
    def is_complete(self):
        """Verifica si el DFA es completo (todas las transiciones definidas)"""
        for state in self.states:
            for symbol in self.alphabet:
                if state.get_transition_for_symbol(symbol) is None:
                    return False
        return True
    
    def get_state_count(self):
        """Retorna el número total de estados"""
        return len(self.states)
    
    def get_transition_count(self):
        """Retorna el número total de transiciones"""
        return sum(len(state.transitions) for state in self.states)
    
    def __str__(self):
        return f"DFA(states={len(self.states)}, start={self.start_state.id}, finals={len(self.final_states)})"
    
    def __repr__(self):
        return self.__str__()