"""
main.py - Programa principal para construcción y simulación de NFAs con Thompson
"""

import os
import sys
from regex_parser import RegexParser
from thompson_builder import ThompsonNFABuilder
from visualizer import ASTVisualizer, NFAVisualizer

class ThompsonNFADemo:
    """Clase principal que coordina todo el proceso"""
    
    def __init__(self):
        self.parser = RegexParser()
        self.nfa_builder = ThompsonNFABuilder()
        self.ast_visualizer = ASTVisualizer()
        self.nfa_visualizer = NFAVisualizer()
    
    def process_expression(self, regex, expr_num, test_strings=None):
        """Procesa una expresión regular completa"""
        print(f"\n{'='*80}")
        print(f"🎯 PROCESANDO EXPRESIÓN {expr_num}: {regex}")
        print(f"{'='*80}")
        
        try:
            # 1. Parsear expresión regular a AST
            print(f"\n📝 PASO 1: ANÁLISIS SINTÁCTICO")
            ast_root = self.parser.parse(regex)
            
            # 2. Mostrar AST
            print(f"\n🌳 PASO 2: VISUALIZACIÓN DEL AST")
            self.ast_visualizer.print_ast_ascii(ast_root)
            
            # 3. Generar imagen del AST
            ast_filename = f"ast_expr_{expr_num}"
            ast_png_success = self.ast_visualizer.create_ast_png(ast_root, ast_filename)
            
            # 4. Construir NFA usando Thompson
            print(f"\n🏗️ PASO 3: CONSTRUCCIÓN DEL NFA")
            nfa = self.nfa_builder.build_nfa_from_ast(ast_root)
            
            # 5. Validar NFA
            is_valid = self.nfa_builder.validate_nfa(nfa)
            if not is_valid:
                print("⚠️ NFA construido tiene problemas, pero continuaremos...")
            
            # 6. Mostrar estructura del NFA
            print(f"\n📋 PASO 4: ESTRUCTURA DEL NFA")
            self.nfa_visualizer.print_nfa_ascii(nfa)
            
            # 7. Generar imagen del NFA
            nfa_filename = f"nfa_expr_{expr_num}"
            nfa_png_success = self.nfa_visualizer.create_nfa_png(nfa, nfa_filename)
            
            # 8. Probar cadenas si se proporcionan
            if test_strings:
                print(f"\n🧪 PASO 5: SIMULACIÓN DEL NFA")
                print("=" * 50)
                self._test_strings(nfa, regex, test_strings)
            
            return {
                'ast': ast_root,
                'nfa': nfa,
                'ast_png': ast_png_success,
                'nfa_png': nfa_png_success,
                'valid': is_valid
            }
            
        except Exception as e:
            print(f"❌ Error procesando expresión '{regex}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _test_strings(self, nfa, regex, test_strings):
        """Prueba una lista de cadenas con el NFA"""
        results = []
        
        for i, test_string in enumerate(test_strings, 1):
            print(f"\n--- PRUEBA {i}/{len(test_strings)} ---")
            print(f"Cadena: '{test_string}'")
            print("-" * 30)
            
            # Simular NFA
            accepted = nfa.simulate(test_string)
            result = "SÍ" if accepted else "NO"
            results.append((test_string, accepted))
            
            print(f"\n🎯 RESULTADO: '{test_string}' ∈ L({regex}): {result}")
        
        # Resumen de pruebas
        print(f"\n📊 RESUMEN DE PRUEBAS:")
        accepted_count = sum(1 for _, accepted in results if accepted)
        print(f"   ✅ Aceptadas: {accepted_count}/{len(results)}")
        print(f"   ❌ Rechazadas: {len(results) - accepted_count}/{len(results)}")
        
        return results
    
    def run_demo(self):
        """Ejecuta la demostración completa con las expresiones requeridas"""
        expressions = [
            "(a*|b*)+",
            "((ε|a)|b*)*",
            "(a|b)*abb(a|b)*",
            "0?(1?)?0*"
        ]
        
        # Cadenas de prueba para cada expresión
        test_cases = [
            # Para (a*|b*)+
            ["", "a", "b", "aa", "bb", "aaa", "bbb", "ab", "ba", "aabb"],
            
            # Para ((ε|a)|b*)*
            ["", "a", "b", "aa", "bb", "ab", "ba", "bbb", "aaabbb", "ababa"],
            
            # Para (a|b)*abb(a|b)*
            ["abb", "aabb", "abba", "babb", "abbb", "aabba", "ab", "", "ababb", "abbabb"],
            
            # Para 0?(1?)?0*
            ["", "0", "1", "01", "10", "00", "000", "010", "100", "110"]
        ]
        
        print(f"\n🚀 DEMOSTRACIÓN COMPLETA - ALGORITMO DE THOMPSON")
        print("=" * 80)
        print(f"📋 {len(expressions)} expresiones regulares a procesar")
        print(f"🧪 Cada expresión será probada con {len(test_cases[0])} cadenas")
        print(f"🖼️ Se generarán imágenes de AST y NFA")
        print("=" * 80)
        
        results = []
        total_png_count = 0
        
        for i, expr in enumerate(expressions, 1):
            test_strings = test_cases[i-1] if i-1 < len(test_cases) else []
            
            result = self.process_expression(expr, i, test_strings)
            
            if result:
                results.append((expr, True, result['ast_png'], result['nfa_png']))
                if result['ast_png']:
                    total_png_count += 1
                if result['nfa_png']:
                    total_png_count += 1
            else:
                results.append((expr, False, False, False))
            
            # Pausa entre expresiones (excepto la última)
            if i < len(expressions):
                print(f"\n{'='*60}")
                try:
                    input(f"⏸️  Presiona Enter para continuar con la siguiente expresión...")
                except KeyboardInterrupt:
                    print(f"\n👋 Demostración interrumpida por el usuario")
                    break
        
        # Resumen final
        self._print_final_summary(results, total_png_count)
    
    def run_interactive_mode(self):
        """Modo interactivo para probar expresiones y cadenas"""
        print(f"\n🎮 MODO INTERACTIVO")
        print("=" * 50)
        print("Ingresa expresiones regulares y cadenas para probar")
        print("\nComandos especiales:")
        print("  'demo'  - ejecutar demostración completa")
        print("  'quit'  - salir del programa")
        print("  'help'  - mostrar esta ayuda")
        print("  'clear' - limpiar pantalla")
        
        expr_counter = 1
        
        while True:
            try:
                print(f"\n{'─'*50}")
                user_input = input("🔤 Expresión regular (o comando): ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 ¡Hasta luego!")
                    break
                
                elif user_input.lower() == 'demo':
                    self.run_demo()
                    continue
                
                elif user_input.lower() == 'help':
                    self._print_help()
                    continue
                
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                
                elif not user_input:
                    continue
                
                # Procesar expresión
                print(f"\n🔄 Procesando: {user_input}")
                result = self.process_expression(user_input, expr_counter)
                
                if not result:
                    print("❌ Error procesando la expresión")
                    continue
                
                # Modo de prueba de cadenas
                self._interactive_string_testing(result['nfa'], user_input)
                
                expr_counter += 1
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _interactive_string_testing(self, nfa, regex):
        """Modo interactivo para probar cadenas"""
        print(f"\n🧪 PROBADOR INTERACTIVO DE CADENAS")
        print("=" * 40)
        print("Ingresa cadenas para probar (Enter vacío para terminar)")
        print("Comandos: 'back' para volver, 'trace <cadena>' para ver traza detallada")
        
        test_counter = 1
        
        while True:
            try:
                user_input = input(f"\nCadena {test_counter}: ").strip()
                
                if user_input == "":
                    break
                elif user_input.lower() == 'back':
                    break
                elif user_input.startswith('trace '):
                    # Traza detallada
                    test_string = user_input[6:]  # Remover 'trace '
                    print(f"\n🔍 TRAZA DETALLADA PARA: '{test_string}'")
                    self.nfa_visualizer.print_simulation_trace(nfa, test_string)
                else:
                    # Simulación normal
                    print(f"\n--- Probando '{user_input}' ---")
                    accepted = nfa.simulate(user_input)
                    result = "SÍ" if accepted else "NO"
                    print(f"🎯 Resultado: '{user_input}' ∈ L({regex}): {result}")
                    
                    test_counter += 1
                    
            except KeyboardInterrupt:
                print(f"\n⏪ Volviendo al menú principal...")
                break
    
    def run_from_file(self, filename):
        """Procesa expresiones desde un archivo"""
        if not os.path.exists(filename):
            print(f"❌ Archivo '{filename}' no encontrado")
            
            # Ofrecer crear archivo con expresiones por defecto
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
                expressions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not expressions:
                print(f"❌ No se encontraron expresiones válidas en '{filename}'")
                return
            
            print(f"✅ Leídas {len(expressions)} expresiones de '{filename}'")
            
        except Exception as e:
            print(f"❌ Error leyendo archivo: {e}")
            return
        
        # Procesar expresiones
        print(f"\n🔄 Procesando {len(expressions)} expresiones del archivo...")
        
        results = []
        
        for i, expr in enumerate(expressions, 1):
            # Cadenas de prueba básicas para todas las expresiones
            test_strings = ["", "a", "b", "ab", "ba", "aa", "bb", "aaa", "bbb", "aba"]
            
            print(f"\n{'='*60}")
            print(f"Expresión {i}/{len(expressions)} del archivo")
            
            result = self.process_expression(expr, i, test_strings)
            results.append(result)
            
            # Pausa entre expresiones (excepto la última)
            if i < len(expressions):
                try:
                    input(f"\n⏸️ Presiona Enter para continuar...")
                except KeyboardInterrupt:
                    print(f"\n👋 Procesamiento interrumpido")
                    break
        
        # Resumen final
        successful = sum(1 for r in results if r is not None)
        print(f"\n📊 PROCESAMIENTO COMPLETO:")
        print(f"   ✅ Expresiones procesadas: {successful}/{len(expressions)}")
    
    def _create_default_file(self, filename):
        """Crea archivo con las expresiones por defecto"""
        default_expressions = [
            "# Expresiones regulares para demostración",
            "# Algoritmo de Thompson - Construcción de NFAs",
            "",
            "(a*|b*)+",
            "((ε|a)|b*)*",
            "(a|b)*abb(a|b)*",
            "0?(1?)?0*"
        ]
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for expr in default_expressions:
                    f.write(expr + '\n')
            return True
        except Exception as e:
            print(f"❌ Error creando archivo: {e}")
            return False
    
    def _print_help(self):
        """Imprime ayuda del programa"""
        print(f"\n📚 AYUDA DEL PROGRAMA")
        print("=" * 40)
        print("EXPRESIONES REGULARES SOPORTADAS:")
        print("• Operadores: * (Kleene), + (una o más), ? (opcional)")
        print("• Unión: | (a|b)")
        print("• Concatenación: ab (implícita)")
        print("• Paréntesis: (ab)*")
        print("• Epsilon: ε")
        print("")
        print("EJEMPLOS:")
        print("• a*        - cero o más 'a'")
        print("• (a|b)+    - una o más 'a' o 'b'")
        print("• a?b*c+    - 'a' opcional, cero o más 'b', una o más 'c'")
        print("• (ab)*     - cero o más repeticiones de 'ab'")
        print("")
        print("COMANDOS INTERACTIVOS:")
        print("• trace <cadena> - muestra traza detallada de simulación")
        print("• back          - volver al menú anterior")
        print("• quit          - salir del programa")
    
    def _print_final_summary(self, results, png_count):
        """Imprime resumen final de la demostración"""
        print(f"\n🎉 RESUMEN FINAL DE LA DEMOSTRACIÓN")
        print("=" * 80)
        
        successful = sum(1 for _, success, _, _ in results if success)
        print(f"✅ Expresiones procesadas exitosamente: {successful}/{len(results)}")
        print(f"🖼️ Imágenes PNG generadas: {png_count}")
        
        print(f"\n📁 ARCHIVOS GENERADOS:")
        for i, (expr, success, ast_png, nfa_png) in enumerate(results, 1):
            if success:
                print(f"\n--- Expresión {i}: {expr} ---")
                
                # Verificar archivos AST
                ast_png_file = f"ast_expr_{i}.png"
                ast_dot_file = f"ast_expr_{i}.dot"
                
                if os.path.exists(ast_png_file):
                    size = os.path.getsize(ast_png_file)
                    print(f"🌳 AST: {ast_png_file} ({size} bytes)")
                elif os.path.exists(ast_dot_file):
                    print(f"🌳 AST: {ast_dot_file} (convertir con dot)")
                
                # Verificar archivos NFA
                nfa_png_file = f"nfa_expr_{i}.png"
                nfa_dot_file = f"nfa_expr_{i}.dot"
                
                if os.path.exists(nfa_png_file):
                    size = os.path.getsize(nfa_png_file)
                    print(f"🤖 NFA: {nfa_png_file} ({size} bytes)")
                elif os.path.exists(nfa_dot_file):
                    print(f"🤖 NFA: {nfa_dot_file} (convertir con dot)")
        
        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   • Total de expresiones: {len(results)}")
        print(f"   • Procesadas exitosamente: {successful}")
        print(f"   • Tasa de éxito: {(successful/len(results)*100):.1f}%")
        print(f"   • Archivos generados: {png_count} imágenes + archivos DOT")

def main():
    """Función principal del programa"""
    print("🎯 CONSTRUCTOR DE NFA CON ALGORITMO DE THOMPSON")
    print("=" * 60)
    print("Este programa:")
    print("1. 📝 Convierte expresiones regulares a AST")
    print("2. 🏗️ Construye NFAs usando el algoritmo de Thompson") 
    print("3. 🖼️ Genera visualizaciones (PNG/DOT)")
    print("4. 🧪 Simula NFAs para reconocer cadenas")
    print("=" * 60)
    
    demo = ThompsonNFADemo()
    
    # Verificar capacidades de visualización
    if demo.ast_visualizer.png_methods or demo.nfa_visualizer.png_methods:
        png_methods = len(demo.ast_visualizer.png_methods)
        print(f"🚀 Listo para generar PNG con {png_methods} métodos disponibles")
    else:
        print("⚠️ PNG no disponible, pero continuaremos con visualización ASCII")
    
    # Menú principal
    while True:
        try:
            print(f"\n🎛️ MENÚ PRINCIPAL:")
            print("1. 🎬 Demostración completa (expresiones predefinidas)")
            print("2. 🎮 Modo interactivo (ingresar expresiones manualmente)")
            print("3. 📁 Leer desde archivo")
            print("4. ❓ Ayuda")
            print("5. 🚪 Salir")
            
            choice = input(f"\n👉 Selecciona opción (1-5): ").strip()
            
            if choice == '1':
                demo.run_demo()
            
            elif choice == '2':
                demo.run_interactive_mode()
            
            elif choice == '3':
                filename = input("📁 Nombre del archivo (Enter para 'expresiones.txt'): ").strip()
                if not filename:
                    filename = "expresiones.txt"
                demo.run_from_file(filename)
            
            elif choice == '4':
                demo._print_help()
            
            elif choice == '5':
                print("👋 ¡Gracias por usar el programa!")
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