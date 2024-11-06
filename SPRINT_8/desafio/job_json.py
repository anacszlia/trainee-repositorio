#import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F 

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df = spark.read.json("s3://data-lake-de-ana.sganzerla/Raw/TMDB/JSON/movies/*/*/*/*.json",multiLine=True)
trusted_path = "s3://data-lake-de-ana.sganzerla/Trusted/TMDB/PARQUET/movies/"

df = df.withColumn("file_path", F.input_file_name())

df = df.withColumn("ano", F.regexp_extract(F.col("file_path"), r"/(\d{4})/", 1)) \
       .withColumn("mês", F.regexp_extract(F.col("file_path"), r"/\d{4}/(\d{2})/", 1)) \
       .withColumn("dia", F.regexp_extract(F.col("file_path"), r"/\d{4}/\d{2}/(\d{2})/", 1))

df = df.dropDuplicates(["id", "title"])

df = df.coalesce(1)

df.write.mode("overwrite") \
   .partitionBy("ano", "mês", "dia") \
   .parquet(trusted_path)

job.commit()