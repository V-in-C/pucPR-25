import re
from graphviz import Digraph

# Função para analisar a expressão lógica em uma árvore
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def parse_expr(expr):
    expr = expr.replace(' ', '')
    def parse(tokens):
        stack = []
        ops = []
        precedence = {'NOT': 3, '&': 2, 'AND': 2, '|': 1, 'OR': 1}
        def apply():
            op = ops.pop()
            if op == 'NOT':
                node = Node('NOT', left=stack.pop())
            else:
                right = stack.pop()
                left = stack.pop()
                node = Node(op, left, right)
            stack.append(node)
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t == '(':
                ops.append(t)
            elif t == ')':
                while ops and ops[-1] != '(':
                    apply()
                ops.pop()
            elif t in precedence:
                while (ops and ops[-1] in precedence and
                       precedence[ops[-1]] >= precedence[t]):
                    apply()
                ops.append(t)
            else:
                stack.append(Node(t))
            i += 1
        while ops:
            apply()
        return stack[0]
    # Tokenização
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i] in '()&|':
            tokens.append(expr[i])
            i += 1
        elif expr[i:i+3] == 'NOT':
            tokens.append('NOT')
            i += 3
        elif expr[i:i+2] == 'OR':
            tokens.append('OR')
            i += 2
        elif expr[i:i+3] == 'AND':
            tokens.append('AND')
            i += 3
        elif expr[i].isalpha():
            tokens.append(expr[i])
            i += 1
        else:
            i += 1
    return parse(tokens)

# Função para desenhar o circuito lógico
def draw_circuit(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph()
    nid = str(id(node))
    label = node.value
    if label == '&':
        label = 'AND'
    elif label == '|':
        label = 'OR'
    graph.node(nid, label)
    if parent:
        graph.edge(parent, nid)
    if node.left:
        draw_circuit(node.left, graph, nid)
    if node.right:
        draw_circuit(node.right, graph, nid)
    return graph

# Simplificação básica usando regras booleanas
def simplify(node, steps):
    # Simplificação recursiva
    if node is None:
        return None
    if node.value == 'NOT':
        child = simplify(node.left, steps)
        # Dupla negação
        if child.value == 'NOT':
            steps.append('Dupla negação: NOT NOT X = X')
            return simplify(child.left, steps)
        return Node('NOT', left=child)
    if node.value in ('&', 'AND', '|', 'OR'):
        left = simplify(node.left, steps)
        right = simplify(node.right, steps)
        # Idempotência: X & X = X, X | X = X
        if left.value == right.value and left.value.isalpha():
            steps.append(f'Idempotência: {left.value} {node.value} {right.value} = {left.value}')
            return left
        # Dominação: X & 0 = 0, X | 1 = 1
        if node.value in ('&', 'AND'):
            if (left.value == '0' or right.value == '0'):
                steps.append('Dominação: X & 0 = 0')
                return Node('0')
            if left.value == '1':
                steps.append('Identidade: 1 & X = X')
                return right
            if right.value == '1':
                steps.append('Identidade: X & 1 = X')
                return left
        if node.value in ('|', 'OR'):
            if (left.value == '1' or right.value == '1'):
                steps.append('Dominação: X | 1 = 1')
                return Node('1')
            if left.value == '0':
                steps.append('Identidade: 0 | X = X')
                return right
            if right.value == '0':
                steps.append('Identidade: X | 0 = X')
                return left
        # Complementação: X & NOT X = 0, X | NOT X = 1
        if (left.value == 'NOT' and left.left.value == right.value) or \
           (right.value == 'NOT' and right.left.value == left.value):
            if node.value in ('&', 'AND'):
                steps.append('Complementação: X & NOT X = 0')
                return Node('0')
            if node.value in ('|', 'OR'):
                steps.append('Complementação: X | NOT X = 1')
                return Node('1')
        return Node(node.value, left, right)
    return node

# Função para imprimir a expressão a partir da árvore
def expr_from_tree(node):
    if node is None:
        return ''
    if node.value == 'NOT':
        return f'NOT({expr_from_tree(node.left)})'
    if node.left and node.right:
        return f'({expr_from_tree(node.left)} {node.value} {expr_from_tree(node.right)})'
    return node.value

# Exemplo de uso
entrada = '((A & B) OR ((C OR A) & NOT (B)))'
print('Entrada:', entrada)

# 1. Monta a árvore e desenha o circuito
arvore = parse_expr(entrada)
g = draw_circuit(arvore)
g.render('circuito_original', format='png', cleanup=True)
print('Saída 1: Circuito original salvo como circuito_original.png')

# 2. Simplifica e mostra os passos
passos = []
arvore_simplificada = simplify(arvore, passos)
g2 = draw_circuit(arvore_simplificada)
g2.render('circuito_simplificado', format='png', cleanup=True)
print('Saída 2: Circuito simplificado salvo como circuito_simplificado.png')
print('Passos da simplificação:')
for p in passos:
    print('-', p)
print('Expressão simplificada:', expr_from_tree(arvore_simplificada))