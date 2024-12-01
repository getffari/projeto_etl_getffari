import re
from bs4 import BeautifulSoup
import requests
import csv
from minio import Minio
from minio.error import S3Error

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
        return {'Música': parts[0], 'Artista': parts[1], 'Gravadora': parts[2]}
    elif len(parts) > 3:
        return {'Música': f"{parts[0]}-{parts[1]}", 'Artista': parts[2], 'Gravadora': parts[3]}
    return None

def write_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Música', 'Artista', 'Gravadora']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def upload_to_minio(client, bucket_name, object_name, file_path):
    client.fput_object(bucket_name, object_name, file_path)
    print(f"Arquivo '{object_name}' enviado para o bucket '{bucket_name}' com sucesso!")

def main():
    html = fetch_page(URL, HEADERS)
    texts = parse_html(html)
    data = [extract_data(text) for text in texts if extract_data(text) is not None]
    write_csv(data, 'musicas.csv')

    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin123",
        secure=False
    )

    try:
        upload_to_minio(client, "bruto", "musicas.csv", "musicas.csv")
    except S3Error as e:
        print(f"Erro ao enviar o arquivo: {e}")

if __name__ == "__main__":
    main()