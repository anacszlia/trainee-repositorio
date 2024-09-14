import boto3
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

client = boto3.client(
    's3',
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name="us-east-1"
)
def hello_s3():
    """
    Use the AWS SDK for Python (Boto3) to create an Amazon Simple Storage Service
    (Amazon S3) resource and list the buckets in your account.
    This example uses the default settings specified in your shared credentials
    and config files.
    """
    s3_resource = boto3.resource("s3")
    print("Hello, Amazon S3! Let's list your buckets:")
    for bucket in s3_resource.buckets.all():
        print(f"\t{bucket.name}")


if __name__ == "__main__":
    hello_s3()

# Configurar o cliente S3
s3 = boto3.client('s3')
def carregar_query(caminho):
    with open(caminho, 'r') as arquivo:
        return arquivo.read()
# Definir a consulta SQL
query = carregar_query('./query.sql')


# Executar a consulta
resp = s3.select_object_content(
    Bucket='mybucketanacloud',
    Key='PrecoTaxaTesouroDireto.csv',
    ExpressionType='SQL',
    Expression=query,
    InputSerialization={
        'CSV': {
            "FileHeaderInfo": "USE",  
            "FieldDelimiter": ';',
        },
        'CompressionType': 'NONE' 
    },
    OutputSerialization={'CSV': {}}
)

# Processar a resposta
for event in resp['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])
        print("Stats details bytesReturned: ")
        print(statsDetails['BytesReturned'])