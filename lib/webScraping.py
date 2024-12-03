import re
from bs4 import BeautifulSoup
import requests
import csv
from minio import Minio
from minio.error import S3Error

from apiSpotiFy import ApiSpotify
from minioBucket import MinioBucket

URL = "https://maistocadas.mus.br/musicas-mais-tocadas/"
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

def fetch_page(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    li_items = soup.find_all('li')
    return [li.get_text(strip=True) for li in li_items]

def extract_data(text):
    parts = re.split(r" – |-", text)
    if len(parts) == 3:
        return {'musica': parts[0], 'artista': parts[1], 'gravadora': parts[2]}
    elif len(parts) > 3:
        return {'musica': f"{parts[0]}-{parts[1]}", 'artista': parts[2], 'gravadora': parts[3]}
    return None

def write_csv(data, filename, fieldNames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = fieldNames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def music_list_with_track_id():
    minioBuket = MinioBucket()
    api_spotify = ApiSpotify()
    csv_content = minioBuket.get_csv_content("bruto", "musicas/musicas.csv")
    if csv_content is not None:
        music_list = []
        for index, row in csv_content.iterrows():
            track_id = api_spotify.search_track_id(row['musica'])
            music = {
                    "trackId": track_id,
                    "musica": row['musica'],
                    "artista": row["artista"],
                    "gravadora": row["gravadora"]
                     }
            music_list.append(music)
        return music_list
    else:
        return []

def main():
    html = fetch_page(URL, HEADERS)
    texts = parse_html(html)
    data = [extract_data(text) for text in texts if extract_data(text) is not None]
    write_csv(data, 'bruto/musicas.csv', ['musica', 'artista', 'gravadora'])
    minioBuket = MinioBucket()
    minioBuket.upload_to_minio("bruto", "musicas", "musicas.csv", "bruto/musicas.csv")
    musicas_refinado = music_list_with_track_id()
    write_csv(musicas_refinado, 'refinado/musicas.csv', ['trackId', 'musica', 'artista', 'gravadora'])
    minioBuket.upload_to_minio("refinado", "musicas", "musicas.csv", "refinado/musicas.csv")


if __name__ == "__main__":
    main()