import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import *

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

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