# etapa 3.1
import random
# list comprehension
lista = [random.randint(1, 1000) for _ in range(250)]

lista.reverse()

print(lista)

# etapa 3.2
animais = ["cobra", "bugio", "aranha", "elefante", "girafa", "coelho", 
           "cavalo", "hipopótamo", "raposa", "zebra", "urso", 
           "leopardo", "jacaré", "lobo", "javali", "macaco", "pinguim", 
           "golfinho", "tubarão", "vaca"]

animais.sort()
[print(animal) for animal in animais]

with open("animais.csv", "w") as arquivo:
    for animal in animais:
        arquivo.write(animal + "\n")

# etapa 3.3
import names
from datetime import datetime
random.seed(40)
qtd_nomes_unicos=3000
qtd_nomes_aleatorios=10000000
aux=[]

for i in range (0,qtd_nomes_unicos):
    aux.append(names.get_full_name())
print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios")

dados=[]
for i in range(0,qtd_nomes_aleatorios):
    dados.append(random.choice(aux))
with open("nomes_aleatorios.txt","w") as file:
    for nome in dados:
        file.write(nome + "\n")