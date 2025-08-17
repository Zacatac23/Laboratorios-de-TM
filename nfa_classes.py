"""
nfa_classes.py - Clases para representar NFAs (Autómatas Finitos No Deterministas)
"""

from collections import defaultdict, deque

class NFAState:
    """Representa un estado en el NFA"""
    
    def __init__(self, state_id, is_final=False):
        self.id = state_id
        self.is_final = is_final
        self.transitions = defaultdict(set)  # symbol -> set of states
        self.epsilon_transitions = set()     # set of states reachable by epsilon
    
    def add_transition(self, symbol, state):
        """Agrega una transición desde este estado"""
        if symbol == 'ε' or symbol == '':
            self.epsilon_transitions.add(state)
        else:
            self.transitions[symbol].add(state)
    
    def get_transitions_for_symbol(self, symbol):
        """Obtiene estados alcanzables con un símbolo específico"""
        return self.transitions.get(symbol, set())
    
    def has_epsilon_transitions(self):
        """Verifica si tiene transiciones epsilon"""
        return len(self.epsilon_transitions) > 0
    
    def get_all_symbols(self):
        """Obtiene todos los símbolos de transición"""
        symbols = set(self.transitions.keys())
        if self.epsilon_transitions:
            symbols.add('ε')
        return symbols
    
    def __str__(self):
        return f"State {self.id}{'(F)' if self.is_final else ''}"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, NFAState) and self.id == other.id

class NFA:
    """Representa un NFA completo"""
    
    def __init__(self, start_state, final_state):
        self.start_state = start_state
        self.final_state = final_state
        self.states = set()
        self._collect_states()
    
    def _collect_states(self):
        """Recolecta todos los estados del NFA mediante BFS"""
        visited = set()
        queue = deque([self.start_state])
        
        while queue:
            state = queue.popleft()
            if state in visited:
                continue
            
            visited.add(state)
            self.states.add(state)
            
            # Agregar estados alcanzables por transiciones normales
            for symbol_states in state.transitions.values():
                for next_state in symbol_states:
                    if next_state not in visited:
                        queue.append(next_state)
            
            # Agregar estados alcanzables por epsilon
            for next_state in state.epsilon_transitions:
                if next_state not in visited:
                    queue.append(next_state)
    
    def epsilon_closure(self, states):
        """Calcula la epsilon-clausura de un conjunto de estados"""
        if not states:
            return set()
        
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            for next_state in state.epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        
        return closure
    
    def get_alphabet(self):
        """Obtiene el alfabeto del NFA (símbolos sin epsilon)"""
        alphabet = set()
        for state in self.states:
            alphabet.update(state.transitions.keys())
        alphabet.discard('ε')  # Remover epsilon si está presente
        return alphabet
    
    def simulate(self, input_string):
        """Simula el NFA con una cadena de entrada"""
        print(f"\n🔄 SIMULANDO NFA CON CADENA: '{input_string}'")
        print("=" * 50)
        
        # Estado inicial con epsilon-clausura
        current_states = self.epsilon_closure({self.start_state})
        print(f"Estados iniciales (con ε-clausura): {sorted([s.id for s in current_states])}")
        
        # Procesar cada símbolo
        for i, symbol in enumerate(input_string):
            print(f"\nPaso {i+1}: Procesando símbolo '{symbol}'")
            print(f"Estados actuales: {sorted([s.id for s in current_states])}")
            
            # Calcular estados alcanzables con el símbolo actual
            next_states = set()
            for state in current_states:
                next_states.update(state.get_transitions_for_symbol(symbol))
            
            print(f"Estados después de '{symbol}': {sorted([s.id for s in next_states])}")
            
            # Aplicar epsilon-clausura
            current_states = self.epsilon_closure(next_states)
            print(f"Estados con ε-clausura: {sorted([s.id for s in current_states])}")
            
            # Verificar si no hay estados alcanzables
            if not current_states:
                print("❌ No hay estados alcanzables - RECHAZADA")
                return False
        
        # Verificar aceptación
        final_reached = any(state.is_final for state in current_states)
        final_states = [s.id for s in current_states if s.is_final]
        
        print(f"\n🎯 RESULTADO:")
        if final_reached:
            print(f"✅ ACEPTADA - Estado final alcanzado")
            print(f"Estados finales en conjunto: {final_states}")
        else:
            print(f"❌ RECHAZADA - No se alcanzó estado final")
            print(f"Estados actuales: {sorted([s.id for s in current_states])}")
        
        return final_reached
    
    def simulate_step_by_step(self, input_string):
        """Simulación detallada que retorna información de cada paso"""
        steps = []
        current_states = self.epsilon_closure({self.start_state})
        
        steps.append({
            'step': 0,
            'symbol': None,
            'states_before': set(),
            'states_after_transition': set(),
            'states_after_epsilon': current_states.copy(),
            'description': 'Estado inicial con ε-clausura'
        })
        
        for i, symbol in enumerate(input_string):
            # Estados antes de procesar el símbolo
            states_before = current_states.copy()
            
            # Calcular transiciones
            next_states = set()
            for state in current_states:
                next_states.update(state.get_transitions_for_symbol(symbol))
            
            # Aplicar epsilon-clausura
            current_states = self.epsilon_closure(next_states)
            
            steps.append({
                'step': i + 1,
                'symbol': symbol,
                'states_before': states_before,
                'states_after_transition': next_states.copy(),
                'states_after_epsilon': current_states.copy(),
                'description': f'Procesando símbolo {symbol}'
            })
            
            # Si no hay estados, terminar
            if not current_states:
                break
        
        # Resultado final
        final_reached = any(state.is_final for state in current_states)
        
        return {
            'steps': steps,
            'accepted': final_reached,
            'final_states': current_states
        }
    
    def get_state_count(self):
        """Retorna el número total de estados"""
        return len(self.states)
    
    def get_transition_count(self):
        """Retorna el número total de transiciones"""
        count = 0
        for state in self.states:
            count += len(state.epsilon_transitions)
            for symbol_states in state.transitions.values():
                count += len(symbol_states)
        return count
    
    def __str__(self):
        return f"NFA(states={len(self.states)}, start={self.start_state.id}, final={self.final_state.id})"
    
    def __repr__(self):
        return self.__str__()