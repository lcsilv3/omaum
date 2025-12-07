#!/bin/bash
set -e

# Aguardar banco de dados estar pronto
echo "Aguardando banco de dados..."

# Usar pg_isready para verificar conexão
while ! pg_isready -h omaum-db -p 5432 -U omaum_user > /dev/null 2>&1; do
    echo "Banco ainda não está pronto, aguardando..."
    sleep 1
done

echo "Banco de dados conectado!"

# Executar migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Executar Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 omaum.wsgi:application
