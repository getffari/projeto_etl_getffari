import requests
import base64

# Substitua com seu Client ID e Client Secret
# Você consegue esses dados lá no dashboard do Spotify Developer
CLIENT_ID = '#'
CLIENT_SECRET = '#'

# Autenticação (Client Credentials Flow)
auth_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
}
data = {
    "grant_type": "client_credentials"
}

# Obtendo o token de acesso
response = requests.post(auth_url, headers=headers, data=data)
access_token = response.json().get("access_token")

if access_token:
    print("Autenticado com sucesso!")
else:
    print("Erro na autenticação.")
    
# Exemplo de ID de uma música (você pode pegar um ID qualquer do Spotify)

#https://open.spotify.com/intl-pt/track/1h2xVEoJORqrg71HocgqXd?si=59f010d734794b3d
# track_id fica depois do track/ e antes do '?' na url
track_id = "1h2xVEoJORqrg71HocgqXd"  # Exemplo de ID de uma faixa do Spotify

# Usando o token para fazer uma requisição à API do Spotify
track_url = f"https://api.spotify.com/v1/tracks/{track_id}"  # Substitua {track_id} com o ID de uma faixa específica
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Exemplo de ID de uma música (você pode pegar um ID qualquer do Spotify)
response = requests.get(track_url.format(track_id=track_id), headers=headers)

if response.status_code == 200:
    track_data = response.json()
    print("Título:", track_data['name'])
    print("Artista:", track_data['artists'][0]['name'])
    print("Álbum:", track_data['album']['name'])
else:
    print(f"Erro na requisição: {response.status_code}")
    