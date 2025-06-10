"""
Desenvolver um jogo completo e funcional de Batalha Naval em Python, aplicando conceitos fundamentais de programação, como manipulação de matrizes bidimensionais, funções, estruturas de repetição, condicionais, validação de entrada, encapsulamento e exibição formatada no terminal.
"""
import random
import time
from colorama import init, Fore, Back, Style
init(autoreset=True)
log_level = 1  # Nível de log (1 para INFO, 2 para DEBUG, 3 para ERROR)
arquivo_log = f"partida_batalha_naval_{int(time.time())}.txt"


def menu_inicial() -> tuple:
    """
    Exibe o menu inicial do jogo e coleta as configurações do usuário.
    Parâmetros: Nenhum.
    Retorna: (int, int) Tamanho do tabuleiro (ex: 10 para 10x10) e modo de jogo escolhido pelo usuário (1 para Jogador vs Jogador, 2 para Jogador vs IA).
    """
    print(Fore.CYAN + Style.BRIGHT + "Bem-vindo ao Batalha Naval!")
    print()
    tamanho = int(input(Fore.CYAN + "Digite o tamanho do tabuleiro (ex: 10 para 10x10): "))
    
    while tamanho < 10:
        print(Fore.RED + "Tamanho inválido. Tente novamente.")
        tamanho = input(Fore.CYAN + "Digite o tamanho do tabuleiro (ex: 10 para 10x10): ")
    
    modo = input(Fore.CYAN + "Escolha o modo de jogo (1 para Jogador vs Jogador, 2 para Jogador vs IA): ")
    
    while modo not in ['1', '2']:
        print(Fore.RED + "Modo inválido. Tente novamente.")
        modo = input(Fore.CYAN + "Digite o número do modo (1 para Jogador vs Jogador, 2 para Jogador vs IA): ")

    return int(tamanho), int(modo)

def configurar_tabuleiro(tamanho) -> tuple:
    """
    Cria duas matrizes bidimensionais para o tabuleiro do jogador. 
    Parâmetros:
    - tamanho: Tamanho do tabuleiro (número de linhas e colunas).
    - A matriz do tabuleiro é inicializada com '~' para representar água.
    Retorna: (matriz, matriz) Duas matrizes: uma para o próprio tabuleiro e outra para os ataques realizados.
    """
    tabuleiro = [['~' for _ in range(tamanho)] for _ in range(tamanho)]
    ataques = [['~' for _ in range(tamanho)] for _ in range(tamanho)]
    return tabuleiro, ataques

def exibir_tabuleiro(tabuleiro, ataques) -> None:
    """
    Exibe o tabuleiro do jogador e a matriz de ataques realizados.
    Parâmetros:
    - tabuleiro: Matriz do tabuleiro do jogador.
    - ataques: Matriz de ataques.
    Retorna: None
    """
    tamanho = len(tabuleiro)
    print(Fore.YELLOW + Style.BRIGHT + "Tabuleiro do Jogador:")
    print(f"\t{' '.join([chr(65 + i) for i in range(tamanho)])}")  # Colunas alfabéticas
    for i in range(tamanho):
        linha = f"{i + 1}\t"
        for j in range(tamanho):
            if tabuleiro[i][j] == 'N':
                linha += Fore.YELLOW + 'N ' + Style.RESET_ALL  # Navio
            elif ataques[i][j] == 'X':
                linha += Fore.RED + 'X ' + Style.RESET_ALL  # Acerto
            elif ataques[i][j] == 'O':
                linha += Fore.LIGHTBLACK_EX + 'O ' + Style.RESET_ALL  # Erro
            else:
                linha += Fore.BLUE + '~ ' + Style.RESET_ALL  # Água
        print(linha)
    if ataques:
        print(Fore.RED + Style.BRIGHT + "\nTabuleiro de Ataques:")
        print(f"\t{' '.join([chr(65 + i) for i in range(tamanho)])}")  # Colunas alfabéticas
        for i in range(tamanho):
            linha = f"{i + 1}\t"
            for j in range(tamanho):
                if ataques[i][j] == 'X':
                    linha += Fore.RED + 'X ' + Style.RESET_ALL  # Acerto
                elif ataques[i][j] == 'O':
                    linha += Fore.LIGHTBLACK_EX + 'O ' + Style.RESET_ALL  # Erro
                else:
                    linha += Fore.GREEN + '~ ' + Style.RESET_ALL  # Água
        print(linha)

