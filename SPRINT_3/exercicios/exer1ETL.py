coluna_filmes_vendidos = []
coluna_nomes_atores =[]
with open('actors.csv',encoding='utf-8') as file:
    header = file.readline().strip()
    for linha in file:
        campos = linha.strip().split(',')
        coluna_nomes_atores.append(campos[0])
        coluna_filmes_vendidos.append(campos[2])
indice_max = coluna_filmes_vendidos.index(max(coluna_filmes_vendidos))
nome_ator = coluna_nomes_atores[indice_max]
max_filmes = coluna_filmes_vendidos[indice_max]
with open('etapa-1.txt','w') as saida:
    print(f'O ator(a) com maior número de filmes é {nome_ator} com participação em {max_filmes} filmes',file=saida)

if file.closed:
    print("arquivo já fechado")
if saida.closed:
    print("arquivo finalizado")

