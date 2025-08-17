"""
regex_parser.py - Parser para convertir expresiones regulares a AST
"""

from ast_node import ASTNode

class RegexParser:
    """Parser para expresiones regulares usando Shunting Yard"""
    
    def __init__(self):
        self.precedence = {
            '*': 4, '+': 4, '?': 4,  # Operadores unarios (mayor precedencia)
            '.': 3,                   # Concatenación
            '|': 2,                   # Unión
            '(': 1                    # Paréntesis (menor precedencia)
        }
        self.node_counter = 0
    
    def expand_extensions(self, regex):
        """Expande operadores + y ? a formas básicas"""
        print(f"\n🔄 EXPANDIENDO EXTENSIONES")
        print(f"Original: {regex}")
        
        expanded = regex
        changes = []
        
        # Expandir a? → (a|ε)
        i = 0
        while i < len(expanded):
            if i > 0 and expanded[i] == '?':
                if expanded[i-1] == ')':
                    # Encontrar paréntesis correspondiente
                    paren_count = 1
                    j = i - 2
                    while j >= 0 and paren_count > 0:
                        if expanded[j] == ')':
                            paren_count += 1
                        elif expanded[j] == '(':
                            paren_count -= 1
                        j -= 1
                    j += 1
                    operand = expanded[j:i]
                    new_expanded = expanded[:j] + f"({operand}|ε)" + expanded[i+1:]
                    changes.append(f"  {operand}? → ({operand}|ε)")
                    expanded = new_expanded
                    i = j + len(f"({operand}|ε)") - 1
                else:
                    operand = expanded[i-1]
                    new_expanded = expanded[:i-1] + f"({operand}|ε)" + expanded[i+1:]
                    changes.append(f"  {operand}? → ({operand}|ε)")
                    expanded = new_expanded
                    i = i - 1 + len(f"({operand}|ε)") - 1
            i += 1
        
        # Expandir a+ → aa*
        i = 0
        while i < len(expanded):
            if i > 0 and expanded[i] == '+':
                if expanded[i-1] == ')':
                    # Encontrar paréntesis correspondiente
                    paren_count = 1
                    j = i - 2
                    while j >= 0 and paren_count > 0:
                        if expanded[j] == ')':
                            paren_count += 1
                        elif expanded[j] == '(':
                            paren_count -= 1
                        j -= 1
                    j += 1
                    operand = expanded[j:i]
                    new_expanded = expanded[:j] + f"{operand}{operand}*" + expanded[i+1:]
                    changes.append(f"  {operand}+ → {operand}{operand}*")
                    expanded = new_expanded
                    i = j + len(f"{operand}{operand}*") - 1
                else:
                    operand = expanded[i-1]
                    new_expanded = expanded[:i-1] + f"{operand}{operand}*" + expanded[i+1:]
                    changes.append(f"  {operand}+ → {operand}{operand}*")
                    expanded = new_expanded
                    i = i - 1 + len(f"{operand}{operand}*") - 1
            i += 1
        
        if changes:
            print("Cambios realizados:")
            for change in changes:
                print(change)
        else:
            print("No hay extensiones que expandir")
        
        print(f"Expandida: {expanded}")
        return expanded
    
    def tokenize(self, regex):
        """Tokeniza la expresión regular"""
        tokens = []
        i = 0
        
        while i < len(regex):
            char = regex[i]
            
            # Manejar caracteres escapados
            if char == '\\' and i + 1 < len(regex):
                tokens.append(regex[i:i+2])
                i += 2
            # Manejar clases de caracteres [...]
            elif char == '[':
                j = i + 1
                while j < len(regex) and regex[j] != ']':
                    j += 1
                if j < len(regex):
                    tokens.append(regex[i:j+1])
                    i = j + 1
                else:
                    # Paréntesis sin cerrar, tratar como carácter literal
                    tokens.append(char)
                    i += 1
            # Caracteres normales
            else:
                tokens.append(char)
                i += 1
        
        return tokens
    
    def insert_concatenation(self, tokens):
        """Inserta operadores de concatenación explícitos"""
        if not tokens:
            return tokens
        
        new_tokens = []
        
        for i in range(len(tokens)):
            if i > 0:
                prev_token = tokens[i-1]
                curr_token = tokens[i]
                
                # Insertar concatenación entre:
                # - operando y operando
                # - operando y paréntesis de apertura
                # - paréntesis de cierre y operando
                # - paréntesis de cierre y paréntesis de apertura
                # - operadores unarios y operandos/paréntesis de apertura
                
                need_concat = False
                
                # Casos donde el token anterior NO es un operador binario o paréntesis de apertura
                if prev_token not in ['|', '(']:
                    # Casos donde el token actual NO es un operador o paréntesis de cierre
                    if curr_token not in ['|', '*', '+', '?', ')']:
                        need_concat = True
                
                # Casos especiales para operadores unarios
                if prev_token in [')', '*', '+', '?']:
                    if curr_token not in ['|', ')', '*', '+', '?']:
                        need_concat = True
                
                if need_concat:
                    new_tokens.append('.')
            
            new_tokens.append(tokens[i])
        
        return new_tokens
    
    def to_postfix(self, regex):
        """Convierte expresión regular a notación postfix usando Shunting Yard"""
        # 1. Expandir extensiones
        expanded = self.expand_extensions(regex)
        
        # 2. Tokenizar
        tokens = self.tokenize(expanded)
        print(f"\nTokens: {tokens}")
        
        # 3. Insertar concatenación
        tokens = self.insert_concatenation(tokens)
        print(f"Con concatenación: {tokens}")
        
        # 4. Algoritmo Shunting Yard
        output = []
        operator_stack = []
        
        print(f"\n🔄 APLICANDO SHUNTING YARD")
        
        for token in tokens:
            print(f"Procesando token: '{token}'")
            
            # Operandos van directamente a la salida
            if token not in self.precedence and token != ')':
                output.append(token)
                print(f"  Operando → salida: {output}")
            
            # Paréntesis de apertura va al stack
            elif token == '(':
                operator_stack.append(token)
                print(f"  '(' → stack: {operator_stack}")
            
            # Paréntesis de cierre: vaciar hasta encontrar '('
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    op = operator_stack.pop()
                    output.append(op)
                    print(f"  ')' → sacar '{op}' del stack: {output}")
                
                # Remover el '(' del stack
                if operator_stack:
                    operator_stack.pop()
                    print(f"  ')' → remover '(' del stack: {operator_stack}")
            
            # Operadores
            else:
                # Sacar operadores con mayor o igual precedencia
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       self.precedence.get(operator_stack[-1], 0) >= 
                       self.precedence.get(token, 0)):
                    op = operator_stack.pop()
                    output.append(op)
                    print(f"  Sacar '{op}' por precedencia: {output}")
                
                operator_stack.append(token)
                print(f"  '{token}' → stack: {operator_stack}")
        
        # Vaciar stack restante
        while operator_stack:
            op = operator_stack.pop()
            output.append(op)
            print(f"Vaciar stack: '{op}' → {output}")
        
        postfix = ' '.join(output)
        print(f"\n✅ Expresión postfix: {postfix}")
        return output
    
    def postfix_to_ast(self, postfix_tokens):
        """Construye AST desde expresión en postfix"""
        print(f"\n🌳 CONSTRUYENDO AST DESDE POSTFIX")
        print(f"Tokens postfix: {postfix_tokens}")
        
        stack = []
        self.node_counter = 0
        
        for token in postfix_tokens:
            self.node_counter += 1
            print(f"\nProcesando token '{token}' (nodo #{self.node_counter})")
            
            # Operadores unarios
            if token in ['*', '+', '?']:
                if not stack:
                    raise ValueError(f"Operador unario '{token}' sin operando")
                
                child = stack.pop()
                node = ASTNode(token, left=child, node_type="unary_op")
                node.id = self.node_counter
                stack.append(node)
                print(f"  Operador unario: {token}({child.value}) → nodo {node.id}")
            
            # Operadores binarios
            elif token in ['|', '.']:
                if len(stack) < 2:
                    raise ValueError(f"Operador binario '{token}' necesita 2 operandos")
                
                right = stack.pop()
                left = stack.pop()
                node = ASTNode(token, left=left, right=right, node_type="binary_op")
                node.id = self.node_counter
                stack.append(node)
                print(f"  Operador binario: {left.value} {token} {right.value} → nodo {node.id}")
            
            # Operandos
            else:
                node = ASTNode(token, node_type="operand")
                node.id = self.node_counter
                stack.append(node)
                print(f"  Operando: '{token}' → nodo {node.id}")
            
            print(f"  Stack actual: {[n.value for n in stack]}")
        
        if len(stack) != 1:
            raise ValueError(f"Error en construcción del AST: stack final tiene {len(stack)} elementos")
        
        root = stack[0]
        print(f"\n✅ AST construido exitosamente con raíz: {root.value} (nodo {root.id})")
        return root
    
    def parse(self, regex):
        """Método principal para parsear una expresión regular"""
        print(f"\n{'='*60}")
        print(f"🔤 PARSEANDO EXPRESIÓN REGULAR: {regex}")
        print(f"{'='*60}")
        
        try:
            # Convertir a postfix
            postfix_tokens = self.to_postfix(regex)
            
            # Construir AST
            ast_root = self.postfix_to_ast(postfix_tokens)
            
            return ast_root
            
        except Exception as e:
            print(f"❌ Error parseando expresión '{regex}': {e}")
            raise