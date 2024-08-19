coluna_NomeFilme = []
with open('actors.csv') as file:
    next(file)  
    for linha in file:
        campos = linha.strip().split(',')
        coluna_NomeFilme.append(campos[4])
frequencia_filmes = {}
for filme in coluna_NomeFilme:
    if filme in frequencia_filmes:
        frequencia_filmes[filme] += 1
    else:
        frequencia_filmes[filme] = 1
filmes_ordenados = sorted(frequencia_filmes.items(), key=lambda x: x[1], reverse=True)
with open("etapa-4.txt", "w") as saida:
    for filme,quantidade  in filmes_ordenados:
        saida.write(f"O filme {filme} aparece {quantidade} vez(es) no dataset.\n")       
if file.closed:
    print("Arquivo CSV fechado")
if saida.closed:
    print("Arquivo finalizado")
