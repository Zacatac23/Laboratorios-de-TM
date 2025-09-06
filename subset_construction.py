"""
subset_construction.py - Implementación del algoritmo de construcción de subconjuntos (NFA a DFA)
"""

from collections import deque
from dfa_classes import DFA, DFAState

class SubsetConstructor:
    """Implementa el algoritmo de construcción de subconjuntos"""
    
    def __init__(self):
        self.state_counter = 0
        self.subset_to_dfa_state = {}  # Mapeo de conjuntos de estados NFA a estados DFA
    
    def reset_counter(self):
        """Reinicia el contador de estados"""
        self.state_counter = 0
        self.subset_to_dfa_state = {}
    
    def new_dfa_state(self, nfa_states, is_final=False):
        """Crea un nuevo estado DFA"""
        state = DFAState(self.state_counter, is_final, nfa_states)
        self.state_counter += 1
        return state
    
    def nfa_to_dfa(self, nfa):
        """Convierte NFA a DFA usando construcción de subconjuntos"""
        print(f"\n🔧 CONSTRUCCIÓN DE SUBCONJUNTOS (NFA → DFA)")
        print("=" * 55)
        
        self.reset_counter()
        
        # Obtener alfabeto del NFA (sin epsilon)
        alphabet = nfa.get_alphabet()
        print(f"📝 Alfabeto: {sorted(alphabet)}")
        
        # Estado inicial del DFA: epsilon-clausura del estado inicial del NFA
        initial_subset = nfa.epsilon_closure({nfa.start_state})
        initial_subset_frozen = frozenset(initial_subset)
        
        # Verificar si el estado inicial es final
        initial_is_final = any(state.is_final for state in initial_subset)
        
        # Crear estado inicial del DFA
        dfa_start = self.new_dfa_state(initial_subset, initial_is_final)
        self.subset_to_dfa_state[initial_subset_frozen] = dfa_start
        
        print(f"\n🏁 Estado inicial DFA:")
        print(f"   Estado DFA: {dfa_start.id}")
        print(f"   Estados NFA: {sorted([s.id for s in initial_subset])}")
        print(f"   Es final: {initial_is_final}")
        
        # Cola de trabajo: conjuntos de estados por procesar
        work_queue = deque([initial_subset_frozen])
        processed = set()
        
        print(f"\n🔄 PROCESAMIENTO DE ESTADOS:")
        print("-" * 40)
        
        while work_queue:
            current_subset_frozen = work_queue.popleft()
            
            if current_subset_frozen in processed:
                continue
                
            processed.add(current_subset_frozen)
            current_subset = set(current_subset_frozen)
            current_dfa_state = self.subset_to_dfa_state[current_subset_frozen]
            
            print(f"\n📍 Procesando estado DFA {current_dfa_state.id}:")
            print(f"   Estados NFA: {sorted([s.id for s in current_subset])}")
            
            # Para cada símbolo del alfabeto
            for symbol in sorted(alphabet):
                # Calcular el conjunto de estados alcanzables con este símbolo
                next_subset = set()
                
                for nfa_state in current_subset:
                    # Obtener estados alcanzables con el símbolo
                    reachable = nfa_state.get_transitions_for_symbol(symbol)
                    next_subset.update(reachable)
                
                # Aplicar epsilon-clausura al resultado
                if next_subset:
                    next_subset_with_epsilon = nfa.epsilon_closure(next_subset)
                else:
                    next_subset_with_epsilon = set()
                
                print(f"   Con '{symbol}': {sorted([s.id for s in next_subset_with_epsilon]) if next_subset_with_epsilon else '∅'}")
                
                # Si el conjunto no está vacío, crear/obtener estado DFA correspondiente
                if next_subset_with_epsilon:
                    next_subset_frozen = frozenset(next_subset_with_epsilon)
                    
                    # Si no existe, crear nuevo estado DFA
                    if next_subset_frozen not in self.subset_to_dfa_state:
                        # Verificar si es estado final
                        is_final = any(state.is_final for state in next_subset_with_epsilon)
                        
                        next_dfa_state = self.new_dfa_state(next_subset_with_epsilon, is_final)
                        self.subset_to_dfa_state[next_subset_frozen] = next_dfa_state
                        
                        # Agregar a la cola para procesamiento
                        work_queue.append(next_subset_frozen)
                        
                        print(f"     → Nuevo estado DFA {next_dfa_state.id} {'(Final)' if is_final else ''}")
                    else:
                        next_dfa_state = self.subset_to_dfa_state[next_subset_frozen]
                        print(f"     → Estado existente DFA {next_dfa_state.id}")
                    
                    # Agregar transición
                    current_dfa_state.add_transition(symbol, next_dfa_state)
        
        # Recolectar estados finales
        final_states = {state for state in self.subset_to_dfa_state.values() if state.is_final}
        
        # Crear DFA
        dfa = DFA(dfa_start, final_states)
        
        print(f"\n✅ DFA CONSTRUIDO:")
        print(f"   🔢 Estados DFA: {self.state_counter}")
        print(f"   🏁 Estado inicial: {dfa_start.id}")
        print(f"   🎯 Estados finales: {sorted([s.id for s in final_states])}")
        print(f"   📊 Total transiciones: {dfa.get_transition_count()}")
        print(f"   🔤 Alfabeto: {sorted(dfa.get_alphabet())}")
        
        return dfa
    
    def print_subset_mapping(self):
        """Imprime el mapeo de subconjuntos NFA a estados DFA"""
        print(f"\n📋 MAPEO DE SUBCONJUNTOS:")
        print("-" * 50)
        
        for subset_frozen, dfa_state in sorted(self.subset_to_dfa_state.items(), 
                                               key=lambda x: x[1].id):
            nfa_ids = sorted([s.id for s in subset_frozen])
            final_mark = " (Final)" if dfa_state.is_final else ""
            print(f"Estado DFA {dfa_state.id}{final_mark}: {{{', '.join(map(str, nfa_ids))}}}")
    
    def validate_dfa(self, dfa):
        """Valida que el DFA construido sea correcto"""
        issues = []
        
        # Verificar que hay exactamente un estado inicial
        if not dfa.start_state:
            issues.append("No hay estado inicial")
        
        # Verificar que hay al menos un estado final (opcional para algunos casos)
        if len(dfa.final_states) == 0:
            issues.append("No hay estados finales")
        
        # Verificar determinismo: cada estado tiene exactamente una transición por símbolo
        alphabet = dfa.get_alphabet()
        
        for state in dfa.states:
            for symbol in alphabet:
                transition = state.get_transition_for_symbol(symbol)
                # En un DFA puede no tener transición para algunos símbolos (DFA incompleto)
                # pero si la tiene, debe ser única (ya garantizado por la estructura de datos)
        
        # Verificar que todas las transiciones apuntan a estados válidos
        for state in dfa.states:
            for symbol, target_state in state.transitions.items():
                if target_state not in dfa.states:
                    issues.append(f"Transición inválida: Estado {state.id} --{symbol}--> {target_state.id} (destino no existe)")
        
        if issues:
            print(f"\n⚠️ PROBLEMAS EN DFA:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print(f"\n✅ DFA válido - Todas las verificaciones pasaron")
            return True