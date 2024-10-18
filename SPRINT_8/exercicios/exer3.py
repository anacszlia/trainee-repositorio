from pyspark.sql import SparkSession
from pyspark import SparkContext ,SQLContext
from pyspark.sql.functions import *


# Etapa 3.1
spark = SparkSession.builder \
      .master("local[*]") \
      .appName("Exercicio intro") \
      .getOrCreate()

df_nomes = spark.read.text("/home/anaclaudia/nomes_aleatorios.txt")
df_nomes.show(5)
# Etapa 3.2
df_nomes = df_nomes.withColumnRenamed("value", "nomes")
df_nomes.printSchema()
df_nomes.show(10)

# Etapa 3.3
df_nomes = df_nomes.withColumn(
    'Escolaridade',
    when(floor(rand() * 3) == 0, 'Fundamental')
    .when(floor(rand() * 3) == 1, 'Medio')
    .otherwise('Superior')
)
# Etapa 3.4
df_nomes =df_nomes.withColumn(
      'Pais',
      when(floor(rand() * 13) ==0,'Venezuela')
      .when(floor(rand() * 13 )==1,'Peru')
      .when(floor(rand() * 13) ==2,'Bolivia')
      .when(floor(rand() * 13) == 3, 'Colombia')
      .when(floor(rand() * 13) == 4, 'Equador')
      .when(floor(rand() * 13) == 5, 'Chile')
      .when(floor(rand() * 13) == 6, 'Argentina')
      .when(floor(rand() * 13) == 7, 'Uruguai')
      .when(floor(rand() * 13) == 8, 'Paraguai')
      .when(floor(rand() * 13) == 9, 'Brasil')
      .when(floor(rand() * 13) == 10, 'Guiana')
      .when(floor(rand() * 13) == 11, 'Suriname')
      .otherwise('Guiana Francesa')
)
# Etapa 3.5
df_nomes = df_nomes.withColumn(
        'AnoNascimento',
        floor(rand() * (2010 - 1945 + 1) + 1945)
    )

# Etapa 3.6
df_select=df_nomes.select("nomes","AnoNascimento").where(col("AnoNascimento")>=2000).show(10)

# Etapa 3.7
df_nomes.createOrReplaceTempView('pessoas')
spark.sql('select nomes,AnoNascimento from pessoas where AnoNascimento >=2000 limit 10').show()

# Etapa 3.8
contaM = df_nomes.where((col("AnoNascimento") >= 1980) & (col("AnoNascimento") <= 1994)).select(count("*").alias('soma_milleniuns'))
contaM.show()

# Etapa 3.9
spark.sql('select count(AnoNascimento) as soma_milleniuns from pessoas where AnoNascimento between 1980 and 1994').show()

# Etapa 3.10
query = """
SELECT
    Pais,
    CASE
        WHEN AnoNascimento BETWEEN 1945 AND 1964 THEN 'Baby Boomers'
        WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
        WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials (Geração Y)'
        WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
        ELSE 'Outras'
    END AS Geracao,
    COUNT(*) AS Quantidade
FROM pessoas
GROUP BY Pais, Geracao
ORDER BY Pais, Geracao, Quantidade
"""
df_geracoes = spark.sql(query)

df_geracoes.show(52)# 4 gerações x 13 países