"""
visualizer.py - Visualizador para AST y NFA usando Graphviz
"""

import os
import subprocess
import tempfile

class Visualizer:
    """Clase base para visualización"""
    
    def __init__(self):
        self.png_methods = []
        self._test_png_methods()
    
    def _test_png_methods(self):
        """Prueba diferentes métodos para generar PNG"""
        print("🔍 Probando métodos para generar PNG...")
        
        # Método 1: Graphviz Python module
        try:
            import graphviz
            test_dot = graphviz.Digraph()
            test_dot.node('A', 'Test')
            test_file = tempfile.mktemp()
            test_dot.render(test_file, format='png', cleanup=False)
            if os.path.exists(f'{test_file}.png'):
                os.remove(f'{test_file}.png')
                self.png_methods.append('graphviz_module')
                print("✅ Método 1: Módulo graphviz Python")
        except Exception:
            pass
        
        # Método 2: Subprocess directo
        try:
            result = subprocess.run(
                ['dot', '-Tpng'], 
                input='digraph test { A -> B; }',
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.png_methods.append('subprocess_direct')
                print("✅ Método 2: Subprocess directo")
        except Exception:
            pass
        
        # Método 3: Archivo temporal
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False) as f:
                f.write('digraph test { A -> B; }')
                temp_dot = f.name
            
            temp_png = temp_dot.replace('.dot', '.png')
            result = subprocess.run(['dot', '-Tpng', temp_dot, '-o', temp_png], 
                                  capture_output=True, timeout=5)
            
            if result.returncode == 0 and os.path.exists(temp_png):
                self.png_methods.append('temp_file')
                print("✅ Método 3: Archivo temporal")
                os.remove(temp_png)
            os.remove(temp_dot)
        except Exception:
            pass
        
        if not self.png_methods:
            print("❌ No se encontraron métodos válidos para PNG")
        else:
            print(f"🎯 {len(self.png_methods)} métodos disponibles para PNG")
    
    def create_png_from_dot(self, dot_code, filename):
        """Crea PNG desde código DOT usando el mejor método disponible"""
        print(f"\n🖼️ Generando imagen: {filename}")
        
        if not self.png_methods:
            return self._save_dot_file(dot_code, filename)
        
        for method in self.png_methods:
            try:
                if method == 'graphviz_module':
                    if self._create_png_graphviz_module(dot_code, filename):
                        return True
                
                elif method == 'subprocess_direct':
                    if self._create_png_subprocess_direct(dot_code, filename):
                        return True
                
                elif method == 'temp_file':
                    if self._create_png_temp_file(dot_code, filename):
                        return True
                        
            except Exception as e:
                print(f"⚠️ Método {method} falló: {e}")
                continue
        
        # Si todos los métodos fallan, guardar archivo DOT
        return self._save_dot_file(dot_code, filename)
    
    def _create_png_graphviz_module(self, dot_code, filename):
        """Crear PNG usando módulo graphviz"""
        import graphviz
        dot = graphviz.Source(dot_code)
        dot.render(filename, format='png', cleanup=True)
        
        if os.path.exists(f'{filename}.png'):
            print(f"✅ PNG creado: {filename}.png (método: graphviz_module)")
            return True
        return False
    
    def _create_png_subprocess_direct(self, dot_code, filename):
        """Crear PNG usando subprocess directo"""
        result = subprocess.run(
            ['dot', '-Tpng'], input=dot_code,
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0:
            with open(f'{filename}.png', 'wb') as f:
                f.write(result.stdout.encode('latin1'))
            print(f"✅ PNG creado: {filename}.png (método: subprocess_direct)")
            return True
        return False
    
    def _create_png_temp_file(self, dot_code, filename):
        """Crear PNG usando archivo temporal"""
        dot_file = f'{filename}.dot'
        
        with open(dot_file, 'w') as f:
            f.write(dot_code)
        
        result = subprocess.run(
            ['dot', '-Tpng', dot_file, '-o', f'{filename}.png'],
            capture_output=True, timeout=10
        )
        
        success = result.returncode == 0 and os.path.exists(f'{filename}.png')
        
        if success:
            print(f"✅ PNG creado: {filename}.png (método: temp_file)")
        
        # Limpiar archivo DOT temporal
        if os.path.exists(dot_file):
            os.remove(dot_file)
        
        return success
    
    def _save_dot_file(self, dot_code, filename):
        """Guardar código DOT como fallback"""
        try:
            with open(f'{filename}.dot', 'w') as f:
                f.write(dot_code)
            print(f"💾 Código DOT guardado: {filename}.dot")
            print(f"   Convertir manualmente: dot -Tpng {filename}.dot -o {filename}.png")
            return False
        except Exception as e:
            print(f"❌ Error guardando DOT: {e}")
            return False

class ASTVisualizer(Visualizer):
    """Visualizador específico para AST"""
    
    def generate_ast_dot(self, root):
        """Genera código DOT para el AST"""
        dot_lines = []
        dot_lines.append('digraph AST {')
        dot_lines.append('  rankdir=TB;')
        dot_lines.append('  size="10,8";')
        dot_lines.append('  dpi=150;')
        dot_lines.append('  node [shape=circle, style=filled, fontname="Arial", fontsize=14];')
        dot_lines.append('  edge [fontname="Arial", fontsize=12];')
        
        # Colores para diferentes tipos de nodos
        colors = {
            'operand': '"#E3F2FD"',      # Azul claro
            'unary_op': '"#E8F5E8"',     # Verde claro
            'binary_op': '"#FFEBEE"'     # Rojo claro
        }
        
        def add_node(node):
            if not node:
                return
            
            # Formatear etiqueta del nodo
            label = node.value
            if label == '.':
                label = 'CONCAT'
            elif label == '|':
                label = 'OR'
            elif label == 'ε':
                label = 'ε'
            
            # Seleccionar color
            color = colors.get(node.node_type, '"white"')
            
            # Agregar nodo
            dot_lines.append(f'  {node.id} [label="{label}", fillcolor={color}];')
            
            # Agregar aristas a hijos
            if node.left:
                dot_lines.append(f'  {node.id} -> {node.left.id} [label="L"];')
                add_node(node.left)
            
            if node.right:
                dot_lines.append(f'  {node.id} -> {node.right.id} [label="R"];')
                add_node(node.right)
        
        add_node(root)
        dot_lines.append('}')
        return '\n'.join(dot_lines)
    
    def create_ast_png(self, root, filename):
        """Crea imagen PNG del AST"""
        dot_code = self.generate_ast_dot(root)
        return self.create_png_from_dot(dot_code, filename)
    
    def print_ast_ascii(self, root):
        """Imprime representación ASCII del AST"""
        print(f"\n🎨 VISUALIZACIÓN ASCII DEL AST")
        print("═" * 50)
        
        def print_tree(node, prefix="", is_last=True, is_root=True):
            if not node:
                return
            
            # Símbolos para diferentes tipos de nodos
            symbols = {
                'operand': '🔵',
                'unary_op': '🟢', 
                'binary_op': '🔴'
            }
            
            # Formatear display del valor
            display = node.value
            if display == '.':
                display = 'CONCAT'
            elif display == '|':
                display = 'OR'
            elif display == 'ε':
                display = 'EPSILON'
            
            symbol = symbols.get(node.node_type, '⚪')
            
            # Imprimir nodo actual
            if is_root:
                print(f"🌳 Root: {symbol} {display} (ID: {node.id})")
                child_prefix = ""
            else:
                connector = "└── " if is_last else "├── "
                print(f"{prefix}{connector}{symbol} {display} (ID: {node.id})")
                child_prefix = prefix + ("    " if is_last else "│   ")
            
            # Procesar hijos
            children = []
            if node.left:
                children.append(('Left', node.left))
            if node.right:
                children.append(('Right', node.right))
            
            for i, (side, child) in enumerate(children):
                is_last_child = (i == len(children) - 1)
                print_tree(child, child_prefix, is_last_child, False)
        
        print_tree(root)

class NFAVisualizer(Visualizer):
    """Visualizador específico para NFA"""
    
    def generate_nfa_dot(self, nfa):
        """Genera código DOT para el NFA"""
        dot_lines = []
        dot_lines.append('digraph NFA {')
        dot_lines.append('  rankdir=LR;')
        dot_lines.append('  size="12,8";')
        dot_lines.append('  dpi=150;')
        dot_lines.append('  node [shape=circle, style=filled, fontname="Arial", fontsize=12];')
        dot_lines.append('  edge [fontname="Arial", fontsize=10];')
        
        # Nodo inicial invisible para la flecha de entrada
        dot_lines.append('  start [shape=point, style=invis];')
        
        # Agregar todos los estados
        for state in sorted(nfa.states, key=lambda s: s.id):
            if state.is_final:
                # Estado final (doble círculo, verde)
                dot_lines.append(f'  {state.id} [shape=doublecircle, fillcolor="#90EE90", label="{state.id}"];')
            elif state == nfa.start_state:
                # Estado inicial (azul)
                dot_lines.append(f'  {state.id} [fillcolor="#87CEEB", label="{state.id}"];')
            else:
                # Estado normal (gris claro)
                dot_lines.append(f'  {state.id} [fillcolor="#F0F0F0", label="{state.id}"];')
        
        # Flecha hacia el estado inicial
        dot_lines.append(f'  start -> {nfa.start_state.id} [label="start"];')
        
        # Agregar transiciones
        for state in sorted(nfa.states, key=lambda s: s.id):
            # Transiciones con símbolos
            for symbol, target_states in state.transitions.items():
                for target in sorted(target_states, key=lambda s: s.id):
                    dot_lines.append(f'  {state.id} -> {target.id} [label="{symbol}"];')
            
            # Transiciones epsilon (líneas punteadas azules)
            for target in sorted(state.epsilon_transitions, key=lambda s: s.id):
                dot_lines.append(f'  {state.id} -> {target.id} [label="ε", style=dashed, color=blue];')
        
        dot_lines.append('}')
        return '\n'.join(dot_lines)
    
    def create_nfa_png(self, nfa, filename):
        """Crea imagen PNG del NFA"""
        dot_code = self.generate_nfa_dot(nfa)
        return self.create_png_from_dot(dot_code, filename)
    
    def print_nfa_ascii(self, nfa):
        """Imprime representación ASCII del NFA"""
        print(f"\n📋 ESTRUCTURA DEL NFA")
        print("=" * 40)
        print(f"🏁 Estado inicial: {nfa.start_state.id}")
        print(f"🎯 Estado final: {nfa.final_state.id}")
        print(f"📊 Total estados: {len(nfa.states)}")
        print(f"🔗 Total transiciones: {nfa.get_transition_count()}")
        
        # Mostrar alfabeto
        alphabet = nfa.get_alphabet()
        if alphabet:
            print(f"🔤 Alfabeto: {{{', '.join(sorted(alphabet))}}}")
        else:
            print(f"🔤 Alfabeto: {{ε}}")
        
        print(f"\n🔗 TABLA DE TRANSICIONES:")
        print("Estado    Símbolo    Destino(s)")
        print("-" * 35)
        
        for state in sorted(nfa.states, key=lambda s: s.id):
            state_printed = False
            
            # Transiciones con símbolos
            for symbol in sorted(state.transitions.keys()):
                targets = sorted(state.transitions[symbol], key=lambda s: s.id)
                target_str = ', '.join(str(t.id) for t in targets)
                
                if not state_printed:
                    state_marker = f"{state.id}{'(F)' if state.is_final else ''}"
                    print(f"{state_marker:<9} {symbol:<10} {target_str}")
                    state_printed = True
                else:
                    print(f"{'':9} {symbol:<10} {target_str}")
            
            # Transiciones epsilon
            if state.epsilon_transitions:
                epsilon_targets = sorted(state.epsilon_transitions, key=lambda s: s.id)
                target_str = ', '.join(str(t.id) for t in epsilon_targets)
                
                if not state_printed:
                    state_marker = f"{state.id}{'(F)' if state.is_final else ''}"
                    print(f"{state_marker:<9} {'ε':<10} {target_str}")
                    state_printed = True
                else:
                    print(f"{'':9} {'ε':<10} {target_str}")
            
            # Si no tiene transiciones
            if not state_printed:
                state_marker = f"{state.id}{'(F)' if state.is_final else ''}"
                print(f"{state_marker:<9} {'--':<10} {'--'}")
    
    def print_simulation_trace(self, nfa, input_string):
        """Imprime traza detallada de la simulación"""
        simulation_result = nfa.simulate_step_by_step(input_string)
        
        print(f"\n🔍 TRAZA DETALLADA DE SIMULACIÓN")
        print(f"Cadena: '{input_string}'")
        print("=" * 60)
        
        for step_info in simulation_result['steps']:
            step_num = step_info['step']
            symbol = step_info['symbol']
            states_before = sorted([s.id for s in step_info['states_before']])
            states_after_trans = sorted([s.id for s in step_info['states_after_transition']])
            states_after_eps = sorted([s.id for s in step_info['states_after_epsilon']])
            
            if step_num == 0:
                print(f"Paso {step_num}: {step_info['description']}")
                print(f"  Estados: {states_after_eps}")
            else:
                print(f"\nPaso {step_num}: Procesando '{symbol}'")
                print(f"  Estados antes: {states_before}")
                print(f"  Después de '{symbol}': {states_after_trans}")
                print(f"  Con ε-clausura: {states_after_eps}")
        
        print(f"\n🎯 RESULTADO FINAL:")
        if simulation_result['accepted']:
            final_states = sorted([s.id for s in simulation_result['final_states']])
            print(f"✅ ACEPTADA - Estados finales: {final_states}")
        else:
            print(f"❌ RECHAZADA")
        
        return simulation_result['accepted']