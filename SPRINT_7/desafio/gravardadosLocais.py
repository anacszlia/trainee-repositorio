import requests
import os 
from dotenv import load_dotenv
import json
from datetime import datetime
import random
import boto3

load_dotenv()

apikey = os.getenv("api_key")
S3_BUCKET_NAME = 'data-lake-de-ana.sganzerla'
READ_TOKEN = os.getenv('READ_TOKEN')

BASE_URL = 'https://api.themoviedb.org/3'
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {READ_TOKEN}"
}

def filtered_movies(genre_id, genre_name, max_movies=100):
    all_movies = []
    total_pages = 50
    
    for page in range(1, total_pages + 1):
        url = f'{BASE_URL}/discover/movie'
        params = {
            'language': 'en-US',
            'with_genres': genre_id,
            'primary_release_date.gte': '1894-01-01',
            'primary_release_date.lte': datetime.now().strftime('%Y-%m-%d'),
            'page': page,
            'sort_by': 'popularity.desc'  
        }

        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            movies = response.json().get('results', [])
            all_movies.extend(movies) 
        else:
            print(f'Erro na requisição: {response.status_code}')
    
    # Embaralhar a lista de filmes
    random.shuffle(all_movies)

    filtered_movies = []
    for movie in all_movies:
        movie_details = fetch_movie_details(movie['id'])
        if movie_details:
            movie.update(movie_details)
            filtered_movie_data = {
                'title': movie.get('title', ''),
                'imdb_id': movie.get('imdb_id', ''),
                'id': movie.get('id', ''),
                'original_language': movie.get('original_language', ''),
                'revenue': movie.get('revenue', 0),
                'release_date': movie.get('release_date', ''),
                'popularity': movie.get('popularity', 0),
                'genres': [genre['name'] for genre in movie.get('genres', [])],
                'production_companies': [company['name'] for company in movie.get('production_companies', [])],
                'origin_country': movie.get('origin_country', []),
                'vote_average': movie.get('vote_average', 0)
            }
            filtered_movies.append(filtered_movie_data)

        if len(filtered_movies) >= max_movies: 
            break

    return filtered_movies

def fetch_movie_details(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

movies_filtered = filtered_movies(35, 'Comédia')

# Abrir o arquivo e salvar os dados no formato JSON
with open('movies_filtered.json', 'w', encoding='utf-8') as json_file:
    json.dump(movies_filtered, json_file, ensure_ascii=False, indent=4)

print("Arquivo JSON salvo com sucesso!")


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


# Função para gerar o caminho S3 com data
def caminho_s3(camada, origem_dado, formato_dado, especificacao_dado, arquivo):
    data = datetime.now().strftime("%Y/%m/%d")
    return f"{camada}/{origem_dado}/{formato_dado}/{especificacao_dado}/{data}/{arquivo}"

# Função para fazer upload de um arquivo para o S3
def upload_para_s3(arquivo_local, bucket, caminho_s3):
    try:
        s3.upload_file(arquivo_local, bucket, caminho_s3)
        print(f"Upload realizado: {arquivo_local} -> s3://{bucket}/{caminho_s3}")
    except Exception as e:
        print(f"Erro no upload: {e}")

# Função Lambda principal ou execução local
def lambda_handler(event=None, context=None):
    bucket = "data-lake-de-ana.sganzerla"
    camada = "Raw"
    origem_dado = "TMDB"
    formato_dado = "JSON"
    
    arquivo_local = f'/{movies_filtered}' 
    arquivo_nome = os.path.basename(arquivo_local)  # Nome do arquivo
    
    # Gerar caminho S3 e fazer o upload
    caminho = caminho_s3(camada, origem_dado, formato_dado, 'movies', arquivo_nome)
    upload_para_s3(arquivo_local, bucket, caminho)
    
    return {
        'statusCode': 200,
        'body': f"Upload para {bucket}/{caminho} concluído."
    }

# Executar localmente
if __name__ == "__main__":
    lambda_handler()
