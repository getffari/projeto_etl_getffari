import requests
import csv
import base64
import ast
from minioBucket import MinioBucket

from until import *

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

    def get_tracks_data(self, track_ids):
        tracks_data = []
        for track_id in track_ids:
            tracks_data.append(self.get_track_data(track_id))
            
        return tracks_data
    
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
            "trackId": track_data["id"],
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

    def get_track_id_list(self):
        minioBuket = MinioBucket()
        csv_content = minioBuket.get_csv_content("refinado", "musicas/musicas.csv")
        if csv_content is not None:
            track_id_list = []
            for index, row in csv_content.iterrows():
                trackId = row['trackId']
                track_id_list.append(trackId)
            return track_id_list
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

    def normatize_track_data(sefl):
        minioBuket = MinioBucket()
        csv_content = minioBuket.get_csv_content("bruto", "trackData/trackData.csv")
        if csv_content is not None:
            tracks_data = []
            artists_by_track_data_id = []
            for index, row in csv_content.iterrows():
                new_track_data = {
                    "trackId": row["trackId"],
                    "name": row["name"],
                    "album": row["album"],
                    "release_date": row["release_date"]
                }
                tracks_data.append(new_track_data)
                artists = ast.literal_eval(row["artists"])
                for artist in artists:
                    artists_by_track_data_id_line = {
                        "trackId": row["trackId"],
                        "artist": artist
                    }
                    artists_by_track_data_id.append(artists_by_track_data_id_line)

            write_csv(tracks_data, "refinado/trackData.csv", ["trackId", "name", "album", "release_date"])
            minioBuket.upload_to_minio("refinado", "trackData", "trackData.csv", "refinado/trackData.csv")
            write_csv(artists_by_track_data_id, "refinado/artistByTrackId.csv", ["trackId", "artist"])
            minioBuket.upload_to_minio("refinado", "artistByTrackId", "artistByTrackId.csv", "refinado/artistByTrackId.csv")

    def normatize_artists_data(sefl):
        minioBuket = MinioBucket()
        csv_content = minioBuket.get_csv_content("bruto", "artistsData/artistsData.csv")
        if csv_content is not None:
            artists_data = []
            genres_by_artist = []
            for index, row in csv_content.iterrows():
                new_artists_data = {
                    "name": row["name"],
                    "popularity": row["popularity"],
                    "followers": row["followers"],
                }
                artists_data.append(new_artists_data)
                genres = ast.literal_eval(row["genres"])
                for genre in genres:
                    genre_by_artist_line = {
                        "artistName": row["name"],
                        "genre": genre
                    }
                    genres_by_artist.append(genre_by_artist_line)

            write_csv(artists_data, "refinado/artistsData.csv", ["name", "popularity", "followers"])
            minioBuket.upload_to_minio("refinado", "artistsData", "artistsData.csv", "refinado/artistsData.csv")

            write_csv(genres_by_artist, "refinado/genresByArtist.csv", ["artistName", "genre"])
            minioBuket.upload_to_minio("refinado", "genresByArtist", "genresByArtist.csv", "refinado/genresByArtist.csv")


if __name__ == "__main__":
    # Crie uma instância da classe ApiSpotify
    api_spotify = ApiSpotify()
    minioBuket = MinioBucket()

    # Lista de nomes de Musicas de exemplo
    track_id_list = api_spotify.get_track_id_list()

    # Obter dados da lista de Musicas
    tracks_data = api_spotify.get_tracks_data(track_id_list)
    
    # Processar e extrair informações específicas dos dados das Musicas
    processed_tracks_data = api_spotify.process_tracks_data(tracks_data)
    
    # Criando CSV
    write_csv(processed_tracks_data, 'bruto/trackData.csv', ["trackId", "name", "album", "artists", "release_date"])
    
    # Enviando para camada refinada
    minioBuket.upload_to_minio("bruto", "trackData", "trackData.csv", "bruto/trackData.csv")
    
    # Obter dados dos artistas de Musicas
    artists_data = api_spotify.get_artist_data(tracks_data)
    
    # Processar e extrair informações específicas dos dados das Musicas
    processed_artist_data = api_spotify.process_artists_data(artists_data)
    
    # Criando CSV
    write_csv(processed_artist_data, "bruto/artistsData.csv", ['name', 'genres', 'popularity', 'followers'])
    
    # Enviando para camada refinada
    minioBuket.upload_to_minio("bruto", "artistsData", "artistsData.csv", "bruto/artistsData.csv")

    api_spotify.normatize_track_data()

    api_spotify.normatize_artists_data()