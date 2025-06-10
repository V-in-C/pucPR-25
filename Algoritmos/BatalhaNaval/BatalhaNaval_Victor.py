# configurações

TamanhoBarco = 1  # tamanho do barco
TamanhoMinimo = 10 # tamanho mínimo do tabuleiro
TamanhoMaximo = 26 # tamanho máximo do tabuleiro (de preferência no MÁXIMO 26 pra não passar as letras do alfabeto)

# código

import random
import os
import platform

# Importa as bibliotecas necessárias para impressão colorida no terminal
from colorama import Fore, Style, init
init(autoreset=True)  # Inicializa o colorama para resetar cores automaticamente

# Importa as bibliotecas datetime e time para manipulação de data e hora
import time
import datetime
arquivo_log = f"batalha_naval_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def clear():
    '''
    Limpa o console dependendo do sistema operacional.'''
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
clear()

def logger(arquivo, mensagem, level=1):
    '''
    Registra mensagens em um arquivo de log.
    Args:
        arquivo (str): Caminho do arquivo de log.
        mensagem (str): Mensagem a ser registrada.
        level (str): Nível de log (padrão é 'INFO').
    '''
    levels = [[1, "[INFO]"], [2, "[WARNING]"], [3, "[ERROR]"], [4, "[DEBUG]"]]

    with open(arquivo, "a") as f:
        f.write(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {levels[level-1][1]} {mensagem}\n")

def menu():
    '''
    Exibe o menu inicial do jogo e solicita as configurações do tabuleiro e modo de jogo.
    Parametros: None
    Retornos: Tamanho do tabuleiro e modo de jogo (1 para jogador vs jogador, 2 para jogador vs máquina).
    '''
    print(Fore.MAGENTA + Style.BRIGHT + "batalha naval\n")
    tamanho = int(input(Fore.CYAN + Style.BRIGHT + f"tamanho do tabuleiro ({TamanhoMinimo}-{TamanhoMaximo}): "))
    while tamanho < TamanhoMinimo or tamanho > TamanhoMaximo:
        clear()
        print(Fore.RED + "tamanho inválido\n")
        tamanho = int(input(Fore.CYAN + Style.BRIGHT + f"tamanho do tabuleiro ({TamanhoMinimo}-{TamanhoMaximo}): "))
    clear()
    modo = input("modo de jogo (1 = jogador vs jogador | 2 = jogador vs maquina): ")
    while modo not in ['1', '2']:
        clear()
        print(Fore.RED + "modo inválido\n")
        modo = input(Fore.CYAN + Style.BRIGHT + "modo de jogo (1 = jogador vs jogador | 2 = jogador vs maquina): ")

    return tamanho, int(modo)

def CriarBoard(tamanho):
    '''
    Cria um tabuleiro vazio com o tamanho especificado.
    Parametros: tamanho (int) - Tamanho do tabuleiro.
    Retornos: (list) - Tabuleiro vazio.
    '''
    return [['~' for _ in range(tamanho)] for _ in range(tamanho)]

def PrintBoard(tabuleiro):
    '''
    Exibe o tabuleiro formatado com letras para colunas e números para linhas.
    Parametros: tabuleiro (list) - Tabuleiro a ser exibido.
    Retornos: None
    '''
    # Exibe o tabuleiro formatado com letras para colunas e números para linhas.
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("\t", end="")
    for i in range(len(tabuleiro[0])):
        print(letras[i], end=" ")
    print()
    for i in range(len(tabuleiro)):
        linha = f"{i + 1}\t"
        for j in range(len(tabuleiro[i])):
            if tabuleiro[i][j] == 'n':
                linha += Fore.YELLOW + 'n ' + Style.RESET_ALL  # Navio
            elif tabuleiro[i][j] == 'X':
                linha += Fore.RED + 'X ' + Style.RESET_ALL  # Acerto
            elif tabuleiro[i][j] == 'O':
                linha += Fore.LIGHTBLACK_EX + 'O ' + Style.RESET_ALL  # Erro
            else:
                linha += Fore.BLUE + '~ ' + Style.RESET_ALL  # Água
        print(linha)

def LetraPNumero(letra):
    '''
    Converte uma letra (A-Z) para um número correspondente (0-25).
    Parametros: letra (str) - Letra a ser convertida.
    Retornos: (int) - Número correspondente (0-25).
    '''
    return ord(letra.upper()) - ord('A')

def NumeroPLetra(numero):
    '''
    Converte um número (0-25) para uma letra correspondente (A-Z).
    Parametros: numero (int) - Número a ser convertido.
    Retornos: (str) - Letra correspondente (A-Z).
    '''
    return chr(ord('A') + numero)

def vitoria(tabuleiro):
    '''
    Verifica se todos os barcos foram afundados no tabuleiro.
    Parametros: tabuleiro (list) - Tabuleiro a ser verificado.
    Retornos: (bool) - True se todos os barcos foram afundados, False caso contrário.
    '''
    for linha in tabuleiro:
        if 'n' in linha:
            return False
    return True

def adicionar_barco_pos(barcos_pos, tipo_barco, posicoes):
    """
    Adiciona as posições de um barco à lista de barcos.
    Cada barco é representado como uma lista, por exemplo: 
    [[tipo_barco, [posicoes]], ...]
    parametros:
        barcos_pos (list) - Lista de barcos já posicionados.
        tipo_barco (str) - Tipo do barco a ser adicionado.
        posicoes (list) - Lista de posições ocupadas pelo barco.
    Retornos: matriz de barcos_pos atualizada.
    """
    barcos_pos.append([tipo_barco, posicoes.copy()])
    return barcos_pos

def registrar_acerto(barcos_pos, linha, coluna):
    """
    Marca a posição atingida e verifica se algum barco foi afundado.
    Retorna (afundou, tipo_barco) se algum barco foi afundado, senão (False, None).
    """
    for barco in barcos_pos:
        if (linha, coluna) in barco[1]:
            barco[1].remove((linha, coluna))
            if len(barco[1]) == 0:
                tipo = barco[0]
                barcos_pos.remove(barco)
                return True, tipo
            return False, None
    return False, None

def barco_valido(tabuleiro, linha, coluna, orientacao, tamanho_barco):
    '''
    Verifica se a posição e orientação do barco são válidas.
    Parametros:
        tabuleiro (list) - Tabuleiro onde o barco será colocado.
        linha (int) - Linha inicial do barco.
        coluna (int) - Coluna inicial do barco.
        orientacao (str) - Orientação do barco ('h' para horizontal, 'v' para vertical).
        tamanho_barco (int) - Tamanho do barco.
    Retornos: (bool) - True se a posição é válida, False caso contrário.
    '''
    if orientacao == 'h':
        if coluna + tamanho_barco > len(tabuleiro[0]) or linha < 0 or linha >= len(tabuleiro):
            return False
        for i in range(tamanho_barco):
            if tabuleiro[linha][coluna + i] != '~':
                return False
    elif orientacao == 'v':
        if linha + tamanho_barco > len(tabuleiro) or coluna < 0 or coluna >= len(tabuleiro[0]):
            return False
        for i in range(tamanho_barco):
            if tabuleiro[linha + i][coluna] != '~':
                return False
    else:
        return False
    return True

def ColocarBarco(tabuleiro, tipo_barco='generico', tamanho_barco=TamanhoBarco):
    '''
    Solicita ao usuário a posição e orientação do barco e o coloca no tabuleiro.
    verifica se a posição é válida.
    Parametros: tabuleiro (list) - Tabuleiro onde o barco será colocado.
    Retorno: tabuleiro atualizado
    '''
    while True:
        print(Fore.CYAN + f"coloque seu navio {tipo_barco} (tamanho: {tamanho_barco})\n")
        while True:
            linha_input = input(Fore.CYAN + f"linha inicial do navio (1 - {len(tabuleiro)}): ")
            if linha_input.isdigit():
                linha = int(linha_input) - 1
                if 0 <= linha < len(tabuleiro):
                    break
                else:
                    print(Fore.RED + "Linha fora do intervalo do tabuleiro.")
            else:
                print(Fore.CYAN + "Por favor, digite um número válido para a linha.")
        while True:
            coluna_letra = input(Fore.CYAN + f"coluna inicial do navio (letra A - {NumeroPLetra(len(tabuleiro[0]) - 1)}): ").upper()
            if coluna_letra.isalpha() and 0 <= LetraPNumero(coluna_letra) < len(tabuleiro[0]):
                coluna = LetraPNumero(coluna_letra)
                break
            else:
                print(Fore.RED + "Por favor, digite uma letra válida para a coluna.")
        orientacao = input(Fore.CYAN + "horizontal (h) ou vertical (v): ").lower()

        if linha < 0 or linha >= len(tabuleiro) or coluna < 0 or coluna >= len(tabuleiro):
            print(Fore.RED + "posição inválida!")
            continue
        if orientacao not in ['h', 'v']:
            print(Fore.RED + "orientação inválida!")
            continue
        if not barco_valido(tabuleiro, linha, coluna, orientacao, tamanho_barco):
            print(Fore.RED + "posição inválida!")
            continue

        for i in range(tamanho_barco):
            if orientacao == 'h':
                tabuleiro[linha][coluna + i] = 'n'
            elif orientacao == 'v':
                tabuleiro[linha + i][coluna] = 'n'
        break
    
    return tabuleiro

def realizar_ataque(tabuleiro_alvo, tabuleiro_tiros):
    '''
    Solicita ao usuário a posição do ataque e atualiza os tabuleiros de acordo com o resultado.
    Parametros:
        tabuleiro_alvo (list) - Tabuleiro do adversário onde o ataque será realizado.
        tabuleiro_tiros (list) - Tabuleiro do jogador onde os tiros são registrados.
    Retornos:
        tabuleiro_alvo (list) - Tabuleiro atualizado com o resultado do ataque.
        tabuleiro_tiros (list) - Tabuleiro atualizado com o resultado do ataque.
        True se o ataque acertou, False se errou.
        posicao (tuple) - Posição do ataque (linha, coluna).
    '''
    while True:
        linha_input = input(Fore.CYAN + f"\nlinha de ataque (1 - {len(tabuleiro_tiros)}): ")
        if linha_input.isdigit():
            linha = int(linha_input) - 1
            if 0 <= linha < len(tabuleiro_alvo):
                break
            else:
                print("Linha fora do intervalo do tabuleiro.")
        else:
            print("Por favor, digite um número válido para a linha.")
    while True:
        coluna_letra = input(Fore.CYAN + f"coluna de ataque (letra A - {NumeroPLetra(len(tabuleiro_tiros[0]) - 1)}): ").upper()
        if coluna_letra.isalpha() and 0 <= LetraPNumero(coluna_letra) < len(tabuleiro_alvo[0]):
            coluna = LetraPNumero(coluna_letra)
            break
        else:
            print("Por favor, digite uma letra válida para a coluna.")
    clear()
    if tabuleiro_alvo[linha][coluna] == 'n':
        print(Fore.GREEN + "acertou!\n")
        tabuleiro_alvo[linha][coluna] = 'X' 
        tabuleiro_tiros[linha][coluna] = 'X'
        return tabuleiro_alvo, tabuleiro_tiros, True, (linha, coluna)
    elif tabuleiro_alvo[linha][coluna] == 'X':
        print(Fore.YELLOW + "ja acertou nessa posicao!\n")
        tabuleiro_tiros[linha][coluna] = 'X'
    else:
        print(Fore.RED + "errou!\n")
        tabuleiro_tiros[linha][coluna] = 'O'
    return tabuleiro_alvo, tabuleiro_tiros, False, (linha, coluna)

def ataque_ia(tabuleiro_alvo, tabuleiro_tiros):
    '''
    Realiza um ataque da máquina em uma posição aleatória do tabuleiro.
    Parametros:
        tabuleiro_alvo (list) - Tabuleiro do adversário onde o ataque será realizado.
        tabuleiro_tiros (list) - Tabuleiro da máquina onde os tiros são registrados.
    Retornos: True se o ataque acertou, False se errou.
    '''
    while True:
        linha = random.randint(0, len(tabuleiro_alvo) - 1)
        coluna = random.randint(0, len(tabuleiro_alvo) - 1)
        if tabuleiro_tiros[linha][coluna] == '~':
            break
    clear()
    print("maquina atacou na posição:", linha + 1, NumeroPLetra(coluna))
    if tabuleiro_alvo[linha][coluna] == 'n':
        print("maquina acertou!\n")
        tabuleiro_alvo[linha][coluna] = 'X'
        tabuleiro_tiros[linha][coluna] = 'X'
        return tabuleiro_alvo, tabuleiro_tiros, True
    elif tabuleiro_alvo[linha][coluna] == 'X':
        print("maquina ja acertou nessa posicao!\n")
        tabuleiro_tiros[linha][coluna] = 'X'
    else:
        print("maquina errou!\n")
        tabuleiro_tiros[linha][coluna] = 'O'
    return tabuleiro_alvo, tabuleiro_tiros, False

def atraso(segundos) -> None:
    """ 
    Implementa uma pausa programada para simular o tempo de espera entre turnos. Mostra um navio navegando no mar em modo animação.
    Parâmetros:
    - segundos: Tempo em segundos para a pausa.
    Retorna: None
    """
    frames = [
        " ~~~~~~🚢~~~~~~ ",
        "  ~~~~~🚢~~~~~  ",
        "   ~~~~🚢~~~~   ",
        "    ~~~🚢~~~    ",
        "     ~~🚢~~     ",
        "      ~🚢~      ",
        "       🚢       ",
        "      ~🚢~      ",
        "     ~~🚢~~     ",
        "    ~~~🚢~~~    ",
        "   ~~~~🚢~~~~   ",
        "  ~~~~~🚢~~~~~  ",
        " ~~~~~~🚢~~~~~~ "
    ]
    for frame in frames:
        print('\r' + Fore.BLUE + Style.BRIGHT + frame, end='', flush=True)
        time.sleep(0.15)
    print('\r' + ' ' * 20, end='\r')  # Limpa a linha
    print(Fore.BLUE + Style.BRIGHT + "Aguardando o próximo turno...")
    time.sleep(segundos-len(frames) * 0.15)  # Ajusta o tempo total de espera

def main():
    '''
    Função principal do jogo Batalha Naval.
    Parametros: None
    Retornos: Estatísticas do jogo.
    '''
    
    # Variáveis globais
    
    global TamanhoBarco, TamanhoMinimo, TamanhoMaximo
    global arquivo_log
    
    # Estatísticas do jogo
    
    turno = 1
    quantidade_tiros_j1 = 0
    acertos_j1 = 0
    quantidade_tiros_j2 = 0
    acertos_j2 = 0
    clear()
    
    # Configurações do jogo
    
    #barcos: [tipo, tamanho, quantidade]
    barcos = [["Encouraçado", 5, 1], ["Porta-avião", 4, 1], ["Contratorpedeiro", 3, 2], ["Submarino", 2, 2]]

    tamanho, modo = menu()
    logger(arquivo_log, f"Jogo iniciado -> Tamanho do tabuleiro: {tamanho} x {tamanho}, Modo: {'Jogador vs Jogador' if modo == 1 else 'Jogador vs Máquina'}")

    # Criação dos tabuleiros
    tabuleiro_j1 = CriarBoard(tamanho)
    tiros_j1 = CriarBoard(tamanho)

    tabuleiro_j2 = CriarBoard(tamanho)
    tiros_j2 = CriarBoard(tamanho)

    clear()
    
    # Colocação dos barcos
    print(Fore.BLUE + "navio do jogador 1\n")
    for barco in barcos:
        for _ in range(barco[2]):
            tabuleiro_j1 = ColocarBarco(tabuleiro_j1, barco[0], barco[1])
            PrintBoard(tabuleiro_j1)
    print(Fore.GREEN + Style.BRIGHT + "Barcos do jogador 1 colocados no tabuleiro.")
    print(Fore.YELLOW + Style.BRIGHT + "Pressione Enter para continuar...")
    input()
    logger(arquivo_log, "Barcos do jogador 1 colocados no tabuleiro.")
    clear()

    if modo == 1:
        print(Fore.GREEN + "navio do jogador 2\n")
        for barco in barcos:
            for _ in range(barco[2]):
                tabuleiro_j2 = ColocarBarco(tabuleiro_j2, barco[0], barco[1])
                PrintBoard(tabuleiro_j2)
        logger(arquivo_log, "Barcos do jogador 2 colocados no tabuleiro.")
    else:
        print(Fore.YELLOW + "navio da maquina colocado")
        for barco in barcos:
            for _ in range(barco[2]):
                linha = random.randint(0, tamanho - 1)
                coluna = random.randint(0, tamanho - barco[1])
                orientacao = random.choice(['h', 'v'])
                while not barco_valido(tabuleiro_j2, linha, coluna, orientacao, barco[1]):
                    linha = random.randint(0, tamanho - 1)
                    coluna = random.randint(0, tamanho - barco[1])
                    orientacao = random.choice(['h', 'v'])
                for i in range(barco[1]):
                    if orientacao == 'h':
                        tabuleiro_j2[linha][coluna + i] = 'n'
                    elif orientacao == 'v':
                        tabuleiro_j2[linha + i][coluna] = 'n'
        logger(arquivo_log, "Barcos da máquina colocados no tabuleiro.")
    
    
    # Início de ataques
    while True:
        print(Fore.YELLOW + "turno do jogador 1:\n")
        print(Fore.BLUE + Style.BRIGHT + "Tabuleiro do Jogador 1:")
        PrintBoard(tabuleiro_j1)
        print(Fore.GREEN + Style.BRIGHT + "Tabuleiro de Tiros do Jogador 1:")
        PrintBoard(tiros_j1)
        tabuleiro_j2, tiros_j1, acertou, posicao = realizar_ataque(tabuleiro_j2, tiros_j1)
        if acertou:
            print(Fore.GREEN + "jogador 1 acertou!\n")
            acertos_j1 += 1
        else:
            print(Fore.RED + "jogador 1 errou!\n")
        quantidade_tiros_j1 += 1
        if vitoria(tabuleiro_j2):
            print(Fore.GREEN + "jogador 1 venceu!")
            break
        input(Fore.YELLOW + Style.BRIGHT + "Pressione Enter para continuar...")
        if modo == 1:
            print(Fore.YELLOW + "turno do jogador 2:\n")
            print(Fore.BLUE + Style.BRIGHT + "Tabuleiro do Jogador 2:")
            print(Fore.GREEN + Style.BRIGHT + "Tabuleiro de Tiros do Jogador 2:")
            tabuleiro_j1, tiros_j2, acertou, posicao = realizar_ataque(tabuleiro_j1, tiros_j2)
            if acertou:
                print(Fore.GREEN + "jogador 2 acertou!\n")
                acertos_j2 += 1
            else:
                print(Fore.RED + "jogador 2 errou!\n")
            quantidade_tiros_j2 += 1
            if vitoria(tabuleiro_j1):
                print(Fore.GREEN + "jogador 2 venceu!")
                break
        else:
            print(Fore.YELLOW + "turno da maquina:\n")
            atraso(5) # Simula um atraso para o ataque da máquina
            tabuleiro_j1, tiros_j2, acertou, posicao = ataque_ia(tabuleiro_j1, tiros_j2)
            if acertou:
                print(Fore.GREEN + "maquina acertou!\n")
                acertos_j2 += 1
            else:
                print(Fore.RED + "maquina errou!\n")
            quantidade_tiros_j2 += 1
            if vitoria(tabuleiro_j1):
                print(Fore.GREEN + "maquina venceu!")
                break
        turno += 1
        logger(arquivo_log, f"Turno {turno}: Jogador 1 - Tiros: {quantidade_tiros_j1}, Acertos: {acertos_j1}; Jogador 2 - Tiros: {quantidade_tiros_j2}, Acertos: {acertos_j2}")
        clear()
      
    #Mostra es estatísticas do jogo
    print(Fore.MAGENTA + Style.BRIGHT + f"\nEstatísticas do jogo:")
    print(Fore.CYAN + Style.BRIGHT + f"Jogador 1 - Tiros: {quantidade_tiros_j1}, Acertos: {acertos_j1}")
    print(Fore.CYAN + Style.BRIGHT + f"Jogador 2 - Tiros: {quantidade_tiros_j2}, Acertos: {acertos_j2}")
    logger(arquivo_log, f"Estatísticas do jogo: Jogador 1 - Tiros: {quantidade_tiros_j1}, Acertos: {acertos_j1}; Jogador 2 - Tiros: {quantidade_tiros_j2}, Acertos: {acertos_j2}")

    #Verifica se quer continuar jogando
    continuar = input(Fore.CYAN + Style.BRIGHT + "Deseja jogar novamente? (s/n): ").lower()
    while continuar not in ['s', 'n']:
        print(Fore.RED + "Opção inválida. Tente novamente.")
        continuar = input(Fore.CYAN + Style.BRIGHT + "Deseja jogar novamente? (s/n): ").lower()
    if continuar == 's':
        main()
    else:
        print(Fore.GREEN + Style.BRIGHT + "Obrigado por jogar Batalha Naval!")
        logger(arquivo_log, "Jogo encerrado pelo usuário.")  

if __name__ == "__main__":
    main()