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

# Instalar dependências de teste no ambiente de desenvolvimento
if [ "$DJANGO_SETTINGS_MODULE" = "omaum.settings.development" ]; then
    echo "Instalando dependências de teste (pytest e plugins)..."
    # Verifica se pytest-cov está instalado; se não, instala o conjunto necessário
    if ! python -c "import importlib; importlib.import_module('pytest_cov')" >/dev/null 2>&1; then
        pip install --no-cache-dir \
            pytest==7.4.3 \
            pytest-django==4.7.0 \
            pytest-cov==4.1.0 \
            pytest-xdist==3.5.0 \
            coverage==7.3.4 || true
    else
        echo "Dependências de teste já instaladas."
    fi
fi

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
