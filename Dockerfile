# Usando uma imagem base do Python
FROM python:3.8-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo de script para o container
COPY main.py /app

# Instalando dependências (se houver)
RUN pip install --no-cache-dir requests

# Definindo o comando que será executado ao rodar o container
CMD ["python", "main.py"]