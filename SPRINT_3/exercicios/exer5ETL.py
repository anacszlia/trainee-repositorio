coluna_NomeAtor = []
coluna_totalGross = []

with open('actors.csv') as file:
    next(file) 
    for linha in file:
        linha = linha.strip()
        if linha.startswith('"'):
            fim_nome = linha.find('",')
            nome_ator = linha[1:fim_nome]
            valores = linha[fim_nome+2:].split()  
        else:
            campos = linha.split(',')
            nome_ator = campos[0].strip()
            valores = campos[1:] 
        
        total_gross = 0.0
        for valor in valores:
            try:
                total_gross += float(valor.replace(',', '').strip())
            except ValueError:
                pass  

        coluna_NomeAtor.append(nome_ator)
        coluna_totalGross.append(total_gross)
pares_ator_gross = list(zip(coluna_NomeAtor, coluna_totalGross))
pares_ordenados = sorted(pares_ator_gross, key=lambda x: x[1], reverse=True)
with open("etapa-5.txt", "w") as saida:
    for ator, totalgross in pares_ordenados:
        saida.write(f"{ator} {totalgross:.2f}.\n")

print("Arquivo 'etapa-5.txt' criado com sucesso.")
