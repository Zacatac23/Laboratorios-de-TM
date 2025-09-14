import re
from typing import Dict, List, Set, Tuple
from itertools import combinations

class CFGProcessor:
    def __init__(self):
        self.productions = {}  # Dict[str, List[str]]
        self.terminals = set()
        self.non_terminals = set()
        
    def validate_production_line(self, line: str) -> bool:
        """
        Valida que una línea de producción esté bien formada usando regex.
        Formato esperado: A -> alpha | beta | gamma
        donde A es no-terminal (mayúscula) y alpha, beta, gamma son cadenas de terminales/no-terminales
        """
        # Regex para validar producciones
        # [A-Z] -> símbolo inicial (no-terminal)
        # \s*->\s* -> flecha con espacios opcionales
        # ([a-zA-Z0-9ε]|\||\s)* -> cuerpo de producción (terminales, no-terminales, épsilon, OR, espacios)
        pattern = r'^[A-Z]\s*->\s*([a-zA-Z0-9ε]|\||\s)+$'
        
        if not re.match(pattern, line.strip()):
            return False
            
        # Validar que después de la flecha hay contenido válido
        parts = line.split('->')
        if len(parts) != 2:
            return False
            
        left_side = parts[0].strip()
        right_side = parts[1].strip()
        
        # Lado izquierdo debe ser un solo no-terminal
        if len(left_side) != 1 or not left_side.isupper():
            return False
            
        # Validar que el lado derecho tenga formato correcto
        productions = [p.strip() for p in right_side.split('|')]
        for prod in productions:
            if not prod:  # Producción vacía después del split
                return False
            # Cada producción debe contener solo letras, números o épsilon
            if not re.match(r'^[a-zA-Z0-9ε]*$', prod):
                return False
                
        return True
    
    def validate_symbols(self) -> bool:
        """
        Valida que todos los no-terminales usados en producciones estén definidos.
        """
        defined_symbols = set(self.productions.keys())
        used_symbols = set()
        
        # Recopilar todos los símbolos usados en las producciones
        for productions in self.productions.values():
            for production in productions:
                for char in production:
                    if char.isupper() and char != 'ε':
                        used_symbols.add(char)
        
        # Verificar si hay símbolos usados pero no definidos
        undefined_symbols = used_symbols - defined_symbols
        if undefined_symbols:
            print(f"❌ ERROR: Símbolos no definidos encontrados: {sorted(undefined_symbols)}")
            return False
            
        return True
    
    def parse_grammar_file(self, filename: str) -> bool:
        """
        Carga y parsea un archivo de gramática.
        Retorna True si el archivo es válido, False si hay errores.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            print(f"\n=== Cargando gramática desde {filename} ===")
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:  # Saltar líneas vacías
                    continue
                    
                print(f"Línea {line_num}: {line}")
                
                # Validar formato de la línea
                if not self.validate_production_line(line):
                    print(f"❌ ERROR: Línea {line_num} tiene formato inválido: {line}")
                    return False
                    
                # Parsear la producción
                parts = line.split('->')
                left_side = parts[0].strip()
                right_side = parts[1].strip()
                
                # Agregar no-terminal
                self.non_terminals.add(left_side)
                
                # Parsear producciones del lado derecho
                productions = [p.strip() for p in right_side.split('|')]
                
                if left_side not in self.productions:
                    self.productions[left_side] = []
                    
                for prod in productions:
                    self.productions[left_side].append(prod)
                    
                    # Identificar terminales y no-terminales
                    for char in prod:
                        if char.isupper() and char != 'ε':
                            self.non_terminals.add(char)
                        elif char.islower() or char.isdigit():
                            self.terminals.add(char)
                            
            print("✅ Gramática cargada exitosamente")
            return True
            
        except FileNotFoundError:
            print(f"❌ ERROR: No se pudo encontrar el archivo {filename}")
            return False
        except Exception as e:
            print(f"❌ ERROR: Error al leer el archivo: {e}")
            return False
    
    def print_grammar(self, title: str = "Gramática"):
        """Imprime la gramática actual de forma legible."""
        print(f"\n=== {title} ===")
        for non_terminal in sorted(self.productions.keys()):
            productions_str = " | ".join(self.productions[non_terminal])
            print(f"{non_terminal} -> {productions_str}")
    
    def find_nullable_symbols(self) -> Set[str]:
        """
        Encuentra todos los símbolos anulables (que pueden derivar ε).
        Retorna un conjunto de símbolos anulables.
        """
        print("\n=== Paso 1: Encontrando símbolos anulables ===")
        
        nullable = set()
        changed = True
        iteration = 1
        
        while changed:
            changed = False
            print(f"\nIteración {iteration}:")
            
            for non_terminal, productions in self.productions.items():
                if non_terminal in nullable:
                    continue
                    
                for production in productions:
                    # Si la producción es ε, el símbolo es anulable
                    if production == 'ε':
                        nullable.add(non_terminal)
                        print(f"  {non_terminal} es anulable (producción directa: {non_terminal} -> ε)")
                        changed = True
                        break
                    
                    # Si todos los símbolos de la producción son anulables, 
                    # entonces este símbolo también es anulable
                    if production and all(symbol in nullable for symbol in production):
                        nullable.add(non_terminal)
                        print(f"  {non_terminal} es anulable (todos los símbolos en '{production}' son anulables)")
                        changed = True
                        break
            
            if not changed:
                print(f"  No se encontraron nuevos símbolos anulables")
                
            iteration += 1
        
        print(f"\nSímbolos anulables encontrados: {sorted(nullable)}")
        return nullable
    
    def generate_combinations(self, production: str, nullable: Set[str]) -> List[str]:
        """
        Genera todas las combinaciones posibles de una producción 
        considerando los símbolos anulables.
        """
        if not production or production == 'ε':
            return ['ε']
        
        # Encontrar posiciones de símbolos anulables
        nullable_positions = []
        for i, symbol in enumerate(production):
            if symbol in nullable:
                nullable_positions.append(i)
        
        if not nullable_positions:
            return [production]
        
        # Generar todas las combinaciones posibles (2^n)
        combinations_list = []
        
        # Para cada subset de posiciones anulables
        for r in range(len(nullable_positions) + 1):
            for positions_to_remove in combinations(nullable_positions, r):
                # Crear nueva producción removiendo símbolos en las posiciones seleccionadas
                new_production = ''
                for i, symbol in enumerate(production):
                    if i not in positions_to_remove:
                        new_production += symbol
                
                if not new_production:
                    new_production = 'ε'
                    
                combinations_list.append(new_production)
        
        return list(set(combinations_list))  # Remover duplicados
    
    def eliminate_epsilon_productions(self):
        """
        Elimina las producciones-ε de la gramática.
        Muestra el proceso paso a paso.
        """
        print("\n" + "="*60)
        print("ALGORITMO PARA ELIMINAR PRODUCCIONES-ε")
        print("="*60)
        
        # Paso 1: Encontrar símbolos anulables
        nullable = self.find_nullable_symbols()
        
        # Paso 2: Generar nuevas producciones
        print("\n=== Paso 2: Generando nuevas producciones ===")
        
        new_productions = {}
        
        for non_terminal, productions in self.productions.items():
            new_productions[non_terminal] = set()  # Usar set para evitar duplicados
            
            print(f"\nProcesando {non_terminal}:")
            
            for production in productions:
                if production == 'ε':
                    print(f"  Omitiendo producción ε: {non_terminal} -> {production}")
                    continue
                
                # Generar todas las combinaciones
                combinations = self.generate_combinations(production, nullable)
                
                print(f"  Para {non_terminal} -> {production}:")
                for combo in combinations:
                    if combo != 'ε':  # No agregar producciones ε
                        new_productions[non_terminal].add(combo)
                        print(f"    Agregando: {non_terminal} -> {combo}")
                    else:
                        print(f"    Omitiendo: {non_terminal} -> {combo} (es ε)")
        
        # Convertir sets a listas
        for non_terminal in new_productions:
            new_productions[non_terminal] = list(new_productions[non_terminal])
            if not new_productions[non_terminal]:  # Si no hay producciones
                new_productions[non_terminal] = []
        
        # Remover símbolos que solo tenían producciones ε
        symbols_to_remove = []
        for non_terminal, productions in new_productions.items():
            if not productions:
                symbols_to_remove.append(non_terminal)
                print(f"\nEliminando símbolo {non_terminal} (solo tenía producciones-ε)")
        
        for symbol in symbols_to_remove:
            del new_productions[symbol]
            self.non_terminals.discard(symbol)
        
        self.productions = new_productions
        
        print(f"\n=== Resultado: Gramática sin producciones-ε ===")
        self.print_grammar("Gramática sin producciones-ε")

def demonstrate_with_error(filename: str):
    """Demuestra la validación con errores introducidos."""
    print(f"\n{'='*60}")
    print(f"DEMOSTRACIÓN DE VALIDACIÓN CON ERRORES - {filename}")
    print(f"{'='*60}")
    
    # Crear archivo con errores para demostración
    error_filename = f"error_{filename}"
    
    # Leer archivo original y introducir errores
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Introducir algunos errores
        error_lines = []
        for i, line in enumerate(lines):
            if i == 0:
                # Error: usar minúscula en lado izquierdo
                error_lines.append(line.replace('S', 's', 1))
            elif i == 1:
                # Error: flecha incorrecta
                error_lines.append(line.replace('->', '=>'))
            else:
                error_lines.append(line)
        
        # Agregar línea con formato completamente incorrecto
        error_lines.append("X Y Z invalid format\n")
        
        with open(error_filename, 'w', encoding='utf-8') as f:
            f.writelines(error_lines)
        
        # Procesar archivo con errores
        processor = CFGProcessor()
        success = processor.parse_grammar_file(error_filename)
        
        if not success:
            print("✅ Validación funcionó correctamente - errores detectados")
        
        # Limpiar archivo temporal
        import os
        os.remove(error_filename)
        
    except Exception as e:
        print(f"Error en demostración: {e}")

def main():
    """Función principal del programa."""
    print("PROCESADOR DE GRAMÁTICAS LIBRES DE CONTEXTO")
    print("Eliminación de Producciones-ε")
    print("="*60)
    
    # Lista de archivos de gramáticas
    grammar_files = ["grammar1.txt", "grammar2.txt"]
    
    for filename in grammar_files:
        print(f"\n{'='*80}")
        print(f"PROCESANDO {filename.upper()}")
        print(f"{'='*80}")
        
        processor = CFGProcessor()
        
        # Cargar y procesar gramática
        if processor.parse_grammar_file(filename):
            processor.print_grammar("Gramática Original")
            processor.eliminate_epsilon_productions()
            
            # Demostrar validación con errores (solo para el primer archivo)
            if filename == grammar_files[0]:
                demonstrate_with_error(filename)
        else:
            print(f"❌ No se pudo procesar {filename}")
            continue
    
    print(f"\n{'='*80}")
    print("PROCESAMIENTO COMPLETADO")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()