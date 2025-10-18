"""
Módulo de Conversión a Forma Normal de Chomsky (CNF)
Persona 1: Algoritmo de Simplificación de Gramáticas

Autores: [Persona 1]
Fecha: Octubre 2024
"""

from typing import Dict, List, Set


class CNFConverter:
    """
    Conversor de gramáticas a Forma Normal de Chomsky.
    
    Una gramática está en CNF si todas sus producciones son:
    - A → BC (dos no-terminales)
    - A → a (un terminal)
    """
    
    @staticmethod
    def is_terminal(symbol: str) -> bool:
        """
        Verifica si un símbolo es terminal.
        
        Args:
            symbol: Símbolo a verificar
            
        Returns:
            True si es terminal, False si es no-terminal
        """
        return symbol and len(symbol) > 0 and symbol[0].islower()
    
    @staticmethod
    def is_non_terminal(symbol: str) -> bool:
        """
        Verifica si un símbolo es no-terminal.
        
        Args:
            symbol: Símbolo a verificar
            
        Returns:
            True si es no-terminal, False si es terminal
        """
        return not CNFConverter.is_terminal(symbol)
    
    @staticmethod
    def is_in_cnf(grammar: Dict[str, List[List[str]]]) -> bool:
        """
        Verifica si una gramática está en Forma Normal de Chomsky.
        
        Args:
            grammar: Diccionario con la gramática
            
        Returns:
            True si está en CNF, False en caso contrario
        """
        for non_terminal, productions in grammar.items():
            for prod in productions:
                # Producción vacía
                if len(prod) == 0:
                    return False
                
                # Producción unitaria
                elif len(prod) == 1:
                    # Debe ser terminal
                    if not CNFConverter.is_terminal(prod[0]):
                        return False
                
                # Producción binaria
                elif len(prod) == 2:
                    # Ambos deben ser no-terminales
                    if CNFConverter.is_terminal(prod[0]) or CNFConverter.is_terminal(prod[1]):
                        return False
                
                # Producción con más de 2 símbolos
                else:
                    return False
        
        return True
    
    @staticmethod
    def find_nullables(grammar: Dict[str, List[List[str]]]) -> Set[str]:
        """
        Encuentra los símbolos que pueden derivar la cadena vacía (epsilon).
        
        Args:
            grammar: Diccionario con la gramática
            
        Returns:
            Conjunto de símbolos anulables
        """
        nullables = set()
        changed = True
        
        while changed:
            changed = False
            
            for nt, prods in grammar.items():
                if nt in nullables:
                    continue
                
                for prod in prods:
                    # Producción epsilon directa
                    if len(prod) == 1 and prod[0] == 'ε':
                        nullables.add(nt)
                        changed = True
                        break
                    
                    # Todos los símbolos son nullables
                    if len(prod) > 0 and all(symbol in nullables for symbol in prod):
                        nullables.add(nt)
                        changed = True
                        break
        
        return nullables
    
    @staticmethod
    def _generate_variants(prod: List[str], nullables: Set[str]) -> List[List[str]]:
        """
        Genera todas las variantes de una producción eliminando nullables.
        
        Args:
            prod: Producción original
            nullables: Conjunto de símbolos anulables
            
        Returns:
            Lista de todas las variantes posibles
        """
        if not prod:
            return [[]]
        
        first, *rest = prod
        rest_variants = CNFConverter._generate_variants(rest, nullables)
        
        variants = []
        for variant in rest_variants:
            variants.append([first] + variant)
            if first in nullables:
                variants.append(variant)
        
        return variants
    
    @staticmethod
    def eliminate_epsilon(grammar: Dict[str, List[List[str]]]) -> Dict[str, List[List[str]]]:
        """
        Elimina todas las producciones epsilon de la gramática.
        
        Args:
            grammar: Gramática original
            
        Returns:
            Nueva gramática sin producciones epsilon
        """
        nullables = CNFConverter.find_nullables(grammar)
        new_grammar = {}
        
        for nt, prods in grammar.items():
            new_grammar[nt] = []
            
            for prod in prods:
                if len(prod) == 1 and prod[0] == 'ε':
                    continue
                
                variants = CNFConverter._generate_variants(prod, nullables)
                
                for variant in variants:
                    if len(variant) > 0 and variant not in new_grammar[nt]:
                        new_grammar[nt].append(variant)
        
        return new_grammar
    
    @staticmethod
    def eliminate_unit_productions(grammar: Dict[str, List[List[str]]]) -> Dict[str, List[List[str]]]:
        """
        Elimina producciones unitarias de la forma A → B.
        
        Args:
            grammar: Gramática original
            
        Returns:
            Nueva gramática sin producciones unitarias
        """
        unit_pairs = {nt: {nt} for nt in grammar.keys()}
        
        changed = True
        while changed:
            changed = False
            
            for A, prods in grammar.items():
                for prod in prods:
                    if len(prod) == 1 and not CNFConverter.is_terminal(prod[0]):
                        B = prod[0]
                        
                        if B in unit_pairs:
                            for C in unit_pairs[B]:
                                if C not in unit_pairs[A]:
                                    unit_pairs[A].add(C)
                                    changed = True
        
        new_grammar = {}
        for A, reachable in unit_pairs.items():
            new_grammar[A] = []
            
            for B in reachable:
                if B in grammar:
                    for prod in grammar[B]:
                        if len(prod) != 1 or CNFConverter.is_terminal(prod[0]):
                            if prod not in new_grammar[A]:
                                new_grammar[A].append(prod)
        
        return new_grammar
    
    @staticmethod
    def normalize_terminals(grammar: Dict[str, List[List[str]]]) -> Dict[str, List[List[str]]]:
        """
        Reemplaza terminales en producciones mixtas por nuevos no-terminales.
        
        Args:
            grammar: Gramática a normalizar
            
        Returns:
            Nueva gramática con terminales normalizados
        """
        new_grammar = {}
        terminal_vars = {}
        counter = 0
        
        for nt, prods in grammar.items():
            new_grammar[nt] = []
            
            for prod in prods:
                if len(prod) == 1 and CNFConverter.is_terminal(prod[0]):
                    new_grammar[nt].append(prod)
                
                elif len(prod) == 2:
                    new_prod = []
                    
                    for symbol in prod:
                        if CNFConverter.is_terminal(symbol):
                            if symbol not in terminal_vars:
                                terminal_vars[symbol] = f'T{counter}'
                                counter += 1
                                new_grammar[terminal_vars[symbol]] = [[symbol]]
                            
                            new_prod.append(terminal_vars[symbol])
                        else:
                            new_prod.append(symbol)
                    
                    new_grammar[nt].append(new_prod)
                
                else:
                    new_grammar[nt].append(prod)
        
        return new_grammar
    
    @staticmethod
    def break_long_productions(grammar: Dict[str, List[List[str]]]) -> Dict[str, List[List[str]]]:
        """
        Descompone producciones de más de 2 símbolos en producciones binarias.
        
        Args:
            grammar: Gramática con producciones largas
            
        Returns:
            Nueva gramática con producciones máximo binarias
        """
        new_grammar = {}
        counter = 0
        
        for nt, prods in grammar.items():
            new_grammar[nt] = []
            
            for prod in prods:
                if len(prod) <= 2:
                    new_grammar[nt].append(prod)
                
                else:
                    current = nt
                    for i in range(len(prod) - 2):
                        new_var = f'X{counter}'
                        counter += 1
                        
                        new_grammar[current].append([prod[i], new_var])
                        current = new_var
                        new_grammar[current] = []
                    
                    new_grammar[current].append([prod[-2], prod[-1]])
        
        return new_grammar
    
    @staticmethod
    def convert_to_cnf(grammar: Dict[str, List[List[str]]]) -> Dict[str, List[List[str]]]:
        """
        Convierte una gramática CFG completa a Forma Normal de Chomsky.
        
        Args:
            grammar: Gramática CFG original
            
        Returns:
            Gramática equivalente en CNF
        """
        print("🔄 Convirtiendo gramática a CNF...")
        print("   Paso 1: Eliminando producciones ε")
        g = CNFConverter.eliminate_epsilon(grammar)
        
        print("   Paso 2: Eliminando producciones unitarias")
        g = CNFConverter.eliminate_unit_productions(g)
        
        print("   Paso 3: Normalizando terminales")
        g = CNFConverter.normalize_terminals(g)
        
        print("   Paso 4: Descomponiendo producciones largas")
        g = CNFConverter.break_long_productions(g)
        
        print("   ✓ Conversión completada")
        
        return g
    
    @staticmethod
    def print_grammar(grammar: Dict[str, List[List[str]]], title: str = "Gramática"):
        """
        Imprime una gramática de forma legible.
        
        Args:
            grammar: Gramática a imprimir
            title: Título para mostrar
        """
        print(f"\n{title}")
        print("=" * 60)
        
        for nt, prods in sorted(grammar.items()):
            prod_strs = [' '.join(p) for p in prods]
            print(f"{nt} → {' | '.join(prod_strs)}")
        
        print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("📋 MÓDULO CNF_CONVERTER")
    print("=" * 60)
    
    grammar = {
        'S': [['NP', 'VP']],
        'VP': [['V', 'NP']],
        'NP': [['Det', 'N'], ['he']],
        'V': [['eats']],
        'Det': [['a']],
        'N': [['cake']]
    }
    
    CNFConverter.print_grammar(grammar, "Gramática de Ejemplo")
    
    is_cnf = CNFConverter.is_in_cnf(grammar)
    print(f"\n¿Está en CNF? {'✓ Sí' if is_cnf else '✗ No'}")