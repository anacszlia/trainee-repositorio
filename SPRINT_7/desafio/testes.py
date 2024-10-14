import requests
import os 
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('api_key')
READ_TOKEN = os.getenv('READ_TOKEN')

movie_id="tt0000009"

url = f"https://api.themoviedb.org/3/movie/{movie_id}/external_ids"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {READ_TOKEN}"
}
response = requests.get(url, headers=headers)
print("\n")
print(response.text)
print("\n") 

movie_id = 356151

url = f'https://api.themoviedb.org/3/movie/{movie_id}'

# Parâmetros para a requisição
params = {
    'api_key': api_key,
    'language': 'pt-BR' 
}
response = requests.get(url, params=params)
if response.status_code == 200:
    movie_data = response.json()
    print(movie_data)
else:
    print(f'Erro na requisição: {response.status_code}')

print("\n")