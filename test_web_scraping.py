from bs4 import BeautifulSoup
import pandas as pd
import requests

URL = "https://maistocadas.mus.br/musicas-mais-tocadas/"
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
response = requests.get(URL, headers=HEADERS)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Analisando o HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrando todos os itens <li> dentro do <ol>
    li_items = soup.find_all('li')
    
    # Lista para armazenar os dados extraídos
    data = []

    # Iterando sobre cada item <li>
    for item in li_items:
        # Limpando o texto
        text = item.get_text(strip=True)
        
        # Separando a string usando "–" como delimitador
        parts = text.split(" – ")
        
        # Garantindo que a separação tenha 3 partes (Música, Artista(s), Gravadora)
        if len(parts) == 3:
            musica = parts[0]
            artistas = parts[1]
            gravadora = parts[2]
            
            # Adicionando os dados na lista
            data.append({'Música': musica, 'Artistas': artistas, 'Gravadora': gravadora})

            # Criando um DataFrame com os dados extraídos
            df = pd.DataFrame(data)

            # Salvando o DataFrame em um arquivo CSV
            df.to_csv('./app/musicas.csv', index=False, encoding='utf-8')

    print("oi2")

            
else:
    print("Erro ao acessar a página")

