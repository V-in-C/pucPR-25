import pathlib

'''
Criar uma função recursiva chamada ler_arquivos_recursivamente que:​

Recebe um caminho inicial (string).​
Acessa todos os arquivos .txt dentro dessa estrutura.​
Imprime na tela o caminho do arquivo e seu conteúdo.​​
A função deve ser recursiva — ou seja, você não pode usar laços como while ou for para explorar diretórios.
'''

def ler_arquivos_recursivamente(caminho):
    p = pathlib.Path(caminho)
    if p.is_dir():
        # Chama recursivamente para cada item no diretório
        for item in p.iterdir():
            ler_arquivos_recursivamente(str(item))
    elif p.suffix == '.txt':
        with p.open('r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            print(f'Arquivo: {p}\nConteúdo:\n{conteudo}\n')

# Chamada da função
# ler_arquivos_recursivamente('caminho/do/diretorio')  # Substitua pelo caminho desejado

'''
1. Crie uma função recursiva que receba um número inteiro n e
retorne o valor de n! (fatorial de n).
'''
def fatorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fatorial(n - 1)
# Chamada da função
# print(fatorial(5))  # Exemplo: fatorial de 5 é 120

'''
2. Implemente uma função recursiva que calcule o n-ésimo termo da
sequência de Fibonacci.
'''
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
# Chamada da função
print(fibonacci(7))  # Exemplo: o 7º termo da sequência de Fibonacci é 13

''' 
3. Crie uma função recursiva que verifique se uma palavra é um
palíndromo (lê-se igual de trás pra frente).
'''
def eh_palindromo(palavra):
    palavra = palavra.lower().replace(" ", "")  # Normaliza a palavra
    if len(palavra) <= 1:
        return True
    if palavra[0] != palavra[-1]:
        return False
    return eh_palindromo(palavra[1:-1])
# Chamada da função
# print(eh_palindromo("A man a plan a canal Panama"))
'''
4. Implemente uma função recursiva que calcule a soma dos dígitos
de um número inteiro positivo.
'''
def soma_digitos(n):
    if n == 0:
        return 0
    else:
        return n % 10 + soma_digitos(n // 10)
# Chamada da função
# print(soma_digitos(12345))  # Exemplo: a soma dos dígitos de 12345 é 15

