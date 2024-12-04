@REM Levanta o docker compose
docker-compose up -d

docker exec -it superset superset db upgrade
docker exec -it superset superset init
