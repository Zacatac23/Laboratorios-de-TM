"""
regex_parser_fixed.py - Versión corregida de tu parser para manejar escape y clases
"""

from ast_node import ASTNode

class FixedRegexParser:
    """Parser corregido que maneja escape y clases de caracteres correctamente"""
    
    def __init__(self):
        self.precedence = {
            '*': 4, '+': 4, '?': 4,
            '.': 3,
            '|': 2,
            '(': 1
        }
        self.node_counter = 0
    
    def expand_extensions(self, regex):
        """Expande TODAS las extensiones incluyendo escape y clases"""
        print(f"\n📄 EXPANDIENDO EXTENSIONES")
        print(f"Original: {regex}")
        
        expanded = regex
        changes = []
        
        # 1. Primero expandir escape de caracteres
        expanded, escape_changes = self._expand_escape_sequences(expanded)
        changes.extend(escape_changes)
        
        # 2. Expandir clases de caracteres [abc]
        expanded, class_changes = self._expand_character_classes(expanded)
        changes.extend(class_changes)
        
        # 3. Expandir a? → (a|ε)
        i = 0
        while i < len(expanded):
            if i > 0 and expanded[i] == '?':
                if expanded[i-1] == ')':
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
        
        # 4. Expandir a+ → aa*
        i = 0
        while i < len(expanded):
            if i > 0 and expanded[i] == '+':
                if expanded[i-1] == ')':
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
    
    def _expand_escape_sequences(self, regex):
        """Expande secuencias de escape correctamente"""
        changes = []
        expanded = ""
        i = 0
        
        while i < len(regex):
            if i < len(regex) - 1 and regex[i] == '\\':
                next_char = regex[i+1]
                
                # Mapeo de escapes a caracteres literales
                if next_char == '(':
                    expanded += '('  # Paréntesis literal
                    changes.append(f"\\( → ( (paréntesis literal)")
                elif next_char == ')':
                    expanded += ')'  # Paréntesis literal
                    changes.append(f"\\) → ) (paréntesis literal)")
                elif next_char == '{':
                    expanded += '{'  # Llave literal
                    changes.append(f"\\{{ → {{ (llave literal)")
                elif next_char == '}':
                    expanded += '}'  # Llave literal
                    changes.append(f"\\}} → }} (llave literal)")
                elif next_char == '[':
                    expanded += '['  # Corchete literal
                    changes.append(f"\\[ → [ (corchete literal)")
                elif next_char == ']':
                    expanded += ']'  # Corchete literal
                    changes.append(f"\\] → ] (corchete literal)")
                elif next_char == '*':
                    expanded += 'STAR_LITERAL'  # Asterisco literal (símbolo especial)
                    changes.append(f"\\* → STAR_LITERAL (asterisco literal)")
                elif next_char == '+':
                    expanded += 'PLUS_LITERAL'  # Plus literal (símbolo especial)
                    changes.append(f"\\+ → PLUS_LITERAL (plus literal)")
                elif next_char == '?':
                    expanded += 'QUEST_LITERAL'  # Question literal (símbolo especial)
                    changes.append(f"\\? → QUEST_LITERAL (interrogación literal)")
                elif next_char == '|':
                    expanded += 'PIPE_LITERAL'  # Pipe literal (símbolo especial)
                    changes.append(f"\\| → PIPE_LITERAL (pipe literal)")
                else:
                    # Otros escapes: simplemente quitar el backslash
                    expanded += next_char
                    changes.append(f"\\{next_char} → {next_char}")
                
                i += 2
            else:
                expanded += regex[i]
                i += 1
        
        return expanded, changes
    
    def _expand_character_classes(self, regex):
        """Expande clases de caracteres [abc] → (a|b|c)"""
        changes = []
        expanded = ""
        i = 0
        
        while i < len(regex):
            if regex[i] == '[':
                # Encontrar el cierre de la clase
                j = i + 1
                class_content = ""
                
                # Recolectar contenido de la clase
                while j < len(regex) and regex[j] != ']':
                    class_content += regex[j]
                    j += 1
                
                if j < len(regex) and regex[j] == ']':
                    # Clase válida encontrada
                    original_class = regex[i:j+1]
                    
                    # Parsear contenido de la clase
                    chars = self._parse_character_class_content(class_content)
                    
                    if len(chars) == 1:
                        expanded_class = chars[0]
                    else:
                        expanded_class = "(" + "|".join(chars) + ")"
                    
                    changes.append(f"{original_class} → {expanded_class}")
                    expanded += expanded_class
                    i = j + 1
                else:
                    # Corchete sin cerrar, tratar como literal
                    expanded += regex[i]
                    i += 1
            else:
                expanded += regex[i]
                i += 1
        
        return expanded, changes
    
    def _parse_character_class_content(self, content):
        """Parsea el contenido de una clase de caracteres"""
        chars = []
        i = 0
        
        while i < len(content):
            if i < len(content) - 2 and content[i+1] == '-':
                # Rango de caracteres: a-z
                start_char = content[i]
                end_char = content[i+2]
                
                # Generar rango
                if start_char.isalpha() and end_char.isalpha():
                    for char_code in range(ord(start_char), ord(end_char) + 1):
                        chars.append(chr(char_code))
                elif start_char.isdigit() and end_char.isdigit():
                    for char_code in range(ord(start_char), ord(end_char) + 1):
                        chars.append(chr(char_code))
                else:
                    # Rango inválido, tratar como caracteres literales
                    chars.extend([start_char, '-', end_char])
                
                i += 3
            else:
                # Caracter individual
                chars.append(content[i])
                i += 1
        
        return chars
    
    def tokenize(self, regex):
        """Tokeniza la expresión regular"""
        tokens = []
        i = 0
        
        while i < len(regex):
            char = regex[i]
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
                
                need_concat = False
                
                if prev_token not in ['|', '(']:
                    if curr_token not in ['|', '*', '+', '?', ')']:
                        need_concat = True
                
                if prev_token in [')', '*', '+', '?']:
                    if curr_token not in ['|', ')', '*', '+', '?']:
                        need_concat = True
                
                if need_concat:
                    new_tokens.append('.')
            
            new_tokens.append(tokens[i])
        
        return new_tokens
    
    def to_postfix(self, regex):
        """Convierte expresión regular a notación postfix"""
        expanded = self.expand_extensions(regex)
        tokens = self.tokenize(expanded)
        print(f"\nTokens: {tokens}")
        
        tokens = self.insert_concatenation(tokens)
        print(f"Con concatenación: {tokens}")
        
        output = []
        operator_stack = []
        
        print(f"\n🔄 APLICANDO SHUNTING YARD")
        
        for token in tokens:
            print(f"Procesando token: '{token}'")
            
            if token not in self.precedence and token != ')':
                output.append(token)
                print(f"  Operando → salida: {output}")
            
            elif token == '(':
                operator_stack.append(token)
                print(f"  '(' → stack: {operator_stack}")
            
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    op = operator_stack.pop()
                    output.append(op)
                    print(f"  ')' → sacar '{op}' del stack: {output}")
                
                if operator_stack:
                    operator_stack.pop()
                    print(f"  ')' → remover '(' del stack: {operator_stack}")
            
            else:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       self.precedence.get(operator_stack[-1], 0) >= 
                       self.precedence.get(token, 0)):
                    op = operator_stack.pop()
                    output.append(op)
                    print(f"  Sacar '{op}' por precedencia: {output}")
                
                operator_stack.append(token)
                print(f"  '{token}' → stack: {operator_stack}")
        
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
            
            if token in ['*', '+', '?']:
                if not stack:
                    raise ValueError(f"Operador unario '{token}' sin operando")
                
                child = stack.pop()
                node = ASTNode(token, left=child, node_type="unary_op")
                node.id = self.node_counter
                stack.append(node)
                print(f"  Operador unario: {token}({child.value}) → nodo {node.id}")
            
            elif token in ['|', '.']:
                if len(stack) < 2:
                    raise ValueError(f"Operador binario '{token}' necesita 2 operandos")
                
                right = stack.pop()
                left = stack.pop()
                node = ASTNode(token, left=left, right=right, node_type="binary_op")
                node.id = self.node_counter
                stack.append(node)
                print(f"  Operador binario: {left.value} {token} {right.value} → nodo {node.id}")
            
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
        print(f"📤 PARSEANDO EXPRESIÓN REGULAR: {regex}")
        print(f"{'='*60}")
        
        try:
            postfix_tokens = self.to_postfix(regex)
            ast_root = self.postfix_to_ast(postfix_tokens)
            return ast_root
            
        except Exception as e:
            print(f"❌ Error parseando expresión '{regex}': {e}")
            raise


# Test específico para tu caso
def test_if_expression():
    """Prueba específica para la expresión if"""
    parser = FixedRegexParser()
    
    expr = "if\\([abc]+\\)\\{[xyz]*\\}(else\\{[01]+\\})?"
    test_string = "if(abc){x}else{01}"
    
    print(f"🧪 PRUEBA ESPECÍFICA")
    print(f"Expresión: {expr}")
    print(f"Cadena: {test_string}")
    print("=" * 50)
    
    try:
        ast = parser.parse(expr)
        print(f"✅ AST construido correctamente")
        
        # Aquí podrías construir el NFA y probarlo
        # nfa = thompson_builder.build_nfa_from_ast(ast)
        # result = nfa.simulate(test_string)
        # print(f"Resultado: {'ACEPTADA' if result else 'RECHAZADA'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_if_expression()