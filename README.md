# projeto_etl_getffari
Repositorio com o objetivo de conter os codigos para realizar a extração transformação e carregamento das api do Spotify e SerpApi 

## Ideia inicial do Projeto
Tema: Análise de tendências musicais.

### ETL:

### Extract:
> Use a SerpApi para buscar notícias sobre artistas populares.
> Use a API do Spotify para coletar dados de músicas (nome, popularidade, gêneros).

#### Transform:
> Relacione artistas populares com as músicas mais tocadas no Spotify.
> Extraia insights, como gêneros em alta ou artistas mencionados nas notícias.

#### Load:
> Salve em um banco (PostgreSQL ou SQLite) para análises futuras.

##### Tecnologias utilizadas:

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
docker exec -it superset superset load_examples
docker exec -it superset superset init

#String de conexÃ¢o do Trino no Superset
trino://admin@trino-coordinator:8080/minio





