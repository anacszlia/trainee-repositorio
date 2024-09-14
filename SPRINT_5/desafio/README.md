Neste desafio foi praticado a criação de buckets,objetos e uso da api Boto3 para a execução de consultas em sql com base em arquivos de dados governamentais.Onde fiz as queries sql com base na documentação [documentaçãoS3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-select-sql-reference-date.html#s3-select-sql-reference-to-string) e construi o código python com base na [documentaçãoBOTO3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html)
# Etapas de execução
Acessar a conta da AWS S3 ,e podendo ser necessário a instalação do boto3 no prompt de comando do sistema operacional utilizado ```pip install boto3```.Após ,faça o download dos arquivos [arquivocsv](./atividade/PrecoTaxaTesouroDireto.csv), [arquivoSQL](./atividade/query.sql) e [arquivoPython](./atividade/s3.py)
## Etapa 1
Verificar as keys de acesso únicas fornecidas na interface de login da conta,mencionadas como "credentials keys" e substituír os valores de AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_SESSION_TOKEN *Uma recomendação é deixar essas variáveis locais em um arquivo .env*
```python
client = boto3.client(
    's3',
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name="us-east-1"
)
```
## Etapa 2
Depois de efetuar o login ,é só executar a query *OBS:**Lembre de manter os arquivos na mesma pasta para que não ocorra erro de direcionamento entre o arquivo sql e o arquivo python**

1. # Explicação da consulta escolhida
```sql
SELECT
    --funções agregadas que calculam o valor máximo e mínimo das queries
    MIN(CAST(TaxaCompraManha AS DECIMAL(10, 2))) AS min_taxa_compra,
    MAX(CAST(TaxaVendaManha AS DECIMAL(10, 2))) AS max_taxa_venda
FROM s3object 
WHERE
    --condições que permitem calcular função string
    (UPPER("TipoTitulo") = 'Tesouro Selic' 
    OR TipoTitulo = 'Tesouro IPCA+ com Juros Semestrais')
    --condições que permitem calcular função de conversão,para poder usar as funções agregadas sem precisar utilizar group by
    OR (CAST(TaxaCompraManha AS DECIMAL(10, 2)) > 0
    AND CAST(TaxaVendaManha AS DECIMAL(10, 2)) > CAST(TaxaCompraManha AS DECIMAL(10, 2)))
    --função condicional,que retorna null se as duas colunas comparadas forem iguais,neste caso ,apenas o valor não nulo será retornado
    OR NULLIF(DataBase, DataVencimento) IS NOT NULL
    --função que substitua o valor de uma data em formato de string caso haja algum valor nulo na coluna DataBase e compara com a mesma string ou o momento atual,sendo uma função de data  
    AND (CAST(COALESCE(DataBase, '01-01-2005') AS STRING) != '01-01-2005' or UTCNOW())
```

2. # Explicação do conjunto de dados escolhido
Após muita procura ,encontrei um arquivo csv com dados que correspondiam com as funções exigidas na query.
Dadas as limitações do s3 em consultas sql ,tive que pré-processar os dados, como remover manualmente as vírgulas por pontos e tirar os espaçamentos dos nomes das colunas para o s3 select reconhecer como tal.

3. # Explicação do resultado da consulta
O resultado da consulta retornou -0.02,19.16 tendo como seleção as funções agregadas,pois não foi possível selecionar outras colunas junto das funções agregadas.Então,usei outras funções exigidas no desafio como critério de seleção das funções agregadas.
