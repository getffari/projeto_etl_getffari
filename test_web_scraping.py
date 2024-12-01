import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
from minio import Minio
from minio.error import S3Error

URL = "https://maistocadas.mus.br/musicas-mais-tocadas/"
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
response = requests.get(URL, headers=HEADERS)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisando o HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando todos os itens <li> dentro do <ol>
    li_items = soup.find_all('li')

    # Abrir o arquivo CSV
    with open('musicas.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Música', 'Artista', 'Gravadora']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        
        # Escrever cabeçalho
        writer.writeheader()
        
        # Iterando sobre cada item <li>
        for li in li_items:
            # Extrair os dados de cada item
            text = li.get_text(strip=True)

             # Separando a string usando "–" como delimitador
            parts = re.split(r" – |-", text)

            if len(parts) == 3:
                musica = parts[0]
                artistas = parts[1]
                gravadora = parts[2]

                # Escrever no CSV
                writer.writerow({'Música': musica, 'Artista': artistas, 'Gravadora': gravadora})
            elif len(parts) > 3:
                musica = f"{parts[0]}-{parts[1]}"
                artistas = parts[2]
                gravadora = parts[3]

                # Escrever no CSV
                writer.writerow({'Música': musica, 'Artista': artistas, 'Gravadora': gravadora})
            

    print("CSV criado com sucesso!")     

    # Configurando o cliente MinIO
    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin123",
        secure=False
    )

    # Enviando o arquivo CSV para o bucket 'bruto'
    bucket_name = "bruto"
    object_name = "musicas.csv"
    file_path = "musicas.csv"

    try:
        client.fput_object(bucket_name, object_name, file_path)
        print(f"Arquivo '{object_name}' enviado para o bucket '{bucket_name}' com sucesso!")
    except S3Error as e:
        print(f"Erro ao enviar o arquivo: {e}")
        
else:
    print("Erro ao acessar a página")

