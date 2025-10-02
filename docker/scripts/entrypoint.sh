#!/bin/bash
set -e

# Aguardar banco de dados
/wait-for-it.sh ${DATABASE_HOST:-omaum-db}:${DATABASE_PORT:-5432} --timeout=60 --strict

# Executar migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Criar superusuário se não existir
echo "Verificando superusuário..."
python manage.py create_superuser_if_none

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar comando passado como argumento
exec "$@"
