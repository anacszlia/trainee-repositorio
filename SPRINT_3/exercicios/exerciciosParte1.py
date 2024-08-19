#exer 1
nome = "ana"
idade = 20
ano_atual = 2024
ano_cem_anos = ano_atual + (100 - idade)
print(ano_cem_anos)

#exer 2
numeros=[i for i in range(1,4)]
for i in numeros:
    if i % 2 ==0:
        print('Par:',i)
    else:
        print('Ímpar:',i)

#exer 3
for num in range(0, 21, 2):
    print(num)
#exer 4 
def primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

for num in range(1, 101):
    if primo(num):
        print(num)
#exer 5
dia =22
mes =10
ano=2022
print(f'{dia}/{mes}/{ano}')
# exer 21
class Passaro:
    def __init__(self, raca):
        self.raca = raca
    
    def voando(self):
        print(f"{self.raca}\nvoando...")

    def emitir(self):
        print(f'{self.raca}\nemitindo som...')

class Pato(Passaro):
    def emitir(self):
        super().emitir()
        print("Quack Quack")

class Pardal(Passaro):
    def emitir(self):
        super().emitir()
        print("Piu Piu")
pato = Pato("Pato")
pato.voando() 
pato.emitir() 
pardal=Pardal("Pardal")
pardal.voando()
pardal.emitir()

#exer 22 
class Pessoa:
    def __init__(self,id):
        self.__nome=None
        self.id=id
    #usando o metodo getter
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome
pessoa = Pessoa(0)
pessoa.nome = 'Fulano De Tal'  # Usando o setter para definir o nome
print(pessoa.nome)             # Usando o getter para acessar o nome

#exer 23
class Calculo:
   def __init__(self,x,y):
      self.x=x
      self.y=y
   def soma(self):
      return self.x + self.y
   def substracao(self):
      return self.x - self.y
operacao=Calculo(3,4)
print(operacao.soma())
print(operacao.substracao())

#exer 24
class Ordenadora:
    def __init__(self,listaBaguncada):
        self.listaBaguncada=listaBaguncada
    def ordenacaoCrescente(self):
        return sorted(self.listaBaguncada)
    def ordenacaoDecrescente(self):
        return sorted(self.listaBaguncada,reverse=True)
    #instanciar objetos
crescente = Ordenadora([3, 4, 2, 1, 5])
decrescente = Ordenadora([9, 7, 6, 8])
print(crescente.ordenacaoCrescente())
print(decrescente.ordenacaoDecrescente())

#exer 25
class Aviao:
    cor_padrao = "Azul"
    def __init__(self,modelo,velocidade_maxima,capacidade):
        self.modelo=modelo
        self.velocidade_maxima=velocidade_maxima
        self.cor=Aviao.cor_padrao
        self.capacidade=capacidade
boing = Aviao("BOEING456", 1500, 400)
praetor = Aviao("Embraer Praetor 600", 863, 14)
antonov = Aviao("Antonov An-2", 258, 12)
lista=[boing,praetor,antonov]
for i in lista :
    print(f"O modelo {i.modelo} atinge uma velocidade máxima de {i.velocidade_maxima} km/h capacidade para {i.capacidade} passageiros.Cor: {i.cor}.")
print(sublista1,sublista2,sublista3)
x = ('apple', 'banana', 'cherry')
y = enumerate(x)