from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

URL = "https://maistocadas.mus.br/musicas-mais-tocadas/"
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
response = requests.get(URL, headers=HEADERS)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisando o HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Abrir o arquivo CSV
    with open('musicas.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Música', 'Artista', 'Gravadora']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        
        # Escrever cabeçalho
        writer.writeheader()
        
        # Encontrar todos os itens da lista <li>
        for li in soup.find_all('li'):
            # Extrair os dados de cada item
            text = li.get_text(strip=True)
            
            # Dividir a string para separar música, artista e gravadora
            try:
                music, artists_and_label = text.split(" – ", 1)
                artists, label = artists_and_label.rsplit(" – ", 1)
                
                # Escrever no CSV
                writer.writerow({'Música': music, 'Artista': artists, 'Gravadora': label})
            except ValueError:
                # Caso algum item não tenha o formato esperado, ignoramos
                continue

    print("CSV criado com sucesso!")
            
          
else:
    print("Erro ao acessar a página")

