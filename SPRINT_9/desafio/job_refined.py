import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df1=spark.read.parquet("s3://data-lake-de-ana.sganzerla/Trusted/Local/PARQUET/movies/2024/09/27/")
df2=spark.read.parquet("s3://data-lake-de-ana.sganzerla/Trusted/TMDB/PARQUET/movies/*/*/*/")

df_comuns = df1.join(df2, df1.id == df2.imdb_id, "inner")

# Selecionar colunas específicas para a tabela de filmes
df_filmes = df_comuns.select(
    col("imdb_id"),
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
df_filmes.write.mode("overwrite").parquet("s3://data-lake-de-ana.sganzerla/Refined/filmes")

# Selecionar colunas para gerar a tabela artistas
df_artistas = df_comuns.select(
    col("nomeArtista"),
    col("generoArtista"),
    col("idade"),
    col("profissao")
)

df_artistas.write.mode("overwrite").parquet("s3://data-lake-de-ana.sganzerla/Refined/artistas")

# Selecionar colunas para gerar a tabela votos e não ter valores de filmes duplicados nela
df_votos = df_comuns.select(
    col("imdb_id"),
    col("vote_average"),
    col("numeroVotos"),
    col("notaMedia")
).dropDuplicates()

df_votos.write.mode("overwrite").parquet("s3://data-lake-de-ana.sganzerla/Refined/votos")


job.commit()