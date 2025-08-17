"""
ast_node.py - Definiciones básicas para el Árbol Sintáctico Abstracto
"""

class ASTNode:
    """Representa un nodo en el Árbol Sintáctico Abstracto"""
    
    def __init__(self, value, left=None, right=None, node_type="operand"):
        self.value = value
        self.left = left
        self.right = right
        self.node_type = node_type  # "operand", "unary_op", "binary_op"
        self.id = None
    
    def __str__(self):
        return f"ASTNode({self.value}, type={self.node_type})"
    
    def __repr__(self):
        return self.__str__()
    
    def is_operand(self):
        """Verifica si el nodo es un operando"""
        return self.node_type == "operand"
    
    def is_unary_operator(self):
        """Verifica si el nodo es un operador unario"""
        return self.node_type == "unary_op"
    
    def is_binary_operator(self):
        """Verifica si el nodo es un operador binario"""
        return self.node_type == "binary_op"
    
    def get_children(self):
        """Retorna lista de hijos no nulos"""
        children = []
        if self.left:
            children.append(self.left)
        if self.right:
            children.append(self.right)
        return children
    
    def traverse_preorder(self):
        """Recorrido en preorden del árbol"""
        result = [self]
        if self.left:
            result.extend(self.left.traverse_preorder())
        if self.right:
            result.extend(self.right.traverse_preorder())
        return result
    
    def traverse_postorder(self):
        """Recorrido en postorden del árbol"""
        result = []
        if self.left:
            result.extend(self.left.traverse_postorder())
        if self.right:
            result.extend(self.right.traverse_postorder())
        result.append(self)
        return result
    
    def count_nodes(self):
        """Cuenta el total de nodos en el árbol"""
        count = 1
        if self.left:
            count += self.left.count_nodes()
        if self.right:
            count += self.right.count_nodes()
        return count