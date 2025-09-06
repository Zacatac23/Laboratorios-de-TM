"""
dfa_minimization.py - Implementación del algoritmo de minimización de DFAs
"""

from collections import defaultdict, deque
from dfa_classes import DFA, DFAState

class DFAMinimizer:
    """Implementa el algoritmo de minimización de DFAs"""
    
    def __init__(self):
        self.state_counter = 0
    
    def reset_counter(self):
        """Reinicia el contador de estados"""
        self.state_counter = 0
    
    def new_state(self, is_final=False):
        """Crea un nuevo estado con ID único"""
        state = DFAState(self.state_counter, is_final)
        self.state_counter += 1
        return state
    
    def minimize_dfa(self, dfa):
        """Minimiza un DFA usando el algoritmo de particiones"""
        print(f"\n🔧 MINIMIZACIÓN DE DFA")
        print("=" * 40)
        
        self.reset_counter()
        
        if len(dfa.states) <= 1:
            print("DFA ya es mínimo (≤ 1 estado)")
            return dfa
        
        # Paso 1: Eliminar estados inaccesibles
        reachable_states = self._get_reachable_states(dfa)
        print(f"📍 Estados alcanzables: {sorted([s.id for s in reachable_states])}")
        
        if len(reachable_states) < len(dfa.states):
            unreachable = dfa.states - reachable_states
            print(f"🗑️ Estados eliminados (inaccesibles): {sorted([s.id for s in unreachable])}")
        
        # Paso 2: Partición inicial - separar finales de no finales
        final_states = {s for s in reachable_states if s.is_final}
        non_final_states = reachable_states - final_states
        
        # Crear partición inicial
        partitions = []
        if non_final_states:
            partitions.append(non_final_states)
        if final_states:
            partitions.append(final_states)
        
        print(f"\n🔄 ALGORITMO DE PARTICIONES:")
        print(f"Partición inicial:")
        for i, partition in enumerate(partitions):
            print(f"  P{i}: {sorted([s.id for s in partition])}")
        
        alphabet = sorted(dfa.get_alphabet())
        iteration = 0
        
        # Paso 3: Refinar particiones iterativamente
        while True:
            iteration += 1
            print(f"\n--- Iteración {iteration} ---")
            
            new_partitions = []
            changed = False
            
            for partition_idx, partition in enumerate(partitions):
                if len(partition) == 1:
                    # Particiones unitarias no se pueden dividir más
                    new_partitions.append(partition)
                    continue
                
                # Intentar dividir esta partición
                sub_partitions = self._refine_partition(partition, partitions, alphabet)
                
                if len(sub_partitions) > 1:
                    changed = True
                    print(f"  P{partition_idx} dividida en {len(sub_partitions)} sub-particiones:")
                    for i, sub_part in enumerate(sub_partitions):
                        print(f"    P{partition_idx}.{i}: {sorted([s.id for s in sub_part])}")
                
                new_partitions.extend(sub_partitions)
            
            partitions = new_partitions
            
            if not changed:
                print(f"  ✅ No hay más divisiones posibles")
                break
        
        print(f"\n🎯 PARTICIONES FINALES:")
        for i, partition in enumerate(partitions):
            states_ids = sorted([s.id for s in partition])
            is_final = any(s.is_final for s in partition)
            print(f"  P{i}: {states_ids} {'(Final)' if is_final else ''}")
        
        # Paso 4: Construir DFA minimizado
        minimized_dfa = self._build_minimized_dfa(dfa, partitions)
        
        print(f"\n📊 RESULTADO DE MINIMIZACIÓN:")
        print(f"  Estados originales: {len(dfa.states)}")
        print(f"  Estados minimizados: {len(minimized_dfa.states)}")
        print(f"  Reducción: {len(dfa.states) - len(minimized_dfa.states)} estados")
        
        return minimized_dfa
    
    def _get_reachable_states(self, dfa):
        """Obtiene todos los estados alcanzables desde el estado inicial"""
        reachable = set()
        queue = deque([dfa.start_state])
        
        while queue:
            state = queue.popleft()
            if state in reachable:
                continue
                
            reachable.add(state)
            
            # Agregar estados alcanzables por transiciones
            for next_state in state.transitions.values():
                if next_state not in reachable:
                    queue.append(next_state)
        
        return reachable
    
    def _refine_partition(self, partition, all_partitions, alphabet):
        """Refina una partición basándose en las transiciones"""
        if len(partition) == 1:
            return [partition]
        
        # Crear grupos basados en el comportamiento de transiciones
        transition_signatures = defaultdict(set)
        
        for state in partition:
            signature = []
            
            # Para cada símbolo, determinar a qué partición va el estado destino
            for symbol in alphabet:
                target_state = state.get_transition_for_symbol(symbol)
                
                if target_state is None:
                    signature.append(None)
                else:
                    # Encontrar en qué partición está el estado destino
                    target_partition_idx = None
                    for idx, part in enumerate(all_partitions):
                        if target_state in part:
                            target_partition_idx = idx
                            break
                    signature.append(target_partition_idx)
            
            signature_tuple = tuple(signature)
            transition_signatures[signature_tuple].add(state)
        
        # Retornar las sub-particiones
        return list(transition_signatures.values())
    
    def _build_minimized_dfa(self, original_dfa, partitions):
        """Construye el DFA minimizado a partir de las particiones"""
        # Mapeo de estados originales a particiones
        state_to_partition = {}
        partition_representatives = {}
        
        for partition_idx, partition in enumerate(partitions):
            representative = self.new_state()
            partition_representatives[partition_idx] = representative
            
            # Determinar si la partición es final
            representative.is_final = any(s.is_final for s in partition)
            
            for state in partition:
                state_to_partition[state] = partition_idx
        
        # Construir transiciones para el DFA minimizado
        alphabet = original_dfa.get_alphabet()
        
        for partition_idx, partition in enumerate(partitions):
            representative = partition_representatives[partition_idx]
            
            # Tomar cualquier estado de la partición como representante
            sample_state = next(iter(partition))
            
            # Crear transiciones
            for symbol in alphabet:
                target_state = sample_state.get_transition_for_symbol(symbol)
                
                if target_state is not None:
                    target_partition_idx = state_to_partition[target_state]
                    target_representative = partition_representatives[target_partition_idx]
                    
                    representative.add_transition(symbol, target_representative)
        
        # Determinar estado inicial del DFA minimizado
        start_partition_idx = state_to_partition[original_dfa.start_state]
        minimized_start = partition_representatives[start_partition_idx]
        
        # Crear DFA minimizado
        final_states = {rep for rep in partition_representatives.values() if rep.is_final}
        minimized_dfa = DFA(minimized_start, final_states)
        
        return minimized_dfa
    
    def validate_minimized_dfa(self, original_dfa, minimized_dfa):
        """Valida que el DFA minimizado sea equivalente al original"""
        print(f"\n🔍 VALIDANDO EQUIVALENCIA:")
        
        # Probar con algunas cadenas de prueba
        test_strings = ["", "a", "b", "aa", "bb", "ab", "ba", "aaa", "bbb", "aba", "bab"]
        
        all_match = True
        
        for test_string in test_strings:
            original_result = self._simulate_quietly(original_dfa, test_string)
            minimized_result = self._simulate_quietly(minimized_dfa, test_string)
            
            if original_result != minimized_result:
                print(f"❌ Discrepancia en '{test_string}': original={original_result}, minimizado={minimized_result}")
                all_match = False
        
        if all_match:
            print(f"✅ DFA minimizado es equivalente al original")
        else:
            print(f"❌ DFA minimizado NO es equivalente al original")
        
        return all_match
    
    def _simulate_quietly(self, dfa, input_string):
        """Simula DFA sin imprimir información de debug"""
        current_state = dfa.start_state
        
        for symbol in input_string:
            next_state = current_state.get_transition_for_symbol(symbol)
            if next_state is None:
                return False
            current_state = next_state
        
        return current_state.is_final
    
    def print_minimization_summary(self, original_dfa, minimized_dfa):
        """Imprime resumen de la minimización"""
        print(f"\n📋 RESUMEN DE MINIMIZACIÓN:")
        print("-" * 40)
        print(f"Estados originales: {len(original_dfa.states)}")
        print(f"Estados minimizados: {len(minimized_dfa.states)}")
        
        reduction = len(original_dfa.states) - len(minimized_dfa.states)
        if reduction > 0:
            percentage = (reduction / len(original_dfa.states)) * 100
            print(f"Reducción: {reduction} estados ({percentage:.1f}%)")
        else:
            print("Reducción: 0 estados (DFA ya era mínimo)")
        
        print(f"Transiciones originales: {original_dfa.get_transition_count()}")
        print(f"Transiciones minimizadas: {minimized_dfa.get_transition_count()}")