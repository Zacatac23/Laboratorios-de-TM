"""
dfa_visualizer.py - Extensión del visualizador para DFAs
"""

from visualizer import Visualizer

class DFAVisualizer(Visualizer):
    """Visualizador específico para DFAs"""
    
    def generate_dfa_dot(self, dfa, title="DFA"):
        """Genera código DOT para el DFA"""
        dot_lines = []
        dot_lines.append(f'digraph {title.replace(" ", "_")} {{')
        dot_lines.append('  rankdir=LR;')
        dot_lines.append('  size="12,8";')
        dot_lines.append('  dpi=150;')
        dot_lines.append('  node [shape=circle, style=filled, fontname="Arial", fontsize=12];')
        dot_lines.append('  edge [fontname="Arial", fontsize=10];')
        dot_lines.append(f'  label="{title}";')
        dot_lines.append('  labelloc=t;')
        
        # Nodo inicial invisible para la flecha de entrada
        dot_lines.append('  start [shape=point, style=invis];')
        
        # Agregar todos los estados
        for state in sorted(dfa.states, key=lambda s: s.id):
            if state.is_final:
                # Estado final (doble círculo, verde)
                dot_lines.append(f'  {state.id} [shape=doublecircle, fillcolor="#90EE90", label="{state.id}"];')
            elif state == dfa.start_state:
                # Estado inicial (azul)
                dot_lines.append(f'  {state.id} [fillcolor="#87CEEB", label="{state.id}"];')
            else:
                # Estado normal (gris claro)
                dot_lines.append(f'  {state.id} [fillcolor="#F0F0F0", label="{state.id}"];')
        
        # Flecha hacia el estado inicial
        dot_lines.append(f'  start -> {dfa.start_state.id} [label="start"];')
        
        # Agregar transiciones
        for state in sorted(dfa.states, key=lambda s: s.id):
            for symbol, target in sorted(state.transitions.items()):
                dot_lines.append(f'  {state.id} -> {target.id} [label="{symbol}"];')
        
        dot_lines.append('}')
        return '\n'.join(dot_lines)
    
    def create_dfa_png(self, dfa, filename, title="DFA"):
        """Crea imagen PNG del DFA"""
        dot_code = self.generate_dfa_dot(dfa, title)
        return self.create_png_from_dot(dot_code, filename)
    
    def print_dfa_ascii(self, dfa, title="DFA"):
        """Imprime representación ASCII del DFA"""
        print(f"\n📋 ESTRUCTURA DEL {title}")
        print("=" * (15 + len(title)))
        print(f"🏁 Estado inicial: {dfa.start_state.id}")
        
        final_ids = sorted([s.id for s in dfa.final_states])
        if final_ids:
            print(f"🎯 Estados finales: {final_ids}")
        else:
            print(f"🎯 Estados finales: ninguno")
            
        print(f"📊 Total estados: {len(dfa.states)}")
        print(f"🔗 Total transiciones: {dfa.get_transition_count()}")
        
        # Mostrar alfabeto
        alphabet = dfa.get_alphabet()
        if alphabet:
            print(f"📤 Alfabeto: {{{', '.join(sorted(alphabet))}}}")
        else:
            print(f"📤 Alfabeto: vacío")
        
        print(f"\n🔗 TABLA DE TRANSICIONES:")
        print("Estado    Símbolo    Destino")
        print("-" * 30)
        
        for state in sorted(dfa.states, key=lambda s: s.id):
            state_printed = False
            
            # Mostrar transiciones
            for symbol in sorted(state.transitions.keys()):
                target = state.transitions[symbol]
                
                if not state_printed:
                    state_marker = f"{state.id}{'(F)' if state.is_final else ''}"
                    print(f"{state_marker:<9} {symbol:<10} {target.id}")
                    state_printed = True
                else:
                    print(f"{'':9} {symbol:<10} {target.id}")
            
            # Si no tiene transiciones
            if not state_printed:
                state_marker = f"{state.id}{'(F)' if state.is_final else ''}"
                print(f"{state_marker:<9} {'--':<10} {'--'}")
    
    def print_simulation_trace(self, dfa, input_string, title="DFA"):
        """Imprime traza detallada de la simulación del DFA"""
        simulation_result = dfa.simulate_step_by_step(input_string)
        
        print(f"\n🔍 TRAZA DETALLADA DE SIMULACIÓN {title}")
        print(f"Cadena: '{input_string}'")
        print("=" * 60)
        
        for step_info in simulation_result['steps']:
            step_num = step_info['step']
            symbol = step_info['symbol']
            state = step_info['state']
            description = step_info['description']
            
            if step_num == 0:
                print(f"Paso {step_num}: {description}")
                print(f"  Estado: {state.id}")
            else:
                print(f"\nPaso {step_num}: Procesando '{symbol}'")
                if state:
                    print(f"  Estado resultado: {state.id}")
                else:
                    print(f"  Sin transición - RECHAZADA")
                    break
        
        print(f"\n🎯 RESULTADO FINAL:")
        if simulation_result['accepted']:
            print(f"✅ ACEPTADA - Estado final: {simulation_result['final_state'].id}")
        else:
            if simulation_result['final_state']:
                print(f"❌ RECHAZADA - Estado no final: {simulation_result['final_state'].id}")
            else:
                print(f"❌ RECHAZADA - Sin transición válida")
        
        return simulation_result['accepted']
    
    def compare_dfas(self, dfa1, dfa2, title1="DFA 1", title2="DFA 2"):
        """Compara dos DFAs mostrando estadísticas"""
        print(f"\n📊 COMPARACIÓN: {title1} vs {title2}")
        print("=" * 50)
        
        stats = [
            ("Estados", len(dfa1.states), len(dfa2.states)),
            ("Estados finales", len(dfa1.final_states), len(dfa2.final_states)),
            ("Transiciones", dfa1.get_transition_count(), dfa2.get_transition_count()),
            ("Símbolos del alfabeto", len(dfa1.get_alphabet()), len(dfa2.get_alphabet()))
        ]
        
        print(f"{'Métrica':<20} {title1:<15} {title2:<15} {'Diferencia':<12}")
        print("-" * 65)
        
        for metric, val1, val2 in stats:
            diff = val2 - val1
            diff_str = f"{diff:+d}" if diff != 0 else "0"
            print(f"{metric:<20} {val1:<15} {val2:<15} {diff_str:<12}")
        
        # Verificar completitud
        complete1 = dfa1.is_complete()
        complete2 = dfa2.is_complete()
        
        print(f"\n{'Completitud:':<20}")
        print(f"  {title1}: {'Completo' if complete1 else 'Incompleto'}")
        print(f"  {title2}: {'Completo' if complete2 else 'Incompleto'}")