def posicionar_navios(tabuleiro, tamanho, auto=False) -> list:
    """
    Permite ao jogador posicionar seus navios no tabuleiro, mostrando o tabuleiro a cada passo.
    Parametros:
    - tabuleiro: Matriz do tabuleiro do jogador.
    - tamanho: Tamanho do tabuleiro.
    - auto: (bool) Indica se a escolha é automática, caso escolha por IA  (padrão é False, ou seja, não automático).
    Retorna: (matriz) tabuleiro atualizado com os navios posicionados.
    """
    
    #navios: [tipo, tamanho, quantidade]
    navios = [["Encouraçado", 5, 1], ["Porta-avião", 4, 1], ["Contratorpedeiro", 3, 2], ["Submarino", 2, 2]]
    
    if not auto:
        for navio in navios:
            tipo, tamanho_navio, quantidade = navio        
            for _ in range(quantidade):
                posicionado = False
                print(Fore.GREEN + Style.BRIGHT + f"\nPosicione seu {tipo} (tamanho {tamanho_navio}):")
                while not posicionado:
                    orientacao = input(Fore.GREEN + "Escolha a orientação (H para horizontal, V para vertical): ").upper()
                    while orientacao not in ['H', 'V']:
                        print(Fore.RED + "Orientação inválida. Tente novamente.")
                        orientacao = input(Fore.GREEN + "Escolha a orientação (H para horizontal, V para vertical): ").upper()

                    posicao = input(Fore.GREEN + "Digite a coordenada inicial (ex: A1 para coluna A e linha 1): ").upper()
                    while len(posicao) < 2 or len(posicao) > 3:
                        print(Fore.RED + "Coordenada inválida. Tente novamente.")
                        posicao = input(Fore.GREEN + "Digite a coordenada inicial (ex: A1 para coluna A e linha 1): ").upper()
                    coluna = ord(posicao[0]) - 65
                    linha = int(posicao[1:]) - 1
                    if orientacao == 'H':
                        cabe_no_tabuleiro = coluna + tamanho_navio <= tamanho
                        for i in range(tamanho_navio):
                            if cabe_no_tabuleiro and tabuleiro[linha][coluna + i] == '~':
                                continue
                            else:
                                cabe_no_tabuleiro = False
                                break
                        if cabe_no_tabuleiro:
                            for i in range(tamanho_navio):
                                tabuleiro[linha][coluna + i] = 'N'
                            posicionado = True
                    elif orientacao == 'V':
                        cabe_no_tabuleiro = linha + tamanho_navio <= tamanho
                        for i in range(tamanho_navio):
                            if cabe_no_tabuleiro and tabuleiro[linha + i][coluna] == '~':
                                continue
                            else:
                                cabe_no_tabuleiro = False
                                break
                        if cabe_no_tabuleiro:
                            for i in range(tamanho_navio):
                                tabuleiro[linha + i][coluna] = 'N'
                            posicionado = True
                    if not posicionado:
                        print(Fore.RED + "Posição inválida ou já ocupada. Tente novamente.")
                exibir_tabuleiro(tabuleiro, [])
    else:
        for navio in navios:
            tipo, tamanho_navio, quantidade = navio
            for _ in range(quantidade):
                posicionado = False
                while not posicionado:
                    orientacao = random.choice(['H', 'V'])
                    coluna = random.randint(0, tamanho - 1)
                    linha = random.randint(0, tamanho - 1)
                    if orientacao == 'H':
                        cabe_no_tabuleiro = coluna + tamanho_navio <= tamanho
                        for i in range(tamanho_navio):
                            if cabe_no_tabuleiro and tabuleiro[linha][coluna + i] == '~':
                                continue
                            else:
                                cabe_no_tabuleiro = False
                                break
                        if cabe_no_tabuleiro:
                            for i in range(tamanho_navio):
                                tabuleiro[linha][coluna + i] = 'N'
                            posicionado = True
                    elif orientacao == 'V':
                        cabe_no_tabuleiro = linha + tamanho_navio <= tamanho
                        for i in range(tamanho_navio):
                            if cabe_no_tabuleiro and tabuleiro[linha + i][coluna] == '~':
                                continue
                            else:
                                cabe_no_tabuleiro = False
                                break
                        if cabe_no_tabuleiro:
                            for i in range(tamanho_navio):
                                tabuleiro[linha + i][coluna] = 'N'
                            posicionado = True
    print(Fore.GREEN + Style.BRIGHT + "Todos os navios posicionados com sucesso!") 
    return tabuleiro

