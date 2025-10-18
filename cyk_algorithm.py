"""
Módulo del Algoritmo CYK (Cocke-Younger-Kasami)
Persona 2: Algoritmo CYK y Parse Tree

Autores: [Persona 2]
Fecha: Octubre 2024
"""

import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ParseNode:
    """
    Nodo del árbol de parseo.
    
    Attributes:
        symbol: Símbolo no-terminal o terminal
        value: Valor si es terminal
        children: Lista de nodos hijos
    """
    symbol: str
    value: Optional[str] = None
    children: List['ParseNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def is_terminal(self) -> bool:
        """Retorna True si es nodo terminal"""
        return self.value is not None


class CYKParser:
    """
    Implementación del algoritmo CYK.
    
    Complejidad: O(n³ * |G|)
    """
    
    def __init__(self, grammar: Dict[str, List[List[str]]]):
        """
        Inicializa el parser con una gramática en CNF.
        
        Args:
            grammar: Diccionario con la gramática en CNF
        """
        self.grammar = grammar
        self.table = None
        self.backpointers = None
        self.start_symbol = 'S'
    
    def parse(self, sentence: str) -> Tuple[bool, float, List[List[List[str]]]]:
        """
        Analiza una frase usando el algoritmo CYK.
        
        Args:
            sentence: Frase a analizar
            
        Returns:
            Tupla con (aceptada, tiempo_ms, tabla)
        """
        if not sentence or not sentence.strip():
            return False, 0.0, []
        
        words = sentence.strip().split()
        return self._cyk_algorithm(words)
    
    def _cyk_algorithm(self, words: List[str]) -> Tuple[bool, float, List[List[List[str]]]]:
        """
        Implementación del algoritmo CYK con programación dinámica.
        
        Args:
            words: Lista de palabras
            
        Returns:
            Tupla con (aceptada, tiempo_ms, tabla)
        """
        start_time = time.time()
        n = len(words)
        
        # Inicializar tabla triangular
        self.table = [[[] for _ in range(n)] for _ in range(n)]
        self.backpointers = [[{} for _ in range(n)] for _ in range(n)]
        
        # PASO 1: Llenar diagonal
        for i in range(n):
            word = words[i].lower()
            
            for non_terminal, productions in self.grammar.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0].lower() == word:
                        if non_terminal not in self.table[i][i]:
                            self.table[i][i].append(non_terminal)
                            self.backpointers[i][i][non_terminal] = {
                                'type': 'terminal',
                                'value': word
                            }
        
        # PASO 2: Programación dinámica
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                for k in range(i, j):
                    left_cell = self.table[i][k]
                    right_cell = self.table[k + 1][j]
                    
                    for non_terminal, productions in self.grammar.items():
                        for prod in productions:
                            if len(prod) == 2:
                                B, C = prod
                                
                                if B in left_cell and C in right_cell:
                                    if non_terminal not in self.table[i][j]:
                                        self.table[i][j].append(non_terminal)
                                        self.backpointers[i][j][non_terminal] = {
                                            'type': 'binary',
                                            'left': B,
                                            'right': C,
                                            'split': k,
                                            'left_span': (i, k),
                                            'right_span': (k + 1, j)
                                        }
        
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        
        accepted = self.start_symbol in self.table[0][n - 1]
        
        return accepted, elapsed_ms, self.table
    
    def build_parse_tree(self, words: List[str]) -> Optional[ParseNode]:
        """
        Construye el árbol de parseo.
        
        Args:
            words: Lista de palabras
            
        Returns:
            Raíz del árbol o None
        """
        if self.table is None:
            return None
        
        n = len(words)
        if not words or self.start_symbol not in self.table[0][n - 1]:
            return None
        
        return self._build_tree_recursive(self.start_symbol, 0, n - 1, words)
    
    def _build_tree_recursive(self, symbol: str, i: int, j: int, 
                             words: List[str]) -> Optional[ParseNode]:
        """
        Construye el árbol recursivamente.
        
        Args:
            symbol: Símbolo actual
            i: Índice inicial
            j: Índice final
            words: Lista de palabras
            
        Returns:
            Nodo del árbol
        """
        if symbol not in self.backpointers[i][j]:
            return None
        
        bp = self.backpointers[i][j][symbol]
        
        if bp['type'] == 'terminal':
            return ParseNode(symbol=symbol, value=bp['value'])
        
        if bp['type'] == 'binary':
            left_child = self._build_tree_recursive(
                bp['left'],
                bp['left_span'][0],
                bp['left_span'][1],
                words
            )
            
            right_child = self._build_tree_recursive(
                bp['right'],
                bp['right_span'][0],
                bp['right_span'][1],
                words
            )
            
            return ParseNode(
                symbol=symbol,
                children=[left_child, right_child]
            )
        
        return None
    
    def print_table(self, words: List[str]):
        """
        Imprime la tabla CYK.
        
        Args:
            words: Lista de palabras
        """
        if self.table is None:
            print("❌ No hay tabla para mostrar")
            return
        
        n = len(words)
        
        print("\n" + "=" * 80)
        print("📊 TABLA CYK (Programación Dinámica)")
        print("=" * 80)
        print()
        
        for i in range(n):
            line = ""
            
            for j in range(n):
                if j < i:
                    line += "          "
                else:
                    content = ', '.join(self.table[i][j]) if self.table[i][j] else '∅'
                    line += f"[{i},{j}]:{content:8} "
            
            print(line)
            
            if i < n:
                padding = "          " * i
                print(f"{padding}\"{words[i]}\"")
        
        print("=" * 80)
        
        print("\n💡 Interpretación:")
        if self.start_symbol in self.table[0][n-1]:
            print(f"   ✓ '{self.start_symbol}' está en [0,{n-1}] → Frase ACEPTADA")
        else:
            print(f"   ✗ '{self.start_symbol}' NO está en [0,{n-1}] → Frase RECHAZADA")


