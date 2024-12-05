# projeto_etl_getffari
Repositorio com o objetivo de conter os codigos para realizar a extração transformação e carregamento das api do Spotify e SerpApi 

## Ideia inicial do Projeto
Tema: Análise de tendências Artista e Generos Musicais.

### ETL:

### Extract:
> Use o site https://maistocadas.mus.br/musicas-mais-tocadas/ musicas e artistas mais populares de 2024
> Use a API do Spotify para coletar dados de músicas (artistas, popularidade, gêneros).

#### Transform:
> Relacione musicasa popular com os artistas no spotify
> Extraia insights, como gêneros em alta ou artistas.

#### Load:
> Salve em uma ambiente analitico para analise e criação de insights sobre o tema

##### Tecnologias utilizadas:
- Arquivos.bat
- Docker para o ambiente que vai suportar as outras aplicações
- Python para o Web Scraping
- API do Spotify
- Minio para o armazenamento
- Trino para a camada analitica
- Super Set para criação de Dashboards e relatorios sobre o tema

###### Comandos utilizados
- Construindo/atualizando o container
    docker build -t projeto_etl_getffari . 
- Executando o containe
    docker run projeto_etl_getffari 
- Subindo os containers do docker-compose
    docker-compose up -d 
- Verificando container de pé
    docker ps


-- superset
3- rodar os comandos abaixo no terminar 1 a 1:

docker exec -it superset superset fab create-admin --username=admin --password=admin --firstname=admin --lastname=admin --email=admin@example.org
docker exec -it superset superset db upgrade
<!-- Opcional, só serve para carregar exemplos -->
docker exec -it superset superset load_examples
docker exec -it superset superset init

#String de conexÃ¢o do Trino no Superset
trino://admin@trino-coordinator:8080/minio