def Jogador_ataca(tabuleiro, ataques, linha, coluna, ultimo_acerto=None) -> tuple:
    '''
    Simula o ataque do jogador, atualizando as matrizes de ataques e tabuleiro.
    Parâmetros:
    - tabuleiro: Matriz do tabuleiro do jogador atacado.
    - ataques: Matriz de ataques realizados.
    - linha: Linha do ataque.
    - coluna: Coluna do ataque.
    - ultimo_acerto: (coluna, linha) da última posição acertada, usada para IA.
    Retorna: (bool, tabuleiro, ataques, ultimo_acerto)
    - True se o ataque foi bem-sucedido (acerto), False se foi um erro (água).
    - tabuleiro: Matriz do tabuleiro atualizada.
    - ataques: Matriz de ataques atualizada.
    - ultimo_acerto: (coluna, linha) da última posição acertada, usada para IA.
    '''
    if tabuleiro[linha][coluna] == 'N':
        ataques[linha][coluna] = 'X'
        tabuleiro[linha][coluna] = 'X'
        print(Fore.GREEN + "Acertou!")
        ultimo_acerto = (coluna, linha)
    else:
        ataques[linha][coluna] = 'O'
        print(Fore.YELLOW + "Água!")
        ultimo_acerto = None

    exibir_tabuleiro(tabuleiro, ataques)
    return tabuleiro[linha][coluna] == 'X', tabuleiro, ataques, ultimo_acerto
     
def realizar_ataque(tabuleiro, ataques, tamanho, modoAI = False, ultimo_acerto=None) -> tuple:
    """
    Processa o ataque do jogador ou da IA, atualizando as matrizes de ataques e tabuleiro.
    Parâmetros:
    - tabuleiro: Matriz do tabuleiro do jogador atacado.
    - ataques: Matriz de ataques realizados.
    - tamanho: Tamanho do tabuleiro.
    - modoAI: (bool) (opcional) Indica se o ataque é da IA (padrão é False, ou seja, jogador ataca).
    - ultimo_acerto: (coluna, linha) (opcional) Última posição acertada, usada para IA.
    Retorna: (True/False, ataques, ultimo_acerto, proximos_alvos) 
    - True se o ataque foi bem-sucedido (acerto), False se foi um erro (água).
    - tabuleiro: Matriz do tabuleiro atualizada.
    - ataques: Matriz de ataques atualizada.
    - ultimo_acerto: (opcional) Última posição acertada, usada para IA.
    """
    if not modoAI:
        print(Fore.YELLOW + Style.BRIGHT + "Realizando ataque...")
        while True:
            posicao = input("Digite a coordenada de ataque (ex: A1 para coluna A e linha 1): ").upper() 
            while len(posicao) < 2 or len(posicao) > 3:
                print(Fore.RED + "Coordenada inválida. Tente novamente.")
                posicao = input("Digite a coordenada de ataque (ex: A1 para coluna A e linha 1):  ").upper()
            coluna = ord(posicao[0]) - 65
            linha = int(posicao[1:]) - 1
            
            if coluna < 0 or coluna >= tamanho or linha < 0 or linha >= tamanho:
                print(Fore.RED + "Coordenada fora dos limites do tabuleiro. Tente novamente.")
                continue
            
            if ataques[linha][coluna] != '~':
                print(Fore.RED + "Você já atacou essa posição. Tente novamente.")
                continue
            return Jogador_ataca(tabuleiro, ataques, linha, coluna)

    else: 
        print(Fore.YELLOW + Style.BRIGHT + "A IA está realizando um ataque...")
        if ultimo_acerto is None:
            # IA ataca aleatoriamente
            while True:
                coluna = random.randint(0, tamanho - 1)
                linha = random.randint(0, tamanho - 1)
                if ataques[linha][coluna] == '~':
                    return Jogador_ataca(tabuleiro, ataques, linha, coluna, ultimo_acerto)
        else:
            # IA ataca baseado no último acerto
            coluna, linha = ultimo_acerto
            direcoes = [(-1,0),(1,0),(0,-1),(0,1)]
            dx, dy = random.choice(direcoes)
            coluna += dx
            linha += dy
            if 0 <= coluna < tamanho and 0 <= linha < tamanho:
                if ataques[linha][coluna] == '~':
                    return Jogador_ataca(tabuleiro, ataques, linha, coluna, ultimo_acerto)

