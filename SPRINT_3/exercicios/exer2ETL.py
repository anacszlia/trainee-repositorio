dados = []

with open('actors.csv', encoding='utf-8') as file:
    header = file.readline().strip() 
    for linha in file:
        campos = linha.strip().split(',')
        row = {}
        row['actor'] = campos[0]
        row['best_movie'] = campos[4]
        row['gross'] = float(campos[5]) if campos[5].replace('.', '', 1).isdigit() else 0.0
        dados.append(row)

resultado = {}

for linha in dados:
     filme = linha['best_movie']
     gross = linha['gross']
     if filme in resultado:
        resultado[filme]['soma'] += gross
        resultado[filme]['contagem'] += 1
     else:
        resultado[filme] = {'soma': gross, 'contagem': 1}
total_gross = sum(linha['gross'] for linha in dados)
total_filmes = len(dados)
media = total_gross / total_filmes

with open('etapa-2.txt', 'w', encoding='utf-8') as saida:
    print(f'Média Bruta por Filme: {media:.2f}', file=saida)

# Verifica se os arquivos foram fechados
if file.closed:
    print("Arquivo 'actors.csv' já fechado")
#if saida.closed:
#    print("Arquivo 'etapa-2.txt' finalizado")