coluna_average = []
coluna_nomes_atores =[]
with open('actors.csv',encoding='utf-8') as file:
    next(file)
    for linha in file:
        campos = linha.strip().split(',')
        coluna_nomes_atores.append(campos[0])
        coluna_average.append(campos[3])
indice_max = coluna_average.index(max(coluna_average))
nome_ator = coluna_nomes_atores[indice_max]
max_filmes = coluna_average[indice_max]
with open('etapa-3.txt','w') as saida:
    print(f'O ator(a) com maior média de filmes é {nome_ator} com média de {max_filmes} filmes',file=saida)

if file.closed:
    print("arquivo já fechado")
if saida.closed:
    print("arquivo finalizado")