def navio_afundado(tabuleiro, ultimo_acerto) -> bool:
    '''
    Verifica se todas as partes do navio atingido foram destruídas
    Checa nas 4 direções a partir do ponto atingido
    parâmetros:
    - tabuleiro: Matriz do tabuleiro do jogador.
    - ultimo_acerto: (coluna, linha) da última posição acertada.
    Retorna: (bool) True se o navio foi afundado, False caso contrário.
    '''
    if ultimo_acerto is None:
        return False

    coluna, linha = ultimo_acerto
    direcoes = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx, dy in direcoes:
        x, y = coluna, linha
        while 0 <= y < len(tabuleiro) and 0 <= x < len(tabuleiro):
            if tabuleiro[y][x] == 'N':
                return False
            if tabuleiro[y][x] != 'X':
                break
            x += dx
            y += dy
    return True

def verificar_vitoria(tabuleiro) -> bool:
    """
    Verifica se todos os navios foram afundados.
    Parametros:
    - tabuleiro: Matriz do tabuleiro do jogador.
    Retorna: (bool) True se todos os navios foram afundados, False caso contrário.
    """
    for linha in tabuleiro:
        if 'N' in linha:
            return False
    return True

def delay(segundos) -> None:
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
    time.sleep(segundos)
    
def logger(arquivo, texto, level=1) -> None:
    """
    Logger que registra as jogadas em um arquivo de texto.
    Parâmetros:
    - arquivo: Caminho do arquivo onde as jogadas serão registradas.
    - texto: Texto a ser registrado no arquivo.
    - level: Nível de log (1 para INFO, 2 para DEBUG, 3 para ERROR).
    Retorna: None
    """
    if level == 1:
        log_lvl = "[INFO] "
    elif level == 2:
        log_lvl = "[DEBUG] "
    elif level == 3:
        log_lvl = "[ERROR] "
    with open(arquivo, 'a') as f:
        f.write(Fore.BLUE + Style.BRIGHT + str(time.localtime()) + ": " + texto + '\n')
        
