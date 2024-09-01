#exer 1
with open('C:/Users/anacs/trainee-repositorio/SPRINT_4/exercicios/number.txt') as file:
    numeros = list(map(int, file.read().splitlines()))
    def pares():
        return list(filter(lambda item: item % 2 == 0, numeros))
    def filtrado(funcao):
        return sorted(funcao(), reverse=True)[:5]
    resultado = filtrado(pares)
print(resultado)
#exer 2
def quantidade(qtd):
    return len(qtd)
def conta_vogais(texto):
    vogais = filter(lambda l: l in 'aeiou', texto.lower())
    return quantidade(list(vogais))
print(type(conta_vogais("Ana Abacaxi")))
#exer 3
from functools import reduce
def calcula_saldo(lancamentos):
    valor = map(lambda item: item[0] if item[1] == 'C' else -item[0], lancamentos)
    saldo_final = reduce(lambda acumulador,item:acumulador + item, valor,0)
    return saldo_final
lancamentos = [
    (200, 'D'),
    (300, 'C'),
    (100, 'C')
]

print(calcula_saldo(lancamentos))
# exer 4
def calcular_valor_maximo(operadores, operandos) -> float:
    def soma(x, y):
        return x + y

    def substracao(x, y):
        return x - y

    def multiplicacao(x, y):
        return x * y

    def divisao(x, y):
        return x / y
    def resto(x,y):
        return x % y 
    funcoes = {
        '+': soma,
        '-': substracao,
        '*': multiplicacao,
        '/': divisao,
        '%': resto,
    }

    resultados = list(map(lambda x: funcoes[x[0]](x[1][0], x[1][1]),zip(operadores, operandos)))
    return max(resultados)

operadores = ['+', '-', '*', '/', '+']
operandos = [(3, 6), (-7, 4.9), (8, -8), (10, 2), (8, 4)]

print(calcular_valor_maximo(operadores, operandos))

# exer 5
with open('C:\\Users\\anacs\\trainee-repositorio\\SPRINT_4\\exercicios\\estudantes.csv','r') as file:
    dados_processados = []
    for linha in file:
        dados = linha.strip().split(',')
        nome = dados[0]
        notas = list(map(int, dados[1:]))
        notas.sort(reverse=True)
        tres_maiores = notas[:3]
        media = round(sum(tres_maiores) / 3, 2)
        dados_processados.append((nome, tres_maiores, media))
        dados_processados = sorted(dados_processados, key=lambda x: x[0])

    for nome,tres_maiores,media in dados_processados:
        print(f"Nome: {nome} Notas: {tres_maiores} Média: {media}")
# exer 6
def maiores_que_media(conteudo:dict)->list:
    media_produtos=sum(conteudo.values())/len(conteudo)
    acima_media= [(item,valor) for item,valor in conteudo.items() if valor >media_produtos]
    return sorted(acima_media,key=lambda x :x [1])

conteudo={
    "arroz": 4.99,
    "feijão": 3.49,
    "macarrão": 2.99,
    "leite": 3.29,
    "pão": 1.99
}
print(maiores_que_media(conteudo))
# exer 7
def pares_ate(n: int):
    for i in range(2, n+1):
        if i % 2 == 0:
            yield i
pares=pares_ate(10)
print(next(pares))
print(next(pares))




