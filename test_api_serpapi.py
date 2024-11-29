import requests

def test_serpapi(api_key, query):
    # URL da SerpApi para pesquisa no Google
    url = "https://serpapi.com/search"

    # Parâmetros de pesquisa (os parâmetros podem variar dependendo da pesquisa que você deseja fazer)
    params = {
        "api_key": "04c3691ab23fed5b5531d351bac30b711425995476a25af730f6f8ddb3876d55",
        "engine": "google",
        "q": "Músicas mais tocadas de 2024",
        "location": "Porto Alegre, State of Rio Grande do Sul, Brazil",
        "google_domain": "google.com.br",
        "gl": "br",
        "hl": "pt"
    }

    # Fazendo a requisição GET para a API da SerpApi
    response = requests.get(url, params=params)

    # Verificando o status da resposta
    if response.status_code == 200:
        print("Resposta recebida com sucesso!")
        # Aqui você pode trabalhar com os dados retornados pela API
        data = response.json()  # Converte o retorno JSON em um dicionário Python
        print(data)  # Exibe os dados recebidos
    else:
        print(f"Erro na requisição. Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # Substitua com sua chave da API SerpApi
    api_key = "sua_chave_de_api_aqui"
    query = "Python programming"

    test_serpapi(api_key, query)