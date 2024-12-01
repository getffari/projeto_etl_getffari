@REM Instala as bibliotecas para rodar o programa na mão
@echo off
call venv\Scripts\activate
pip install requests
pip install pandas
pip install minio
pip install aiohttp
pip install asyncio

