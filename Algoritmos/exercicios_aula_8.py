'''
Ex 1 – Saudação com horário
Crie uma função `saudacao(nome)` que recebe um nome e imprime uma saudação personalizada de acordo com o **horário atual do sistema**:

- Antes das 12h: "Bom dia, [nome]!"
- Entre 12h e 18h: "Boa tarde, [nome]!"
- Após 18h: "Boa noite, [nome]!"

Utilize o módulo `datetime` para obter o horário atual.  
*Desafio extra*: permita que a função aceite um horário como parâmetro opcional (para testes).
'''

def saudacao(nome, horario=None):
    from datetime import datetime

    if horario is None:
        horario = datetime.now().hour
    else:
        horario = int(horario)

    if horario < 12:
        saudacao = f"Bom dia, {nome}!"
    elif 12 <= horario < 18:
        saudacao = f"Boa tarde, {nome}!"
    else:
        saudacao = f"Boa noite, {nome}!"

    print(saudacao) 
# Chamada da função
# saudacao("João")

'''
Ex 2 Retornar o maior, com validação e lista
Crie uma função `maior_elemento(lista)` que:

1. Recebe uma **lista de números** como argumento.
2. Valida se todos os elementos são realmente numéricos.
3. Retorna o **maior número** da lista.
4. Caso a lista esteja vazia ou inválida, retorne uma mensagem apropriada.

```python
maior_elemento([3, 7, 2, 10, 4]) → 10
maior_elemento([]) → "Lista vazia"
'''
def maior_elemento(lista):
    if not lista:
        return "Lista vazia"
    
    if not all(isinstance(x, (int, float)) for x in lista):
        return "Lista inválida, todos os elementos devem ser numéricos"

    maior = max(lista)
    return maior
# Chamada da função
# print(maior_elemento([3, 7, 2, 10, 4]))

'''
Ex 3 – Desafio Final (Mini Projeto)
Crie uma função chamada `menu()` que exibe um menu para o usuário com opções:

1. Calcular IMC  
2. Verificar maior de dois números  
3. Sair

A cada opção, chame a função correspondente.
'''
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return imc

def verificar_maior(a, b):
    return max(a, b)

def menu():
    while True:
        print("Menu:")
        print("1. Calcular IMC")
        print("2. Verificar maior de dois números")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            peso = float(input("Digite o peso (kg): "))
            altura = float(input("Digite a altura (m): "))
            imc = calcular_imc(peso, altura)
            print(f"Seu IMC é: {imc:.2f}")
        elif opcao == "2":
            a = float(input("Digite o primeiro número: "))
            b = float(input("Digite o segundo número: "))
            maior = verificar_maior(a, b)
            print(f"O maior número é: {maior}")
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
# Chamada da função
# menu()

'''
Ex Extra – Fatorial Recursivo
Crie uma função recursiva `fatorial(n)` que calcula o fatorial de um número inteiro positivo `n`. O fatorial de `n` é o produto de todos os números inteiros de 1 até `n`.
'''
def fatorial(n):
    if n == 0:
        return 1
    else:
        return n * fatorial(n-1)
# Chamada da função
print(fatorial(5))  # Exemplo: 5! = 120