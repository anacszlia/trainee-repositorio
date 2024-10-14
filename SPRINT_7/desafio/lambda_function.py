import requests
import json
from datetime import datetime
import boto3
import os
import random

BASE_URL = 'https://api.themoviedb.org/3'
READ_TOKEN = os.getenv('READ_TOKEN')
S3_BUCKET_NAME = 'data-lake-de-ana.sganzerla'

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
    
    random.shuffle(all_movies)

    filtered_movies = []
    for movie in all_movies:
        movie_details = busca_movie_details(movie['id'])
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

def busca_movie_details(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def caminho_s3(camada, origem_dado, formato_dado, especificacao_dado, arquivo):
    data = datetime.now().strftime("%Y/%m/%d")
    return f"{camada}/{origem_dado}/{formato_dado}/{especificacao_dado}/{data}/{arquivo}"

def upload_para_s3(arquivo_local, bucket, caminho_s3):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(arquivo_local, bucket, caminho_s3)
        print(f"Upload realizado: {arquivo_local} -> s3://{bucket}/{caminho_s3}")
    except Exception as e:
        print(f"Erro no upload: {e}")

def lambda_handler(event, context):
    genre_id = 35
    genre_name = 'Comédia'
    movies_filtered = filtered_movies(genre_id, genre_name)
    local_json_path = '/tmp/movies_filtered.json'
    with open(local_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(movies_filtered, json_file, ensure_ascii=False, indent=4)

    camada = "Raw"
    origem_dado = "TMDB"
    formato_dado = "JSON"
    timestamp = datetime.now().strftime("%H%M%S")
    arquivo_nome = f"movies_filtered_{timestamp}.json"
    caminho = caminho_s3(camada, origem_dado, formato_dado, 'movies', arquivo_nome)
    upload_para_s3(local_json_path, S3_BUCKET_NAME, caminho)
    
    return {
        'statusCode': 200,
        'body': f"Upload para {S3_BUCKET_NAME}/{caminho} concluído."
    }