def print_parse_tree(node: ParseNode, depth: int = 0, prefix: str = "", 
                     is_last: bool = True):
    """
    Imprime el árbol de parseo.
    
    Args:
        node: Nodo actual
        depth: Profundidad
        prefix: Prefijo para líneas
        is_last: Si es el último hijo
    """
    if node is None:
        return
    
    connector = "└─ " if is_last else "├─ "
    
    if depth == 0:
        print(f"{node.symbol}")
    else:
        if node.is_terminal():
            print(f"{prefix}{connector}{node.symbol} → \"{node.value}\"")
        else:
            print(f"{prefix}{connector}{node.symbol}")
    
    if depth > 0:
        extension = "   " if is_last else "│  "
        new_prefix = prefix + extension
    else:
        new_prefix = ""
    
    for i, child in enumerate(node.children):
        is_last_child = i == len(node.children) - 1
        print_parse_tree(child, depth + 1, new_prefix, is_last_child)


if __name__ == "__main__":
    print("=" * 60)
    print("📋 MÓDULO CYK_ALGORITHM")
    print("=" * 60)
    
    grammar = {
        'S': [['NP', 'VP']],
        'VP': [['V', 'NP']],
        'NP': [['Det', 'N'], ['she']],
        'V': [['eats']],
        'Det': [['a']],
        'N': [['cake']]
    }
    
    parser = CYKParser(grammar)
    
    phrase = "she eats a cake"
    print(f"\nAnalizando: \"{phrase}\"")
    
    accepted, time_ms, _ = parser.parse(phrase)
    
    print(f"Resultado: {'✓ ACEPTADA' if accepted else '✗ RECHAZADA'}")
    print(f"Tiempo: {time_ms:.4f} ms")
    
    if accepted:
        tree = parser.build_parse_tree(phrase.split())
        print("\n🌳 Árbol de Parseo:")
        print_parse_tree(tree)