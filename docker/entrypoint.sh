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

# Garantir que arquivos estáticos base existam
# (necessário porque o volume mount pode sobrescrever o build)
if [ ! -f "/app/static/img/logo.png" ]; then
    echo "⚠️  Arquivos estáticos base não encontrados em /app/static/"
    echo "Criando estrutura de diretórios..."
    mkdir -p /app/static/img
    
    # Se existir um backup dos arquivos estáticos no build
    if [ -d "/app/.static_backup" ]; then
        echo "Restaurando arquivos estáticos do backup..."
        cp -r /app/.static_backup/* /app/static/
    else
        echo "⚠️  Aviso: Arquivos estáticos base ausentes. Execute collectstatic manualmente."
    fi
fi

# Executar migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Executar servidor
if [ "$DJANGO_SETTINGS_MODULE" = "omaum.settings.development" ]; then
    echo "Iniciando servidor de desenvolvimento (runserver com hot-reload)..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Iniciando Gunicorn..."
    exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 omaum.wsgi:application
fi
