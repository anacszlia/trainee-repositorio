# Desafio
Este desafio envolveu a transferência de dados da camada Trusted para a camada Refined.Com o objetivo de criar tabelas com dados especificos de cada .

## filtrando mais dados necessários :
Nos testes locais realizados no Google colab ,seguindo as dicas do monitor ,primeiramente,precisei voltar para uma etapa anterior do desafio,pois constatei erros nos meus dados transformados do arquivo csv para parquet que me impediam de alcançar convergências dos dados entre os arquivos da pasta local e da pasta tmdb.
Além disso,optei por deixar colunas como id e tituloPrincipal como forma de corresponder os dados complementares com os da api tmdb.
```py
#dados oriundos de pastas criadas no colab
input_path = "/movies.csv"

output_path = "/data-lake-de-ana.sganzerla/Trusted/Local/PARQUET/movies/"

schema = StructType([
    StructField("id", StringType(), True),
    StructField("tituloPincipal", StringType(), True),  # será apagado
    StructField("tituloOriginal", StringType(), True),  # será apagado
    StructField("anoLancamento", IntegerType(), True),
    StructField("tempoMinutos", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notaMedia", FloatType(), True),
    StructField("numeroVotos", IntegerType(), True),
    StructField("generoArtista", StringType(), True),
    StructField("personagem", StringType(), True),  # será apagado
    StructField("nomeArtista", StringType(), True),
    StructField("anoNascimento", IntegerType(), True), # será apagado
    StructField("anoFalecimento", IntegerType(), True), # será apagado
    StructField("profissao", StringType(), True),
    StructField("titulosMaisConhecidos", StringType(), True)  # será apagada

])
df=spark.read.format("csv").option("header", "true").option("delimiter", "|").schema(schema).load(input_path)
# eliminei dados nulos dessa coluna em específico,pois o resultado calculado na etapa seguinte seria inválidp
df = df.na.drop(subset=['anoNascimento'])

# substitui os valores nulos para 2024 para ,assim,poder trabalhar com dados de atores vivos também
df = df.fillna({'anoFalecimento': 2024})
# criei uma nova coluna idade que reduz o número de consultas da etapa final do desafio

df = df.withColumn("idade", F.col("anoFalecimento") - F.col("anoNascimento"))

# O restante do código já fazia parte do projeto
df = df.na.drop()

df=df.filter(F.col("genero") == "Comedy")
df=df.drop("titulosMaisConhecidos","tituloOriginal","personagem","anoNascimento","anoFalecimento")
total_linhas = df.count()
print("Total de linhas: ", total_linhas) # total de 63.603

df.write.mode("overwrite").parquet(output_path)
```

## Mapa da modelagem dos dados
Utilizei a mesma ferramenta de modelagem da sprint 2 ,o: [https://app.sqldbm.com/](https://app.sqldbm.com/) ,site que permite de maneira simples ,criar modelos não tão complexos mas que auxiliam na visualização.
_Obs_:Tentei especificar como chaves primárias as colunas que correspondem a valores únicos ,como __nomeArtista__ e __imdb_id__ ligadas com a tabela __fatos_filmes__ que unem todas elas .Por motivos de bug,a coluna __imdb_id__ não reconheceu como chave estrangeira na tabela fatos_filmes.
![img](./)

## Teste local do desafio:
Após filtrar de maneira correta os dados e elaborar o modelo que irá apontar como será construída a última camada do data-lake,criei tabelas com base na modelagem.

```py
# Criei dois dataframes no qual o d1 se refere a dados de origem local e o d2 a dados da origem tmdb
df1=spark.read.parquet("/data-lake-de-ana.sganzerla/Trusted/Local/PARQUET/movies/")
df2=spark.read.parquet("/home/tmdb/")

df1.printSchema()
df2.printSchema()

# cria um novo dataframe que prioriza a precedência das colunas do dataframe d1 e une os dados que possuem intersecção de ids 
df_comuns = df1.join(df2, df1.id == df2.imdb_id, "inner")


# Exibir os dados comuns
df_comuns.show(50)

# Selecionar colunas específicas para a tabela de filmes
df_filmes = df_comuns.select(
    col("imdb_id").cast("string"),
    col("title"),
    col("origin_country"),
    col("original_language"),
    col("popularity"),
    col("production_companies"),
    col("revenue"),
    col("tempoMinutos"),
    col("genres"),
    col("nomeArtista"),
    col("anoLancamento")

)
# cria uma tabela ou sobrepõe se já existe
df_filmes.write.mode("overwrite").saveAsTable("filmes")
# método sql que seleciona todas as colunas da tabela 
spark.sql("SELECT * FROM filmes").show(4)

df_filmes.write.mode("overwrite").parquet("/data-lake-de-ana.sganzerla/Refined/filmes")


# Selecionar colunas para gerar a tabela artistas
df_artistas = df_comuns.select(
    col("nomeArtista"),
    col("generoArtista"),
    col("idade"),
    col("profissao")
)
df_artistas.write.mode("overwrite").saveAsTable("artistas")
spark.sql("SELECT * FROM artistas").show(4)

df_artistas.write.mode("overwrite").parquet("/data-lake-de-ana.sganzerla/Refined/artistas")

# Selecionar colunas para gerar a tabela votos
df_votos = df_comuns.select(
    col("imdb_id"),
    col("vote_average"),
    col("numeroVotos"),
    col("notaMedia")
).dropDuplicates()
df_votos.write.mode("overwrite").saveAsTable("votos")
spark.sql("SELECT * FROM votos").show(4)

df_votos.write.mode("overwrite").parquet("/data-lake-de-ana.sganzerla/Refined/votos")

```

## Script job Glue
Após o script rodar com sucesso,importei o código para o job_refined do Glue ,mantendo a mesma estrutura ,apenas alterando os caminhos de escrita das tabelas e deletanto as linhas de `printSchema() e .show()`.Veja aqui: [job_refined](job_refined.py).


## Prosseguimento das perguntas a serem feitas 
Nesta sprint em específica,resumi melhor as perguntas a serem feitas de forma mais simples e direta para serem respondidas.

## FILMES -Lucro
1. Existe um "ponto ideal" de duração de filmes ou séries (em minutos) que maximiza a nota média? Observar padrões de duração que recebem consistentemente boas avaliações pode indicar o que o público prefere em termos de tempo,o que foi que contribuiu para que o filme alcançasse maior lucro ?(Considerar filmes que obtiveram lucros maiores que a média revenue)
## Sobre genêro dos artistas
2. Avaliar se o filme tem maior avaliação de acordo com o gênero .O crescimento da participação feminina aumentou junto com a avaliação dos filmes de comédia ? Se sim,avaliar as produtoras de filmes mais "inclusivas " que tem maior público feminino como artista principal e o país de origem,como também o idioma falado.
## Profissões 
3. Qual profissão secundária dos atores permitiu ganhar mais nota de atuação.Artistas que são além de atores fazem o filme ganhar mais votos?
## Idade
4. Existe uma relação entre a data de nascimento de artistas e o número de votos do filme, indicando que atores mais jovens ou mais velhos são menos reconhecidos, apesar da boa performance,ou se existe uma "curva de ascensão" em que eles se tornam mais populares depois de certa idade.