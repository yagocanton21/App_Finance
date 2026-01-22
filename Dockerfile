FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar netcat para verificar se o PostgreSQL está pronto
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY . .

# Dar permissão de execução ao script
RUN chmod +x /app/scripts/start.sh

EXPOSE 5000

CMD ["/app/scripts/start.sh"]