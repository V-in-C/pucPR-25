

# configurações


TamanhoBarco = 3  # tamanho do barco
TamanhoMinimo = 10 # tamanho mínimo do tabuleiro
TamanhoMaximo = 26 # tamanho máximo do tabuleiro (de preferência no MÁXIMO 26 pra não passar as letras do alfabeto)


# código


import random
import os
import platform
from colorama import init, Fore, Back, Style
init(autoreset=True)

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
clear()

def menu():
    print("batalha naval\n")
    tamanho = int(input(f"tamanho do tabuleiro ({TamanhoMinimo}-{TamanhoMaximo}): "))
    while tamanho < TamanhoMinimo or tamanho > TamanhoMaximo:
        clear()
        print("tamanho inválido\n")
        tamanho = int(input(f"tamanho do tabuleiro ({TamanhoMinimo}-{TamanhoMaximo}): "))
    clear()
    modo = input("modo de jogo (1 = jogador vs jogador | 2 = jogador vs maquina): ")
    while modo not in ['1', '2']:
        clear()
        print("modo inválido\n")
        modo = input("modo de jogo (1 = jogador vs jogador | 2 = jogador vs maquina): ")

    return tamanho, int(modo)

def CriarBoard(tamanho):
    return [[Back.BLUE + '~' for _ in range(tamanho)] for _ in range(tamanho)]

def PrintBoard(tabuleiro):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  ", end="")
    for i in range(len(tabuleiro[0])):
        print(letras[i], end=" ")
    print()
    for i in range(len(tabuleiro)):
        print(str(i+1).rjust(2), end=" ")
        for j in range(len(tabuleiro[i])):
            print(tabuleiro[i][j], end=" ")
        print()

def LetraPNumero(letra):
    return ord(letra.upper()) - ord('A')

def NumeroPLetra(numero):
    return chr(ord('A') + numero)

def vitoria(tabuleiro):
    for linha in tabuleiro:
        if 'n' in linha:
            return False
    return True

def ColocarBarco(tabuleiro):
    print(f"coloque seu navio (tamanho: {TamanhoBarco})\n")
    linha = int(input("linha inicial do navio: ")) - 1
    coluna_letra = input("coluna inicial do navio (letra): ").upper()
    coluna = LetraPNumero(coluna_letra)
    orientacao = input("horizontal (h) ou vertical (v): ").lower()
    clear()

    for i in range(TamanhoBarco):
        if orientacao == 'h':
            tabuleiro[linha][coluna + i] = 'n'
        elif orientacao == 'v':
            tabuleiro[linha + i][coluna] = 'n'

def realizar_ataque(tabuleiro_alvo, tabuleiro_tiros):
    linha = int(input("\nlinha do ataque: ")) - 1
    coluna_letra = input("coluna do ataque (letra): ").upper()
    coluna = LetraPNumero(coluna_letra)
    clear()
    if tabuleiro_alvo[linha][coluna] == 'n':
        print("acertou!\n")
        tabuleiro_alvo[linha][coluna] = Back.GREEN + 'X'
        tabuleiro_tiros[linha][coluna] = Back.GREEN + 'X'
    else:
        print("errou!\n")
        tabuleiro_tiros[linha][coluna] = Back.RED +'O'

def ataque_ia(tabuleiro_alvo, tabuleiro_tiros):
    while True:
        linha = random.randint(0, len(tabuleiro_alvo) - 1)
        coluna = random.randint(0, len(tabuleiro_alvo) - 1)
        if tabuleiro_tiros[linha][coluna] == Back.BLUE + '~':
            break
    print("maquina atacou na posição:", linha + 1, NumeroPLetra(coluna))
    if tabuleiro_alvo[linha][coluna] == 'n':
        print("maquina acertou!\n")
        tabuleiro_alvo[linha][coluna] = Back.GREEN + 'X'
        tabuleiro_tiros[linha][coluna] = Back.GREEN + 'X'
    else:
        print("maquina errou!\n")
        tabuleiro_tiros[linha][coluna] = Back.RED + 'O'

def main():
    tamanho, modo = menu()

    tabuleiro_j1 = CriarBoard(tamanho)
    tiros_j1 = CriarBoard(tamanho)

    tabuleiro_j2 = CriarBoard(tamanho)
    tiros_j2 = CriarBoard(tamanho)

    clear()
    print("navio do jogador 1\n")
    ColocarBarco(tabuleiro_j1)

    if modo == 1:
        clear()
        print("navio do jogador 2\n")
        ColocarBarco(tabuleiro_j2)
    else:
        print("navio da maquina colocado")
        linha = random.randint(0, tamanho - 1)
        coluna = random.randint(0, tamanho - TamanhoBarco)
        for i in range(TamanhoBarco):
            tabuleiro_j2[linha][coluna + i] = 'n'

    while True:
        print("turno do jogador 1:\n")
        PrintBoard(tiros_j1)
        realizar_ataque(tabuleiro_j2, tiros_j1)
        if vitoria(tabuleiro_j2):
            print("jogador 1 venceu!")
            break

        print("turno do jogador 2:\n")
        if modo == 1:
            PrintBoard(tiros_j2)
            realizar_ataque(tabuleiro_j1, tiros_j2)
        else:
            ataque_ia(tabuleiro_j1, tiros_j2)
        if vitoria(tabuleiro_j1):
            if modo == 1:
                print("jogador 2 venceu!")
            else:
                print("maquina venceu!")
            break

if __name__ == "__main__":
    main()