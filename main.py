"""
Archivo principal del proyecto
Autores: [Persona 1] y [Persona 2]
Fecha: Octubre 2024
"""

from cnf_converter import CNFConverter
from cyk_algorithm import CYKParser, print_parse_tree


# Gramática del proyecto (ya en CNF)
ENGLISH_GRAMMAR = {
    'S': [['NP', 'VP']],
    'VP': [['VP', 'PP'], ['V', 'NP'], ['cooks'], ['drinks'], ['eats'], ['cuts']],
    'PP': [['P', 'NP']],
    'NP': [['Det', 'N'], ['he'], ['she']],
    'V': [['cooks'], ['drinks'], ['eats'], ['cuts']],
    'P': [['in'], ['with']],
    'N': [['cat'], ['dog'], ['beer'], ['cake'], ['juice'], ['meat'], ['soup'],
          ['fork'], ['knife'], ['oven'], ['spoon']],
    'Det': [['a'], ['the']]
}


def print_header():
    """Imprime el encabezado"""
    print("=" * 80)
    print("🎓 ALGORITMO CYK - COCKE-YOUNGER-KASAMI")
    print("   Teoría de la Computación 2024 - Proyecto 2")
    print("=" * 80)


def show_grammar(grammar):
    """Muestra la gramática"""
    print("\n📖 GRAMÁTICA UTILIZADA")
    print("=" * 80)
    
    for nt in sorted(grammar.keys()):
        prods = grammar[nt]
        prod_strs = [' '.join(p) for p in prods]
        print(f"{nt:5} → {' | '.join(prod_strs)}")
    
    print("=" * 80)


def run_examples(parser):
    """Ejecuta ejemplos predefinidos"""
    print("\n" + "=" * 80)
    print("🔍 EJEMPLOS DE PRUEBA")
    print("=" * 80)
    
    examples = [
        # Ejemplos exitosos (válidos)
        ("she eats a cake with a fork", "Frase compleja con PP"),
        ("the cat drinks the beer", "Frase simple"),
        ("he cooks the meat", "Con pronombre"),
        ("she eats the cake in the oven", "Frase con PP locativo"),
        ("the dog cuts the meat with a knife", "Frase compleja con instrumento"),
        
        # Ejemplos de error (inválidos)
        ("she eat cake", "ERROR: falta determinante"),
        ("cat the drinks beer", "ERROR: orden incorrecto"),
        ("she eats the with fork", "ERROR: falta sustantivo en PP"),
        ("he cat the eats", "ERROR: estructura incorrecta"),
        ("a fork with", "ERROR: frase incompleta")
    ]
    
    for i, (phrase, description) in enumerate(examples, 1):
        print(f"\n{'-'*80}")
        print(f"Ejemplo {i}: {description}")
        print(f"Frase: \"{phrase}\"")
        print('-'*80)
        
        accepted, time_ms, _ = parser.parse(phrase)
        
        status = "✓ ACEPTADA" if accepted else "✗ RECHAZADA"
        print(f"\nResultado: {status}")
        print(f"Tiempo: {time_ms:.4f} ms")
        
        if accepted:
            words = phrase.split()
            parser.print_table(words)
            
            tree = parser.build_parse_tree(words)
            if tree:
                print("\n🌳 Árbol de Parseo:")
                print_parse_tree(tree)
        
        print()


def interactive_mode(parser):
    """Modo interactivo"""
    print("\n" + "=" * 80)
    print("💡 MODO INTERACTIVO")
    print("=" * 80)
    print("\nIngrese frases para analizar.")
    print("Escriba 'salir' para terminar.\n")
    
    try:
        while True:
            phrase = input("Frase: ").strip()
            
            if not phrase:
                continue
            
            if phrase.lower() in ['exit', 'salir', 'quit']:
                break
            
            print()
            accepted, time_ms, _ = parser.parse(phrase)
            
            status = "✓ ACEPTADA" if accepted else "✗ RECHAZADA"
            print(f"→ {status}")
            print(f"→ Tiempo: {time_ms:.4f} ms")
            
            if accepted:
                words = phrase.split()
                tree = parser.build_parse_tree(words)
                if tree:
                    print("\n🌳 Árbol de Parseo:")
                    print_parse_tree(tree)
            
            print()
    
    except KeyboardInterrupt:
        print("\n")
    
    print("👋 ¡Gracias por usar el analizador CYK!")


