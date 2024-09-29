# Resumo do desafio:
Nesta sprint foi necessário criar um arquivo dockerfile que criasse um volume para armazenar arquivos persistentes ,e ao rodar o container,carregasse os arquivos csvs para o bucket especificado através do [arquivoPython](scriptDesafio6.py).Os comandos para criar o volume do [dockerfile](./Dockerfile) foram :
```docker
docker volume create volume_dados_csv  
docker build -t img_desafio6 .
docker run -v volume_dados_csv:/app/dados_csv img_desafio6
--verifica se criou o diretorio dos arquivos no volume
docker volume inspect  volume_dados_csv
                                                                                                                                                              
```
# Explicação das perguntas escolhidas

## FILMES
1. Existe um "ponto ideal" de duração de filmes ou séries (em minutos) que maximiza a nota média? Observar padrões de duração que recebem consistentemente boas avaliações pode indicar o que o público prefere em termos de tempo.
##
2. Existe alguma correlação entre o número de artistas com uma nota alta em uma produção e a nota média da obra? Produções com "elencos de peso" têm melhor desempenho do que aquelas com apenas um grande nome?
##
3. avaliar se o filme tem maior avaliação de acordo com o gênero crescimento da participação feminina aumentou junto com a avaliação dos filmes de comedia?
##
4. qual profissão secundaria dos atores permitiu ganhar mais nota de atuação?
## SERIES 
5. Existe uma relação entre a data de nascimento de artistas e o número de votos, indicando que atores mais jovens ou mais velhos são menos reconhecidos, apesar de boas performances?
##
6. Existe um padrão de crescimento de popularidade para certos artistas ao longo do tempo, como uma "curva de ascensão" em que eles se tornam mais populares depois de certa idade ou número de obras?
##
7. Artistas que também são diretores/roteiristas tendem a receber melhores notas em filmes em que assumem múltiplos papéis?
