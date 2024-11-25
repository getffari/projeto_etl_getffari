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
docker build -t projeto_etl_getffari . - Construindo/atualizando o container
docker run projeto_etl_getffari - Executando o containe
docker-compose up -d - Subindo os containers do docker-compose
