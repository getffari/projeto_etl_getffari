import requests
import base64
from minioBucket import MinioBucket

# URL da API do Spotify para busca
SPOTIFY_SEARCH_API_URL = "https://api.spotify.com/v1/search"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Função para obter o access token dinamicamente
def get_access_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()
    return response_data["access_token"]

# Função para buscar o ID de uma música pelo nome
def search_track_id(track_name, headers):
    params = {
        "q": track_name,
        "type": "track",
        "limit": 1
    }
    response = requests.get(SPOTIFY_SEARCH_API_URL, headers=headers, params=params)
    results = response.json()
    if results["tracks"]["items"]:
        return results["tracks"]["items"][0]["id"]
    return None

# Função para obter dados de uma música da API do Spotify
def get_track_data(track_id, headers):
    SPOTIFY_API_URL = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(SPOTIFY_API_URL, headers=headers)
    return response.json()

# Função para obter dados de uma lista de músicas
def get_tracks_data(track_names, headers):
    track_ids = [search_track_id(name, headers) for name in track_names]
    return [get_track_data(track_id, headers) for track_id in track_ids if track_id]

# Função para extrair dados específicos das informações da música
def extract_track_info(track_data):
    return {
        "name": track_data["name"],
        "album": track_data["album"]["name"],
        "artists": [artist["name"] for artist in track_data["artists"]],
        "release_date": track_data["album"]["release_date"]
    }

# Função para processar e extrair dados de uma lista de músicas
def process_tracks_data(tracks_data):
    return [extract_track_info(track_data) for track_data in tracks_data]

def get_music_list(bucket_name, object_name):
    minioBuket = MinioBucket()
    csv_content = minioBuket.get_csv_content(bucket_name, object_name)
    if csv_content is not None:
        music_list = []
        for index, row in csv_content.iterrows():
            music = row['Música']
            music_list.append(music)
        return music_list
    else:
        return []

if __name__ == "__main__":
    # Substitua pelos seus client_id e client_secret
    client_id = "50838a69a5fc445b86d340b4b97ef5b4"
    client_secret = "21932daca2264477aa9bda20c037c6e2"

    # Obtenha o access token dinamicamente
    access_token = get_access_token(client_id, client_secret)

    # Cabeçalhos para a requisição da API
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Lista de nomes de músicas de exemplo
    music_list = get_music_list("bruto", "musicas.csv")

    # Obter dados da lista de músicas
    tracks_data = get_tracks_data(music_list, headers)

    # Processar e extrair informações específicas dos dados das músicas
    processed_tracks_data = process_tracks_data(tracks_data)

    # Imprimir as informações extraídas
    print(processed_tracks_data)