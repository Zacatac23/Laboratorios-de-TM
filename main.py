"""
main_complete.py - Programa completo para construcción de NFAs y DFAs
"""

import os
import sys
from regex_parser import RegexParser
from thompson_builder import ThompsonNFABuilder
from subset_construction import SubsetConstructor
from dfa_minimization import DFAMinimizer
from visualizer import ASTVisualizer, NFAVisualizer
from dfa_visualizer import DFAVisualizer

class CompleteAutomataProcessor:
    """Clase principal que coordina todo el proceso completo"""
    
    def __init__(self):
        self.parser = RegexParser()
        self.nfa_builder = ThompsonNFABuilder()
        self.subset_constructor = SubsetConstructor()
        self.dfa_minimizer = DFAMinimizer()
        
        # Visualizadores
        self.ast_visualizer = ASTVisualizer()
        self.nfa_visualizer = NFAVisualizer()
        self.dfa_visualizer = DFAVisualizer()
    
    def process_expression_complete(self, regex, expr_num, test_strings=None):
        """Procesa una expresión regular completa: AST → NFA → DFA → DFA minimizado"""
        print(f"\n{'='*80}")
        print(f"🎯 PROCESAMIENTO COMPLETO - EXPRESIÓN {expr_num}: {regex}")
        print(f"{'='*80}")
        
        try:
            results = {}
            
            # PASO 1: Análisis sintáctico (AST)
            print(f"\n📝 PASO 1: ANÁLISIS SINTÁCTICO")
            print("-" * 40)
            ast_root = self.parser.parse(regex)
            results['ast'] = ast_root
            
            # PASO 2: Visualización del AST
            print(f"\n🌳 PASO 2: VISUALIZACIÓN DEL AST")
            print("-" * 40)
            self.ast_visualizer.print_ast_ascii(ast_root)
            
            # Generar imagen del AST
            ast_filename = f"ast_expr_{expr_num}"
            ast_png_success = self.ast_visualizer.create_ast_png(ast_root, ast_filename)
            results['ast_png'] = ast_png_success
            
            # PASO 3: Construcción del NFA (Thompson)
            print(f"\n🏗️ PASO 3: CONSTRUCCIÓN DEL NFA (THOMPSON)")
            print("-" * 50)
            nfa = self.nfa_builder.build_nfa_from_ast(ast_root)
            is_nfa_valid = self.nfa_builder.validate_nfa(nfa)
            results['nfa'] = nfa
            results['nfa_valid'] = is_nfa_valid
            
            # Visualizar NFA
            self.nfa_visualizer.print_nfa_ascii(nfa)
            
            # Generar imagen del NFA
            nfa_filename = f"nfa_expr_{expr_num}"
            nfa_png_success = self.nfa_visualizer.create_nfa_png(nfa, nfa_filename)
            results['nfa_png'] = nfa_png_success
            
            # PASO 4: Construcción de subconjuntos (NFA → DFA)
            print(f"\n🔄 PASO 4: CONSTRUCCIÓN DE SUBCONJUNTOS (NFA → DFA)")
            print("-" * 55)
            dfa = self.subset_constructor.nfa_to_dfa(nfa)
            self.subset_constructor.print_subset_mapping()
            is_dfa_valid = self.subset_constructor.validate_dfa(dfa)
            results['dfa'] = dfa
            results['dfa_valid'] = is_dfa_valid
            
            # Visualizar DFA
            self.dfa_visualizer.print_dfa_ascii(dfa, "DFA (Construcción de Subconjuntos)")
            
            # Generar imagen del DFA
            dfa_filename = f"dfa_expr_{expr_num}"
            dfa_png_success = self.dfa_visualizer.create_dfa_png(
                dfa, dfa_filename, "DFA por Subconjuntos"
            )
            results['dfa_png'] = dfa_png_success
            
            # PASO 5: Minimización del DFA
            print(f"\n⚡ PASO 5: MINIMIZACIÓN DEL DFA")
            print("-" * 35)
            minimized_dfa = self.dfa_minimizer.minimize_dfa(dfa)
            self.dfa_minimizer.print_minimization_summary(dfa, minimized_dfa)
            
            # Validar equivalencia
            is_equivalent = self.dfa_minimizer.validate_minimized_dfa(dfa, minimized_dfa)
            results['minimized_dfa'] = minimized_dfa
            results['minimization_valid'] = is_equivalent
            
            # Visualizar DFA minimizado
            self.dfa_visualizer.print_dfa_ascii(minimized_dfa, "DFA Minimizado")
            
            # Generar imagen del DFA minimizado
            min_dfa_filename = f"dfa_min_expr_{expr_num}"
            min_dfa_png_success = self.dfa_visualizer.create_dfa_png(
                minimized_dfa, min_dfa_filename, "DFA Minimizado"
            )
            results['min_dfa_png'] = min_dfa_png_success
            
            # PASO 6: Comparación de DFAs
            print(f"\n📊 PASO 6: COMPARACIÓN DE DFAS")
            print("-" * 35)
            self.dfa_visualizer.compare_dfas(dfa, minimized_dfa, 
                                           "DFA Original", "DFA Minimizado")
            
            # PASO 7: Simulación con cadenas de prueba
            if test_strings:
                print(f"\n🧪 PASO 7: SIMULACIÓN DE AUTÓMATAS")
                print("-" * 40)
                self._test_all_automata(nfa, dfa, minimized_dfa, regex, test_strings)
            
            return results
            
        except Exception as e:
            print(f"❌ Error procesando expresión '{regex}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _test_all_automata(self, nfa, dfa, minimized_dfa, regex, test_strings):
        """Prueba todos los autómatas con las cadenas de prueba"""
        results = {'nfa': [], 'dfa': [], 'min_dfa': []}
        
        for i, test_string in enumerate(test_strings, 1):
            print(f"\n--- PRUEBA {i}/{len(test_strings)}: '{test_string}' ---")
            
            # Probar con NFA
            print(f"\n🤖 NFA:")
            nfa_result = nfa.simulate(test_string)
            results['nfa'].append((test_string, nfa_result))
            
            # Probar con DFA
            print(f"\n🔄 DFA:")
            dfa_result = dfa.simulate(test_string)
            results['dfa'].append((test_string, dfa_result))
            
            # Probar con DFA minimizado
            print(f"\n⚡ DFA Minimizado:")
            min_dfa_result = minimized_dfa.simulate(test_string)
            results['min_dfa'].append((test_string, min_dfa_result))
            
            # Verificar consistencia
            if nfa_result == dfa_result == min_dfa_result:
                consistency = "✅ CONSISTENTE"
            else:
                consistency = f"❌ INCONSISTENTE (NFA:{nfa_result}, DFA:{dfa_result}, Min:{min_dfa_result})"
            
            print(f"\n🎯 RESUMEN PRUEBA {i}: '{test_string}' ∈ L({regex})")
            print(f"   NFA: {'SÍ' if nfa_result else 'NO'}")
            print(f"   DFA: {'SÍ' if dfa_result else 'NO'}")
            print(f"   DFA Min: {'SÍ' if min_dfa_result else 'NO'}")
            print(f"   {consistency}")
        
        # Resumen final de pruebas
        self._print_test_summary(results, regex)
        return results
    
    def _print_test_summary(self, results, regex):
        """Imprime resumen final de las pruebas"""
        print(f"\n📊 RESUMEN FINAL DE PRUEBAS PARA: {regex}")
        print("=" * 60)
        
        total_tests = len(results['nfa'])
        
        for automaton_type, type_name in [('nfa', 'NFA'), ('dfa', 'DFA'), ('min_dfa', 'DFA Minimizado')]:
            accepted = sum(1 for _, result in results[automaton_type] if result)
            rejected = total_tests - accepted
            print(f"{type_name:15} - ✅ Aceptadas: {accepted:2d}/{total_tests} | ❌ Rechazadas: {rejected:2d}/{total_tests}")
        
        # Verificar consistencia total
        consistent_count = 0
        for i in range(total_tests):
            nfa_result = results['nfa'][i][1]
            dfa_result = results['dfa'][i][1]
            min_dfa_result = results['min_dfa'][i][1]
            
            if nfa_result == dfa_result == min_dfa_result:
                consistent_count += 1
        
        print(f"\n🔍 CONSISTENCIA: {consistent_count}/{total_tests} pruebas consistentes")
        
        if consistent_count == total_tests:
            print("✅ Todos los autómatas son equivalentes")
        else:
            print("❌ Hay inconsistencias entre autómatas")
    
    def process_from_file(self, filename):
        """Procesa expresiones desde un archivo"""
        if not os.path.exists(filename):
            print(f"❌ Archivo '{filename}' no encontrado")
            
            if input(f"¿Crear '{filename}' con expresiones por defecto? (s/n): ").lower() == 's':
                if self._create_default_file(filename):
                    print(f"✅ Archivo '{filename}' creado")
                else:
                    return
            else:
                return
        
        # Leer expresiones del archivo
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                expressions = [line.strip() for line in f 
                             if line.strip() and not line.startswith('#')]
            
            if not expressions:
                print(f"❌ No se encontraron expresiones válidas en '{filename}'")
                return
            
            print(f"✅ Leídas {len(expressions)} expresiones de '{filename}'")
            
        except Exception as e:
            print(f"❌ Error leyendo archivo: {e}")
            return
        
        # Procesar cada expresión
        print(f"\n🔄 PROCESANDO {len(expressions)} EXPRESIONES DEL ARCHIVO...")
        
        results = []
        
        for i, expr in enumerate(expressions, 1):
            # Cadenas de prueba básicas
            test_strings = ["", "a", "b", "ab", "ba", "aa", "bb", "aaa", "bbb", "aba"]
            
            print(f"\n{'='*60}")
            print(f"EXPRESIÓN {i}/{len(expressions)} DEL ARCHIVO")
            
            result = self.process_expression_complete(expr, i, test_strings)
            results.append(result)
            
            # Pausa entre expresiones (excepto la última)
            if i < len(expressions):
                try:
                    input(f"\n⏸️ Presiona Enter para continuar...")
                except KeyboardInterrupt:
                    print(f"\n👋 Procesamiento interrumpido")
                    break
        
        # Resumen final del archivo
        self._print_file_summary(results, filename)
    
    def _create_default_file(self, filename):
        """Crea archivo con las expresiones por defecto del proyecto"""
        default_expressions = [
            "# Expresiones regulares para el Proyecto No. 1",
            "# Universidad del Valle de Guatemala",
            "# Algoritmos: Shunting Yard, Thompson, Subconjuntos, Minimización",
            "",
            "(a*|b*)+",
            "((ε|a)|b*)*", 
            "(a|b)*abb(a|b)*",
            "0?(1?)?0*",
            "",
            "# Expresiones adicionales de prueba",
            "a|b",
            "ab*",
            "(a|b)*",
            "a+b+",
            "(ab)+",
            "a*b*c*"
        ]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for expr in default_expressions:
                    f.write(expr + '\n')
            return True
        except Exception as e:
            print(f"❌ Error creando archivo: {e}")
            return False
    
    def _print_file_summary(self, results, filename):
        """Imprime resumen del procesamiento del archivo"""
        successful = sum(1 for r in results if r is not None)
        
        print(f"\n🎉 RESUMEN FINAL DEL ARCHIVO: {filename}")
        print("=" * 60)
        print(f"✅ Expresiones procesadas exitosamente: {successful}/{len(results)}")
        
        # Contar archivos generados
        png_count = 0
        dot_count = 0
        
        for i, result in enumerate(results, 1):
            if result:
                # Verificar archivos AST
                for file_type in ['ast', 'nfa', 'dfa', 'dfa_min']:
                    png_file = f"{file_type}_expr_{i}.png"
                    dot_file = f"{file_type}_expr_{i}.dot"
                    
                    if os.path.exists(png_file):
                        png_count += 1
                    elif os.path.exists(dot_file):
                        dot_count += 1
        
        print(f"🖼️ Archivos PNG generados: {png_count}")
        if dot_count > 0:
            print(f"💾 Archivos DOT generados: {dot_count}")
        
        print(f"📊 Tasa de éxito: {(successful/len(results)*100):.1f}%")

def main():
    """Función principal del programa completo"""
    print("🎯 PROCESADOR COMPLETO DE EXPRESIONES REGULARES")
    print("=" * 60)
    print("Implementa los algoritmos requeridos por el Proyecto No. 1:")
    print("1. 📝 Shunting Yard (infix a postfix)")
    print("2. 🏗️ Construcción de Thompson (regex a NFA)")
    print("3. 🔄 Construcción de Subconjuntos (NFA a DFA)")
    print("4. ⚡ Minimización de DFA")
    print("5. 🧪 Simulación de NFA y DFAs")
    print("6. 🖼️ Visualización de todos los autómatas")
    print("=" * 60)
    
    processor = CompleteAutomataProcessor()
    
    # Verificar capacidades de visualización
    total_methods = (len(processor.ast_visualizer.png_methods) + 
                    len(processor.nfa_visualizer.png_methods) + 
                    len(processor.dfa_visualizer.png_methods))
    
    if total_methods > 0:
        print(f"🚀 Sistema listo para generar PNG")
    else:
        print("⚠️ PNG no disponible, usando visualización ASCII y archivos DOT")
    
    # Menú principal
    while True:
        try:
            print(f"\n🎛️ MENÚ PRINCIPAL:")
            print("1. 🎬 Procesar expresiones desde archivo")
            print("2. 🎮 Modo interactivo (una expresión)")
            print("3. 📋 Procesar expresiones del proyecto")
            print("4. ❓ Ayuda")
            print("5. 🚪 Salir")
            
            choice = input(f"\n👉 Selecciona opción (1-5): ").strip()
            
            if choice == '1':
                filename = input("📁 Nombre del archivo (Enter para 'expresiones.txt'): ").strip()
                if not filename:
                    filename = "expresiones.txt"
                processor.process_from_file(filename)
            
            elif choice == '2':
                regex = input("📤 Ingresa expresión regular: ").strip()
                if regex:
                    test_strings = input("🧪 Cadenas de prueba (separadas por comas, Enter para default): ").strip()
                    if test_strings:
                        test_strings = [s.strip() for s in test_strings.split(',')]
                    else:
                        test_strings = ["", "a", "b", "ab", "ba", "aa", "bb", "aaa", "bbb", "aba"]
                    
                    processor.process_expression_complete(regex, 1, test_strings)
            
            elif choice == '3':
                # Expresiones específicas del proyecto
                project_expressions = [
                    "(a*|b*)+",
                    "((ε|a)|b*)*",
                    "(a|b)*abb(a|b)*", 
                    "0?(1?)?0*"
                ]
                
                print(f"\n🎯 PROCESANDO EXPRESIONES DEL PROYECTO:")
                for expr in project_expressions:
                    print(f"   • {expr}")
                
                if input("\n¿Continuar? (s/n): ").lower() == 's':
                    for i, expr in enumerate(project_expressions, 1):
                        test_strings = ["", "a", "b", "aa", "bb", "ab", "ba", "aaa", "bbb", "aba"]
                        processor.process_expression_complete(expr, i, test_strings)
                        
                        if i < len(project_expressions):
                            try:
                                input(f"\n⏸️ Presiona Enter para continuar...")
                            except KeyboardInterrupt:
                                break
            
            elif choice == '4':
                print(f"\n📚 AYUDA DEL PROGRAMA")
                print("=" * 40)
                print("OPERADORES SOPORTADOS:")
                print("• * (Kleene) - cero o más repeticiones")
                print("• + (Plus) - una o más repeticiones") 
                print("• ? (Opcional) - cero o una repetición")
                print("• | (Unión) - alternativa")
                print("• () (Paréntesis) - agrupación")
                print("• ε (Epsilon) - cadena vacía")
                print("")
                print("EJEMPLOS:")
                print("• a* - cero o más 'a'")
                print("• (a|b)+ - una o más 'a' o 'b'")
                print("• a?b*c+ - 'a' opcional, cero o más 'b', una o más 'c'")
            
            elif choice == '5':
                print("👋 ¡Gracias por usar el procesador de expresiones regulares!")
                break
            
            else:
                print("❌ Opción inválida. Usa 1, 2, 3, 4 o 5.")
                
        except KeyboardInterrupt:
            print(f"\n\n👋 Programa interrumpido por el usuario")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()