def jogo():
    """
    Função principal que controla o fluxo do jogo.
    O jogo termina quando todos os navios do jogador forem completamente afundados.
    O programa deve apresenar:
    - O vencedor do jogo.
    - Estatísticas como número de tiros realizados, tiros certeiros e navios afundados
    """
    tiros_realizados = 0
    tiros_certeiros = 0
    navios_afundados = 0
    
    data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ultimo_acerto = None

    tamanho, modo = menu_inicial()
    tabuleiro_jogador1, ataques_jogador1 = configurar_tabuleiro(tamanho)
    tabuleiro_jogador2, ataques_jogador2 = configurar_tabuleiro(tamanho)

    logger(arquivo_log, f"Jogo iniciado em {data}. Tamanho do tabuleiro: {tamanho}x{tamanho}, Modo: {'Jogador vs Jogador' if modo == 1 else 'Jogador vs IA'}")
    
    print(Fore.YELLOW + Style.BRIGHT + f"Você escolheu modo de jogo: {'Jogador vs Jogador' if modo == 1 else 'Jogador vs IA'}")
    print()
    print(Fore.YELLOW + Style.BRIGHT + "É a vez do Jogador 1 posicionar seus navios. Pressione Enter para continuar...")
    input()
    tabuleiro_jogador1 = posicionar_navios(tabuleiro_jogador1, tamanho)
    print(Fore.YELLOW + Style.BRIGHT + "Tabuleiro do Jogador 1:")
    exibir_tabuleiro(tabuleiro_jogador1, ataques_jogador1)
    delay(5)

    if modo == 1:
        print(Fore.YELLOW + Style.BRIGHT + "Agora é a vez do Jogador 2 posicionar seus navios. Pressione Enter para continuar...")
        input()
        tabuleiro_jogador2 = posicionar_navios(tabuleiro_jogador2, tamanho)
        print(Fore.YELLOW + Style.BRIGHT + "Tabuleiro do Jogador 2:")
        exibir_tabuleiro(tabuleiro_jogador2, ataques_jogador2)
        delay(5)
    else:
        print(Fore.CYAN + Style.BRIGHT + "Você escolheu Jogador vs IA!")
        tabuleiro_jogador2 = posicionar_navios(tabuleiro_jogador2, tamanho, True)
        delay(5)

    while True:
        if modo == 1:
            print(Fore.CYAN + Style.BRIGHT + "É a vez do Jogador 1!")
            acerto, ataques_jogador1, ultimo_acerto, proximos_alvos = realizar_ataque(tabuleiro_jogador2, ataques_jogador1, tamanho, modoAI=False)
            logger(arquivo_log, f"Jogador 1 atacou: {'Acertou' if acerto else 'Errou'} na posição {ultimo_acerto}")
            tiros_realizados += 1
            if acerto:
                tiros_certeiros += 1
                if verificar_vitoria(tabuleiro_jogador2):
                    navios_afundados += 1
                    print(Fore.GREEN + Style.BRIGHT + "Jogador 1 afundou um navio!")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Jogador 1 errou o ataque.")
            if verificar_vitoria(tabuleiro_jogador2):
                print(Fore.GREEN + Style.BRIGHT + "Jogador 1 venceu!")
                break
            
            print(Fore.CYAN + Style.BRIGHT + "É a vez do Jogador 2!")
            acerto, ataques_jogador2, ultimo_acerto, proximos_alvos = realizar_ataque(tabuleiro_jogador1, ataques_jogador2, tamanho, modoAI=False)
            tiros_realizados += 1
            if acerto:
                tiros_certeiros += 1
                if verificar_vitoria(tabuleiro_jogador1):
                    navios_afundados += 1
                    print(Fore.GREEN + Style.BRIGHT + "Jogador 2 afundou um navio!")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Jogador 2 errou o ataque.")
            if verificar_vitoria(tabuleiro_jogador1):
                print(Fore.GREEN + Style.BRIGHT + "Jogador 2 venceu!")
                break

        else:
            print(Fore.CYAN + Style.BRIGHT + "É a sua vez de atacar a IA!")
            acerto, ataques_jogador1, ultimo_acerto, proximos_alvos = realizar_ataque(tabuleiro_jogador2, ataques_jogador1, tamanho, modoAI=False)
            tiros_realizados += 1
            if acerto:
                tiros_certeiros += 1
                if verificar_vitoria(tabuleiro_jogador2):
                    navios_afundados += 1
                    print(Fore.GREEN + Style.BRIGHT + "Você afundou um navio da IA!")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "Você errou o ataque.")
            if verificar_vitoria(tabuleiro_jogador2):
                print(Fore.GREEN + Style.BRIGHT + "Você venceu a IA!")
                break
            
            print(Fore.CYAN + Style.BRIGHT + "É a vez da IA atacar!")
            acerto, ataques_jogador2, ultimo_acerto, proximos_alvos = realizar_ataque(tabuleiro_jogador1, ataques_jogador2, tamanho, modoAI=True, ultimo_acerto=ultimo_acerto, proximos_alvos=proximos_alvos)
            tiros_realizados += 1
            if acerto:
                tiros_certeiros += 1
                if verificar_vitoria(tabuleiro_jogador1):
                    navios_afundados += 1
                    print(Fore.GREEN + Style.BRIGHT + "A IA afundou um navio seu!")
            else:
                print(Fore.YELLOW + Style.BRIGHT + "A IA errou o ataque.")
            if verificar_vitoria(tabuleiro_jogador1):
                print(Fore.RED + Style.BRIGHT + "A IA venceu!")
                break
    print(Fore.YELLOW + Style.BRIGHT + "Fim do jogo!")
    print(Fore.YELLOW + Style.BRIGHT + f"Estatísticas: Tiros realizados: {tiros_realizados}, Tiros certeiros: {tiros_certeiros}, Navios afundados: {navios_afundados}")
    logger("batalha_naval.log", f"Jogo finalizado. Estatísticas: Tiros realizados: {tiros_realizados}, Tiros certeiros: {tiros_certeiros}, Navios afundados: {navios_afundados}")
if __name__ == "__main__":
    jogo()
    #Verifica se quer continuar jogando
    continuar = input(Fore.CYAN + Style.BRIGHT + "Deseja jogar novamente? (s/n): ").lower()
    while continuar not in ['s', 'n']:
        print(Fore.RED + "Opção inválida. Tente novamente.")
        continuar = input(Fore.CYAN + Style.BRIGHT + "Deseja jogar novamente? (s/n): ").lower()
    if continuar == 's':
        jogo()
    else:
        print(Fore.GREEN + Style.BRIGHT + "Obrigado por jogar Batalha Naval!")
        logger(arquivo_log, "Jogo encerrado pelo usuário.")
        print(Fore.GREEN + Style.BRIGHT + "Desenvolvido por Victor de Souza Maia.")
        print(Fore.GREEN + Style.BRIGHT + "Versão 1.0")
        exit()
# Fim do jogo