def test_all_grammar_productions(parser):
    """Prueba todas las producciones de la gramática"""
    print("\n" + "=" * 80)
    print("🧪 PRUEBA EXHAUSTIVA DE LA GRAMÁTICA")
    print("=" * 80)
    
    # Prueba todas las combinaciones de verbos y objetos
    verbs = ['eats', 'drinks', 'cooks', 'cuts']
    objects = ['cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup']
    determiners = ['a', 'the']
    subjects = ['he', 'she', 'the cat', 'the dog']
    prepositions = ['in', 'with']
    instruments = ['fork', 'knife', 'spoon', 'oven']
    
    # Generar y probar frases simples
    count_valid = 0
    count_total = 0
    
    print("\n1. Frases simples (SVO):")
    print("-" * 40)
    
    for subject in subjects[:2]:  # Solo pronombres
        for verb in verbs:
            for det in determiners:
                for obj in objects:
                    phrase = f"{subject} {verb} {det} {obj}"
                    accepted, time_ms, _ = parser.parse(phrase)
                    status = "✓" if accepted else "✗"
                    print(f"{status} \"{phrase}\" ({time_ms:.2f} ms)")
                    
                    count_total += 1
                    if accepted:
                        count_valid += 1
    
    print(f"\nResumen: {count_valid}/{count_total} frases válidas")
    
    # Generar y probar frases con preposiciones
    count_valid = 0
    count_total = 0
    
    print("\n2. Frases con preposiciones (SVOP):")
    print("-" * 40)
    
    for subject in subjects[2:]:  # Solo NPs
        for verb in verbs:
            for det1 in determiners:
                for obj in objects[:3]:  # Limitar para no generar demasiados ejemplos
                    for prep in prepositions:
                        for det2 in determiners:
                            for inst in instruments[:2]:  # Limitar
                                phrase = f"{subject} {verb} {det1} {obj} {prep} {det2} {inst}"
                                accepted, time_ms, _ = parser.parse(phrase)
                                status = "✓" if accepted else "✗"
                                print(f"{status} \"{phrase}\" ({time_ms:.2f} ms)")
                                
                                count_total += 1
                                if accepted:
                                    count_valid += 1
    
    print(f"\nResumen: {count_valid}/{count_total} frases válidas")
    
    # Probar algunos casos inválidos específicos
    print("\n3. Casos inválidos específicos:")
    print("-" * 40)
    
    invalid_cases = [
        "cat eats the", 
        "the eats cat", 
        "eats the cat",
        "he eats",
        "the cat",
        "with a fork",
        "the cat with the dog",
        "he she",
        "eats drinks",
        "the the cat"
    ]
    
    for phrase in invalid_cases:
        accepted, time_ms, _ = parser.parse(phrase)
        status = "✓" if accepted else "✗"
        print(f"{status} \"{phrase}\" ({time_ms:.2f} ms)")
    
    print("\nPrueba completa.")
    input("\nPresione Enter para continuar...")


def main():
    """Función principal"""
    
    print_header()
    
    # Verificar CNF
    print("\n📋 Verificando gramática...")
    is_cnf = CNFConverter.is_in_cnf(ENGLISH_GRAMMAR)
    print(f"¿Está en CNF? {'✓ Sí' if is_cnf else '✗ No'}")
    
    # Mostrar gramática
    show_grammar(ENGLISH_GRAMMAR)
    
    # Crear parser
    print("\n⚙️ Inicializando parser CYK...")
    parser = CYKParser(ENGLISH_GRAMMAR)
    print("✓ Parser listo")
    
    # Menú
    while True:
        print("\n" + "=" * 80)
        print("📋 MENÚ PRINCIPAL")
        print("=" * 80)
        print("\n1. Ejecutar ejemplos (10 casos de prueba)")
        print("2. Modo interactivo")
        print("3. Analizar frase específica")
        print("4. Ver gramática")
        print("5. Prueba exhaustiva de la gramática")
        print("6. Salir")
        
        try:
            opcion = input("\nOpción (1-6): ").strip()
            
            if opcion == '1':
                run_examples(parser)
                input("\nPresione Enter para continuar...")
            
            elif opcion == '2':
                interactive_mode(parser)
            
            elif opcion == '3':
                phrase = input("\nIngrese la frase: ").strip()
                if phrase:
                    print()
                    accepted, time_ms, _ = parser.parse(phrase)
                    print(f"Resultado: {'✓ ACEPTADA' if accepted else '✗ RECHAZADA'}")
                    print(f"Tiempo: {time_ms:.4f} ms")
                    
                    if accepted:
                        words = phrase.split()
                        parser.print_table(words)
                        tree = parser.build_parse_tree(words)
                        if tree:
                            print("\n🌳 Árbol de Parseo:")
                            print_parse_tree(tree)
                
                input("\nPresione Enter para continuar...")
            
            elif opcion == '4':
                show_grammar(ENGLISH_GRAMMAR)
                input("\nPresione Enter para continuar...")
            
            elif opcion == '5':
                test_all_grammar_productions(parser)
            
            elif opcion == '6':
                print("\n👋 ¡Hasta luego!")
                break
            
            else:
                print("\n⚠ Opción inválida")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()