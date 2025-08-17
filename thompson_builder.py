"""
thompson_builder.py - Implementación del algoritmo de Thompson para construir NFAs
"""

from ast_node import ASTNode
from nfa_classes import NFA, NFAState

class ThompsonNFABuilder:
    """Construye NFAs usando el algoritmo de Thompson"""
    
    def __init__(self):
        self.state_counter = 0
    
    def new_state(self, is_final=False):
        """Crea un nuevo estado con ID único"""
        state = NFAState(self.state_counter, is_final)
        self.state_counter += 1
        return state
    
    def reset_counter(self):
        """Reinicia el contador de estados"""
        self.state_counter = 0
    
    def build_nfa_from_ast(self, ast_root):
        """Construye NFA a partir del AST usando el algoritmo de Thompson"""
        print(f"\n🏗️ CONSTRUYENDO NFA CON ALGORITMO DE THOMPSON")
        print("=" * 55)
        
        # Reiniciar contador para tener IDs consistentes
        self.reset_counter()
        
        # Construir NFA recursivamente
        nfa = self._build_nfa_recursive(ast_root)
        
        # Mostrar información del NFA construido
        print(f"\n✅ NFA CONSTRUIDO EXITOSAMENTE:")
        print(f"   🏁 Estado inicial: {nfa.start_state.id}")
        print(f"   🎯 Estado final: {nfa.final_state.id}")
        print(f"   📊 Total de estados: {len(nfa.states)}")
        print(f"   🔗 Total de transiciones: {nfa.get_transition_count()}")
        print(f"   🔤 Alfabeto: {sorted(nfa.get_alphabet())}")
        
        return nfa
    
    def _build_nfa_recursive(self, node):
        """Construcción recursiva del NFA según el tipo de nodo"""
        print(f"\n🔨 Construyendo NFA para nodo: '{node.value}' (tipo: {node.node_type})")
        
        if node.is_operand():
            return self._build_basic_nfa(node.value)
        elif node.value == '.':  # Concatenación
            return self._build_concatenation_nfa(node.left, node.right)
        elif node.value == '|':  # Unión
            return self._build_union_nfa(node.left, node.right)
        elif node.value == '*':  # Clausura de Kleene
            return self._build_kleene_nfa(node.left)
        else:
            raise ValueError(f"Operador no soportado en Thompson: {node.value}")
    
    def _build_basic_nfa(self, symbol):
        """Construye NFA básico para un símbolo (Thompson Rule 1 y 2)"""
        start = self.new_state()
        final = self.new_state(is_final=True)
        
        if symbol == 'ε':
            # Regla para epsilon: q0 --ε--> qf
            start.add_transition('ε', final)
            print(f"   NFA básico ε: {start.id} --ε--> {final.id}")
        else:
            # Regla para símbolo: q0 --a--> qf
            start.add_transition(symbol, final)
            print(f"   NFA básico '{symbol}': {start.id} --{symbol}--> {final.id}")
        
        return NFA(start, final)
    
    def _build_concatenation_nfa(self, left_node, right_node):
        """Construye NFA para concatenación A.B (Thompson Rule 3)"""
        print(f"   🔗 Concatenación: {left_node.value} . {right_node.value}")
        
        # Construir NFAs para operandos
        nfa1 = self._build_nfa_recursive(left_node)
        nfa2 = self._build_nfa_recursive(right_node)
        
        # Conectar final de nfa1 con inicio de nfa2 usando epsilon
        nfa1.final_state.is_final = False  # Ya no es final
        nfa1.final_state.add_transition('ε', nfa2.start_state)
        
        print(f"   Conectando: {nfa1.final_state.id} --ε--> {nfa2.start_state.id}")
        print(f"   Resultado: {nfa1.start_state.id} ... {nfa2.final_state.id}")
        
        return NFA(nfa1.start_state, nfa2.final_state)
    
    def _build_union_nfa(self, left_node, right_node):
        """Construye NFA para unión A|B (Thompson Rule 4)"""
        print(f"   🔀 Unión: {left_node.value} | {right_node.value}")
        
        # Construir NFAs para operandos
        nfa1 = self._build_nfa_recursive(left_node)
        nfa2 = self._build_nfa_recursive(right_node)
        
        # Crear nuevos estados inicial y final
        new_start = self.new_state()
        new_final = self.new_state(is_final=True)
        
        # Nuevo inicio conecta a ambos NFAs con epsilon
        new_start.add_transition('ε', nfa1.start_state)
        new_start.add_transition('ε', nfa2.start_state)
        
        # Ambos finales conectan al nuevo final con epsilon
        nfa1.final_state.is_final = False
        nfa2.final_state.is_final = False
        nfa1.final_state.add_transition('ε', new_final)
        nfa2.final_state.add_transition('ε', new_final)
        
        print(f"   Nuevo inicio {new_start.id}:")
        print(f"     {new_start.id} --ε--> {nfa1.start_state.id}")
        print(f"     {new_start.id} --ε--> {nfa2.start_state.id}")
        print(f"   Nuevo final {new_final.id}:")
        print(f"     {nfa1.final_state.id} --ε--> {new_final.id}")
        print(f"     {nfa2.final_state.id} --ε--> {new_final.id}")
        
        return NFA(new_start, new_final)
    
    def _build_kleene_nfa(self, node):
        """Construye NFA para clausura de Kleene A* (Thompson Rule 5)"""
        print(f"   🔄 Clausura de Kleene: {node.value}*")
        
        # Construir NFA para el operando
        nfa = self._build_nfa_recursive(node)
        
        # Crear nuevos estados inicial y final
        new_start = self.new_state()
        new_final = self.new_state(is_final=True)
        
        # Transiciones para A*:
        # 1. Nuevo inicio puede ir directamente al nuevo final (para ε, cero repeticiones)
        new_start.add_transition('ε', new_final)
        
        # 2. Nuevo inicio puede entrar al NFA original
        new_start.add_transition('ε', nfa.start_state)
        
        # 3. Final original puede salir al nuevo final
        nfa.final_state.add_transition('ε', new_final)
        
        # 4. Final original puede volver al inicio original (para repetir)
        nfa.final_state.add_transition('ε', nfa.start_state)
        
        # El estado final original ya no es final
        nfa.final_state.is_final = False
        
        print(f"   Nuevo inicio {new_start.id}:")
        print(f"     {new_start.id} --ε--> {new_final.id} (para ε)")
        print(f"     {new_start.id} --ε--> {nfa.start_state.id} (entrar)")
        print(f"   Desde final original {nfa.final_state.id}:")
        print(f"     {nfa.final_state.id} --ε--> {new_final.id} (salir)")
        print(f"     {nfa.final_state.id} --ε--> {nfa.start_state.id} (repetir)")
        
        return NFA(new_start, new_final)
    
    def print_construction_summary(self, nfa):
        """Imprime un resumen de la construcción del NFA"""
        print(f"\n📋 RESUMEN DE CONSTRUCCIÓN NFA")
        print("=" * 40)
        print(f"🔢 Estados creados: {self.state_counter}")
        print(f"🏁 Estado inicial: {nfa.start_state.id}")
        print(f"🎯 Estado final: {nfa.final_state.id}")
        print(f"📊 Estados totales en NFA: {len(nfa.states)}")
        print(f"🔗 Transiciones totales: {nfa.get_transition_count()}")
        
        # Mostrar alfabeto
        alphabet = nfa.get_alphabet()
        if alphabet:
            print(f"🔤 Alfabeto: {{{', '.join(sorted(alphabet))}}}")
        else:
            print(f"🔤 Alfabeto: {{ε}} (solo epsilon)")
    
    def validate_nfa(self, nfa):
        """Valida que el NFA construido sea correcto"""
        issues = []
        
        # Verificar que hay exactamente un estado inicial
        if not nfa.start_state:
            issues.append("No hay estado inicial")
        
        # Verificar que hay exactamente un estado final
        final_states = [s for s in nfa.states if s.is_final]
        if len(final_states) == 0:
            issues.append("No hay estados finales")
        elif len(final_states) > 1:
            issues.append(f"Múltiples estados finales: {[s.id for s in final_states]}")
        
        # Verificar que el estado final está en el conjunto de estados
        if nfa.final_state not in nfa.states:
            issues.append("Estado final no está en el conjunto de estados")
        
        # Verificar que el estado inicial está en el conjunto de estados
        if nfa.start_state not in nfa.states:
            issues.append("Estado inicial no está en el conjunto de estados")
        
        # Verificar transiciones válidas
        for state in nfa.states:
            # Verificar transiciones normales
            for symbol, target_states in state.transitions.items():
                for target in target_states:
                    if target not in nfa.states:
                        issues.append(f"Transición inválida: Estado {state.id} --{symbol}--> {target.id} (destino no existe)")
            
            # Verificar transiciones epsilon
            for target in state.epsilon_transitions:
                if target not in nfa.states:
                    issues.append(f"Transición ε inválida: Estado {state.id} --ε--> {target.id} (destino no existe)")
        
        if issues:
            print(f"\n⚠️ PROBLEMAS EN NFA:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print(f"\n✅ NFA válido - Todas las verificaciones pasaron")
            return True