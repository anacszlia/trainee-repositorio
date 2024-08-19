#exer 6
a = [1, 1, 2, 3, 5, 8, 14, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
lista_resultante = list(set(a).intersection(set(b)))
print(lista_resultante)
#exer 7
a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
nova_lista = [numero for numero in a if numero % 2 != 0]
print(nova_lista)
#exer 8
palavras=['maça', 'arara', 'audio', 'radio', 'radar', 'moto']
for palavra in palavras:
    if palavra == palavra[::-1]:
        print(f'A palavra: {palavra} é um palíndromo')
    else:
        print(f'A palavra: {palavra} não é um palíndromo') 
#exer 9
primeirosNomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobreNomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]
for i ,primeiroNome in enumerate(primeirosNomes):
    print(f'{i} - {primeirosNomes[i]} {sobreNomes[i]} está com {idades[i]} anos')
#exer 10 transformar em conjunto
def semRepeticao(lista):
    nova_lista=list(set(lista))
    return nova_lista
lista_repetitiva=['abc', 'abc', 'abc', '123', 'abc', '123', '123']
print(semRepeticao(lista_repetitiva))
# exer 11 ler arquivo json
import json
with open('person.json') as pj:
    y = json.load(pj)
    
print(y)
#exer 12

def my_map(list):
    return list **2
lista=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
listaPotencia=list(map(my_map,lista))
print(listaPotencia)

#exer 13
with open('arquivo_texto.txt',encoding='utf-8') as file:
    ler=file.read()
print(ler,end='')

#exer 14
def parametrosNnomeados(*args,**kwargs):
    for arg in args:
        print(arg)
    for value in kwargs.values():
        print(value)
    
parametrosNnomeados(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)

#exer 15
class Lampada:
    def __init__(self, estado_inicial):
        self.ligada = estado_inicial
    def liga(self):
        self.ligada = True
    def desliga(self):
        self.ligada = False
    def esta_ligada(self):
        return self.ligada

lampada = Lampada(True)

lampada.liga()
print("A lâmpada está ligada?", lampada.esta_ligada())
lampada.desliga()
print("A lâmpada ainda está ligada?", lampada.esta_ligada())

#exer 16
n_string="1,3,4,6,10,76"
def soma(n_string):
    return sum(int(n_int)for n_int in n_string.split(','))
print(soma(n_string))

# exer 17
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
def divisaoLista(lista):
    divisao = len(lista) // 3
    lista1, lista2, lista3 = [], [], []
    for i in range(len(lista)):
        if i < divisao:
            lista1.append(lista[i])
        elif i < 2 * divisao:
            lista2.append(lista[i])
        else:
            lista3.append(lista[i])
    
    return lista1, lista2, lista3

sublista1, sublista2, sublista3 = divisaoLista(lista)
print(sublista1,sublista2,sublista3)
# exer 18
speed = {'jan':47, 'feb':52, 'march':47, 'April':44, 'May':52, 'June':53, 'july':54, 'Aug':44, 'Sept':54}
setNaoDuplicada=set([i for i in speed.values()])
print(list(setNaoDuplicada))

# exer 19
import random
random_list = random.sample(range(500), 50)
ncrescente = sorted(random_list)
n = len(ncrescente)
if n % 2 == 0:
    mediana = (ncrescente[n//2 - 1] + ncrescente[n//2]) / 2
else:
    mediana = ncrescente[n//2]


media = sum(random_list)/len(random_list)
valor_minimo = min(random_list)
valor_maximo = max(random_list)
print(f'Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}')

# exer 20
a = [1, 0, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(a[::-1])
numeros=[i for i in range(1,4)]
for i in numeros:
    if i % 2 ==0:
        print('Par:',i)
    else:
        print('Ímpar:',i)

