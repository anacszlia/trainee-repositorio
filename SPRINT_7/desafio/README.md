# Desafio
Nesta sprint foi necessário desenvolver um código python no serviço lambda da AWS que fizesse requisições na api TMDB e devolvesse um arquivo em formato json de todos os dados filtrados de meu interesse .

## Etapas de execução :
1. Desenvolvi este [arquivoTeste](testes.py) para visualizar melhor os detalhes dos filmes e me permitir usar o id da api imdb com a tmdb .
Exemplo:
![img_teste](/SPRINT_7/evidencias/local.png)

2. Depois de desenvolver esse arquivo ,fiz outro [gravarDadosLocais.py](gravardadosLocais.py) que me retornasse os valores desejados localmente e enviasse o arquivo json para o serviço S3 da AWS.
Um exemplo de retorno é :
![img_teste](/SPRINT_7/evidencias/exerrSp7.png)

3. Ao mudar a o código para o lambda ,não houve necessidade de importar as credenciais de acesso da aws,então ,com a função padrão **lambda_handler(event,context)** ,o código ficou menos extenso e de melhor compreensão. Veja aqui: [lambda_function](lambda_function.py)

4. Com o código pronto para rodar no lambda,faltava criar uma role para usuário IAM que permitisse fazer upload para o s3 .Veja como foi configurado o caminho para o bucket ._Obs_:O asterisco indica que pode ser qualquer arquivo a partir dele:
![img_teste](/SPRINT_7/evidencias/role.png)

5. Para usar as bibliotecas necessárias,precisei criar uma camada que instalasse requests e tmdbv3 .Abaixo estão os comandos que utilizei no wsl ubuntu:
exemplo estrutura de arquivos da biblioteca Requests
layer_content.zip
└ python
    └ lib
        └ python3.11
            └ site-packages
                └ requests
                └ <other_dependencies> (i.e. dependencies of the requests package)
                └ ...
```shell
mkdir layer
cd layer
mkdir python
cd python
# instalar na mesma versão python que está a lambda e criar um ambiente virtual para executar os comandos pip
python3.8 -m venv envi
# ativar o ambiente virtual
source envi/bin/activate    
pip install requests urllib3==1.26.15
pip install tmdbv3api
# sair do ambiente virtual
deactivate

```
Após,mover o conteúdo armazenado em envi para uma pasta chamada **python** e compactar em formato de zip e executar o código normalmente.

# Questões formuladas 
Essas questões complementam meu desafio final ,trazendo novos dados que buscam mais detalhes nas minhas perguntas anteriormente formuladas.
## FILMES
1. Existe um "ponto ideal" de duração de filmes ou séries (em minutos) que maximiza a nota média? Observar padrões de duração que recebem consistentemente boas avaliações pode indicar o que o público prefere em termos de tempo,o que foi que contribuiu para que o filme alcançasse maior lucro ?(Considerar filmes que obtiveram lucros maiores que a média revenue)
##
2. Existe alguma correlação entre o número de artistas com uma nota alta em uma produção e a nota média da obra? Produções com "elencos de peso" têm melhor desempenho do que aquelas com apenas um grande nome?
## Sobre genêro dos artistas
3. avaliar se o filme tem maior avaliação de acordo com o gênero crescimento da participação feminina aumentou junto com a avaliação dos filmes de comedia,avaliar a popularidade e as produtoras de filmes mais "inclusivas " que tem maior público feminino como artista principal e o país de origem das produtoras.
##
4. qual profissão secundaria dos atores permitiu ganhar mais nota de atuação e em qual país de origem

5. Existe uma relação entre a data de nascimento de artistas e o número de votos, indicando que atores mais jovens ou mais velhos são menos reconhecidos, apesar da boa performance.
##
6. Existe um padrão de crescimento de popularidade para certos artistas ao longo do tempo, como uma "curva de ascensão" em que eles se tornam mais populares depois de certa idade ou número de obras?
##
7. Artistas que também são diretores/roteiristas tendem a receber melhores notas em filmes em que assumem múltiplos papéis?