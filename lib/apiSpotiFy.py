import requests
import csv
import base64
from minioBucket import MinioBucket
from minio import Minio
from minio.error import S3Error

class ApiSpotify:
    _instance = None
    _client_id = "50838a69a5fc445b86d340b4b97ef5b4"
    _client_secret = "21932daca2264477aa9bda20c037c6e2"

    # URL da API do Spotify para busca
    SPOTIFY_SEARCH_API_URL = "https://api.spotify.com/v1/search"
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiSpotify, cls).__new__(cls)
            cls._instance.access_token = cls._instance.get_access_token()
        return cls._instance

    def get_access_token(self):
        auth_str = f"{self._client_id}:{self._client_secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(self.SPOTIFY_TOKEN_URL, headers=headers, data=data)
        response_data = response.json()
        return response_data["access_token"]

    def search_track_id(self, track_name):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "q": track_name,
            "type": "track",
            "limit": 1
        }
        response = requests.get(self.SPOTIFY_SEARCH_API_URL, headers=headers, params=params)
        results = response.json()
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["id"]
        return None
    
    def get_artist(self, id):
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        SPOTIFY_API_URL = f"https://api.spotify.com/v1/artists/{id}"
        
        response = requests.get(SPOTIFY_API_URL, headers=headers)
        return response.json()

    def get_track_data(self, track_id):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        SPOTIFY_API_URL = f"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(SPOTIFY_API_URL, headers=headers)
        return response.json()

    def get_tracks_data(self, track_names):
        track_ids = [self.search_track_id(name) for name in track_names]
        return [self.get_track_data(track_id) for track_id in track_ids if track_id]
    
    def get_artist_data(self, tracks):
        
        artist_ids = set()
        artists_list = []
        for track in tracks:
            for artist in track["artists"]:
                artist_ids.add(artist["id"])
            
        for artist_id in artist_ids:
            artists_list.append(self.get_artist(artist_id)) # Chama o método get_artist
        
        return artists_list
    

    def extract_track_info(self, track_data):
        return {
            "name": track_data["name"],
            "album": track_data["album"]["name"],
            "artists": [artist["name"] for artist in track_data["artists"]],
            "release_date": track_data["album"]["release_date"]
        }
        
    def extract_artist_info(self, artist_data):
        
        return {
            "name": artist_data["name"],
            "genres": artist_data["genres"],
            "popularity": artist_data["popularity"],
            "followers": f"{artist_data["followers"]["total"]:,.0f}".replace(",", ".")

        }

    def process_tracks_data(self, tracks_data):
        return [self.extract_track_info(track_data) for track_data in tracks_data]
    
    def process_artists_data(self, artists_data):
        return [self.extract_artist_info(artist_data) for artist_data in artists_data]

    def get_music_list(self, bucket_name, object_name):
        minioBuket = MinioBucket()
        csv_content = minioBuket.get_csv_content(bucket_name, object_name)
        if csv_content is not None:
            music_list = []
            for index, row in csv_content.iterrows():
                music = row['Musica']
                music_list.append(music)
            return music_list
        else:
            return []
        
    def write_csv_tracks(self, data, filename):
        # Abrir o arquivo CSV para escrita
        with open('track.csv', mode='w', newline='', encoding='utf-8') as file:
            # Definir os nomes das colunas (headers)
            fieldnames = ['name', 'album', 'artists', 'release_date']
            
            # Criar um escritor de CSV com delimitador ';'
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            
            # Escrever o cabeçalho
            writer.writeheader()
            
            # Escrever os dados
            for row in data:
                # Garantir que a lista de 'artists' seja uma string separada por vírgulas
                row['artists'] = ', '.join(row['artists'])
                writer.writerow(row)
                
    def write_csv_artists(self, data, filename):
        # Abrir o arquivo CSV para escrita
        with open('artists.csv', mode='w', newline='', encoding='utf-8') as file:
            # Definir os nomes das colunas (headers)
            fieldnames = ['name', 'genres', 'popularity', 'followers']
            
            # Criar um escritor de CSV com delimitador ';'
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            
            # Escrever o cabeçalho
            writer.writeheader()
            
            # Escrever os dados
            for row in data:
                # Garantir que a lista de 'genres' seja uma string separada por vírgulas
                row['genres'] = ', '.join(row['genres'])
                writer.writerow(row)


if __name__ == "__main__":
    # Crie uma instância da classe ApiSpotify
    api_spotify = ApiSpotify()

    # Lista de nomes de Musicas de exemplo
    music_list = api_spotify.get_music_list("bruto", "musicas.csv")

    # Obter dados da lista de Musicas
    tracks_data = api_spotify.get_tracks_data(music_list)
    
    # Processar e extrair informações específicas dos dados das Musicas
    processed_tracks_data = api_spotify.process_tracks_data(tracks_data)
    
    # Criando CSV
    api_spotify.write_csv_tracks(processed_tracks_data, 'track.csv')
    
    minioBuket = MinioBucket()

    # Enviando para camada refinada
    
    minioBuket.upload_to_minio("refinado", "track.csv", "track.csv")
    
    # Obter dados dos artistas de Musicas
    artists_data = api_spotify.get_artist_data(tracks_data)
    
    # Processar e extrair informações específicas dos dados das Musicas
    processed_artist_data = api_spotify.process_artists_data(artists_data)
    
    # Criando CSV
    api_spotify.write_csv_artists(processed_artist_data, 'tracks.csv')
    
    minioBuket = MinioBucket()

    # Enviando para camada refinada
    minioBuket.upload_to_minio("refinado", "artists.csv", "artists.csv")