# Descrição do Desafio
Nesta sprint o que era pra ser feito era a limpeza dos dados,com o objetivo de elevar da camada Raw para a camada Trusted, onde os dados são estruturados, validados e enriquecidos no formato parquet.
 O processamento nesta camada inclui a limpeza dos dados, remoção de registros duplicados, validação de
 informações e enriquecimento com metadados ou dados adicionais,sendo armazenados em formatos otimizados como Parquet que melhora a eficiência e o desempenho das consultas.Essas informações foram retiradas do ótimo artigo que o monitor dessa sprint sugeriu em [https://diegoitacolomy.medium.com/as-camadas-de-um-datalake-e-sua-import%C3%A2ncia-7315b42cc230](https://diegoitacolomy.medium.com/as-camadas-de-um-datalake-e-sua-import%C3%A2ncia-7315b42cc230).

## Etapa 1
### Planejamento dos dados que foram filtrados
Efetuei ,primeiramente testes locais por meio do terminal do wsl ubuntu e de arquivos notebooks no Gloogle Colab.
1. `CSV` :
Utilizei métodos como _printSchema()_ para visualizar os tipos de dados presentes nas colunas .Por padrão arquivos Csv só tem colunas do tipo string ,por isso alterei para que certos campos tivessem os valores corretos antes de escrever os arquivos no formato parquet.
Além disso,filtrei genêros atribuídos a Comédia,pois só com este gênero que utilizarei ,e eliminei todas as linhas que contivessem pelo menos um valor nulo,pois trabalharei com perguntas mais genéricas sobre tudo.
Abaixo está o mesmo código que foi utilizado no [job_csv](job_csv.py).
```py

input_path = "s3://data-lake-de-ana.sganzerla/Raw/Local/CSV/movies/2024/09/27/movies.csv"

output_path = "s3://data-lake-de-ana.sganzerla/Trusted/Local/PARQUET/movies/2024/09/27/"

schema = StructType([
    StructField("id", StringType(), True),
    StructField("tituloPincipal", StringType(), True),
    StructField("tituloOriginal", StringType(), True),  # será apagado
    StructField("anoLancamento", IntegerType(), True),
    StructField("tempoMinutos", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notaMedia", FloatType(), True),
    StructField("numeroVotos", IntegerType(), True),
    StructField("generoArtista", StringType(), True),
    StructField("personagem", StringType(), True),
    StructField("nomeArtista", StringType(), True),
    StructField("anoNascimento", IntegerType(), True),
    StructField("anoFalecimento", IntegerType(), True),
    StructField("profissao", StringType(), True),
    StructField("titulosMaisConhecidos", StringType(), True)  # será apagada

])
df=spark.read.format("csv").option("header", "true").option("delimiter", "|").schema(schema).load(input_path)


df = df.na.drop()

df=df.filter(F.col("genero") == "Comedy")

df=df.drop("titulosMaisConhecidos","tituloOriginal")

df.write.mode("overwrite").parquet(output_path)

job.commit()


```

2. `JSON` :
Para fazer o tratamento dos dados no formato json foi um processo um pouco mais simples,pois por padrão os tipos de dados já são definidos corretamente,assim,não sendo necessário definir a estrutura manualmente dos campos das colunas.Dessa forma,as colunas e os dados já estavam prontos do jeito que iria utilizar ,então só implementei uma forma de ler todos os arquivos em um único dataframe e eliminar os que se repetiam de acordo com o id e o título do filme.

Támbem era necessário fazer partição pela data de ingestão periódica dos arquivos.Por não possuir essas colunas ,procurei no suporte da Aws e vi uma maneira de fazer isso : [https://repost.aws/questions/QU63IoegHFQrCllAtjNeetEg/aws-glue-json-to-parquet-keep-json-partitioning](https://repost.aws/questions/QU63IoegHFQrCllAtjNeetEg/aws-glue-json-to-parquet-keep-json-partitioning)

O código completo está no script [job_json](job_json.py)
```py
# pegar todos os arquivos presentes no diretório raw/tmdb
df = spark.read.json("s3://data-lake-de-ana.sganzerla/Raw/TMDB/JSON/movies/*/*/*/*.json",multiLine=True)
trusted_path = "s3://data-lake-de-ana.sganzerla/Trusted/TMDB/PARQUET/movies/"

# Adicionar uma coluna com o caminho do arquivo de origem para pegar o diretório 
df = df.withColumn("file_path", F.input_file_name())

df = df.withColumn("ano", F.regexp_extract(F.col("file_path"), r"/(\d{4})/", 1)) \
       .withColumn("mês", F.regexp_extract(F.col("file_path"), r"/\d{4}/(\d{2})/", 1)) \
       .withColumn("dia", F.regexp_extract(F.col("file_path"), r"/\d{4}/\d{2}/(\d{2})/", 1))

df = df.dropDuplicates(["id", "title"])

# 1 arquivo por partição ,pois os arquivos parquet ficavam muito menores ,o que não era o necessário
df = df.coalesce(1)

df.write.mode("overwrite") \
   .partitionBy("ano", "mês", "dia") \
   .parquet(trusted_path)
   

job.commit()


```

