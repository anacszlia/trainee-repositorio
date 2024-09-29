import boto3
from dotenv import load_dotenv
from datetime import datetime
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Obtenção das credenciais a partir do arquivo .env
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID') 
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')
region = "us-east-1"

# Inicializa o cliente S3 com as credenciais
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region
)

# Função para carregar arquivo
def carregar_arquivo(caminho):
    try:
        with open(caminho, 'r') as arquivo:
            return arquivo.read()
    except Exception as e:
        print(f"Erro ao carregar o arquivo {caminho}: {e}")
        return None

# Função para fazer upload de um arquivo local para o S3
def upload_file_to_s3(local_file, bucket_name, s3_path):
    try:
        s3.upload_file(local_file, bucket_name, s3_path)
        print(f"Upload bem-sucedido: {local_file} -> s3://{bucket_name}/{s3_path}")
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")

# Função para construir o caminho S3 conforme o padrão solicitado
def construir_caminho_s3(camada, origem_dado, formato_dado, especificacao_dado, arquivo):
    data_processamento = datetime.now()
    ano = data_processamento.strftime("%Y")
    mes = data_processamento.strftime("%m")
    dia = data_processamento.strftime("%d")
    
    caminho_s3 = f"{camada}/{origem_dado}/{formato_dado}/{especificacao_dado}/{ano}/{mes}/{dia}/{arquivo}"
    return caminho_s3

# Função para automatizar o upload de múltiplos arquivos
def upload_arquivos_automatico(arquivos, bucket_name, camada, origem_dado, formato_dado):
    for especificacao_dado, arquivo_local in arquivos.items():
        print(f"Processando o arquivo: {arquivo_local}")  # Adicionado para depuração
        arquivo_nome = os.path.basename(arquivo_local)  # Extrai o nome do arquivo
        caminho_s3 = construir_caminho_s3(camada, origem_dado, formato_dado, especificacao_dado, arquivo_nome)
        upload_file_to_s3(arquivo_local, bucket_name, caminho_s3)

# Nome do bucket e outros parâmetros
bucket_name = "data-lake-de-ana.sganzerla"
camada = "Raw"
origem_dado = "Local"
formato_dado = "CSV"

# Lista de arquivos locais a serem enviados para o S3
arquivos = {
    "movies": "./Filmes+e+Series/movies.csv",
    "series": "./Filmes+e+Series/series.csv",
}

# Chama a função para fazer upload automático dos arquivos
upload_arquivos_automatico(arquivos, bucket_name, camada, origem_dado, formato_dado)