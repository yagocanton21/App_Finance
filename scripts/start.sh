#!/bin/bash
echo "Aguardando PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL está pronto!"
echo "Inicializando tabelas..."
python scripts/init_db.py
echo "Iniciando aplicação..."
python -c "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=5000)"