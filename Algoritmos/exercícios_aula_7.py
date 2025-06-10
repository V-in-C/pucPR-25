'''Exercício 1
Crie uma matriz 3x3 preenchida com zeros.
Peça ao usuário para digitar 9 números e preencha a matriz com eles.
Exiba a matriz formatada.
Some todos os elementos da matriz.
Conte quantos elementos são maiores que 10.
'''

def exercicio_1():
    matriz = [[0,0,0], [0,0,0], [0,0,0]]
    soma = 0
    contador_maiores_que_10 = 0
    print("Digite 9 números para preencher a matriz 3x3:")
    for i in range(3):
        for j in range(3):
            matriz[i][j] = int(input(f"Digite o número para a posição [{i}][{j}]: "))
            soma += matriz[i][j]
            if matriz[i][j] > 10:
                contador_maiores_que_10 += 1
    print("Matriz preenchida:")
    for linha in matriz:
        print(linha)
    print(f"Soma dos elementos: {soma}")
    print(f"Elementos maiores que 10: {contador_maiores_que_10}")

# Chamada da função
# exercicio_1()

'''
Exercício 2
Faça um programa que gere uma matriz 10x10 com números aleatorios, o programa deve retornar o maior número presente na matriz.
'''
import random
maior = float('-inf')  # Inicializa o maior número com o menor valor possível
def exercicio_2():
    matriz = [[random.randint(1, 100) for _ in range(10)] for _ in range(10)]
    for linha in matriz:
        for numero in linha:
            if numero > maior:      
                maior = numero
    print(f"Maior número na matriz: {maior}")
# Chamada da função
# exercicio_2()

'''
Exercício 3
Faça um programa que gere uma matriz 10 x 10 com números aleatórios e imprima todos os elementos em ordem crescente (não use sort)
'''
def exercicio_3():
    matriz = [[random.randint(-1000, 1000) for _ in range(10)] for _ in range(10)]
    elementos = [numero for linha in matriz for numero in linha]
    for i in range(len(elementos)):
        for j in range(i + 1, len(elementos)):
            if elementos[i] < elementos[j]:
                elementos[i], elementos[j] = elementos[j], elementos[i]
    print("Elementos em ordem crescente:")
    for numero in elementos:
        print(numero)
# Chamada da função
# exercicio_3()

'''Exercício 4
**Criar um tabuleiro de Jogo da Velha**

- Use uma matriz 3x3 com espaços vazios " "
- Peça para dois jogadores alternarem jogadas (X e O)
- Atualize o tabuleiro a cada jogada
- Impeça que uma posição ocupada seja sobrescrita
- [Avançado] Verifique vitória ou empate
'''
def exibir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" | ".join(linha))
        print("-" * 9)
def verificar_vitoria(tabuleiro):
    # Verifica linhas
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] and linha[0] != " ":
            return True
    # Verifica colunas
    for j in range(3):
        if tabuleiro[0][j] == tabuleiro[1][j] == tabuleiro[2][j] and tabuleiro[0][j] != " ":
            return True
    # Verifica diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] != " ":
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] != " ":
        return True
    return False
def verificar_empate(tabuleiro):
    for linha in tabuleiro:
        if " " in linha:
            return False
    return True
def jogo_da_velha():
    tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
    jogador_atual = "X"
    while True:
        exibir_tabuleiro(tabuleiro)
        print(f"Vez do jogador {jogador_atual}")
        linha = int(input("Digite a linha (1-3): ")) - 1
        coluna = int(input("Digite a coluna (1-3): ")) - 1
        if tabuleiro[linha][coluna] != " ":
            print("Posição já ocupada! Tente novamente.")
            continue
        tabuleiro[linha][coluna] = jogador_atual
        if verificar_vitoria(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print(f"Jogador {jogador_atual} venceu!")
            break
        if verificar_empate(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("Empate!")
            break
        jogador_atual = "O" if jogador_atual == "X" else "X"
# Chamada da função
jogo_da_velha()