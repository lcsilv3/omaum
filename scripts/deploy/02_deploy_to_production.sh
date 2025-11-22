#!/bin/bash
################################################################################
# Script de Deploy Zero-Downtime para Produção
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configurações
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/docker"
BACKUP_DIR="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"
COMPOSE_FILE="$DOCKER_DIR/docker-compose.prod.yml"
ENV_FILE="$DOCKER_DIR/.env.production"

# Funções auxiliares
log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Verificar pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Arquivo docker-compose.prod.yml não encontrado!"
        exit 1
    fi
    
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Arquivo .env.production não encontrado!"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker não está instalado!"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose não está instalado!"
        exit 1
    fi
    
    log_success "Pré-requisitos verificados"
}

# Criar backup do banco de dados atual
backup_database() {
    log_info "Criando backup do banco de dados de produção..."
    mkdir -p "$BACKUP_DIR"
    
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T omaum-db \
        pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} > "$BACKUP_DIR/db_backup.sql"
    
    if [ -f "$BACKUP_DIR/db_backup.sql" ]; then
        BACKUP_SIZE=$(du -h "$BACKUP_DIR/db_backup.sql" | cut -f1)
        log_success "Backup criado: $BACKUP_DIR/db_backup.sql ($BACKUP_SIZE)"
    else
        log_error "Falha ao criar backup!"
        exit 1
    fi
}

# Pull de imagens e build
build_images() {
    log_info "Construindo novas imagens Docker..."
    
    cd "$DOCKER_DIR"
    docker-compose -f docker-compose.prod.yml --env-file .env.production build --pull
    
    log_success "Imagens construídas com sucesso"
}

# Importar dados do desenvolvimento
import_dev_data() {
    log_info "Importando dados de desenvolvimento..."
    
    # Encontrar arquivo de export mais recente
    EXPORT_FILE=$(ls -t "$SCRIPT_DIR/exports/dev_data_*.json" 2>/dev/null | head -1)
    
    if [ -z "$EXPORT_FILE" ]; then
        log_error "Nenhum arquivo de exportação encontrado!"
        log_error "Execute primeiro: python scripts/deploy/01_export_dev_data.py"
        exit 1
    fi
    
    log_info "Usando arquivo: $EXPORT_FILE"
    
    # Copiar arquivo para container
    docker cp "$EXPORT_FILE" omaum-web-prod:/tmp/dev_data.json
    
    # Limpar banco atual (cuidado!)
    log_warning "Limpando banco de dados atual..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T omaum-web \
        python manage.py flush --no-input
    
    # Importar dados
    log_info "Importando dados..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T omaum-web \
        python manage.py loaddata /tmp/dev_data.json
    
    log_success "Dados importados com sucesso"
}

# Aplicar migrações
apply_migrations() {
    log_info "Aplicando migrações do banco de dados..."
    
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T omaum-web \
        python manage.py migrate --no-input
    
    log_success "Migrações aplicadas"
}

# Coletar arquivos estáticos
collect_static() {
    log_info "Coletando arquivos estáticos..."
    
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T omaum-web \
        python manage.py collectstatic --no-input --clear
    
    log_success "Arquivos estáticos coletados"
}

# Rolling restart dos serviços
rolling_restart() {
    log_info "Iniciando rolling restart dos serviços..."
    
    cd "$DOCKER_DIR"
    
    # Atualizar serviços um por um
    SERVICES=("omaum-celery-beat" "omaum-celery" "omaum-web")
    
    for service in "${SERVICES[@]}"; do
        log_info "Reiniciando $service..."
        
        # Criar nova instância
        docker-compose -f docker-compose.prod.yml --env-file .env.production up -d --no-deps --scale $service=2 $service
        
        # Aguardar healthcheck
        sleep 10
        
        # Remover instância antiga
        docker-compose -f docker-compose.prod.yml --env-file .env.production up -d --no-deps --scale $service=1 $service
        
        log_success "$service reiniciado"
    done
    
    # Recarregar nginx
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec omaum-nginx nginx -s reload
    
    log_success "Rolling restart concluído"
}

# Verificar saúde dos serviços
health_check() {
    log_info "Verificando saúde dos serviços..."
    
    # Aguardar healthchecks
    sleep 5
    
    # Verificar status dos containers
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps
    
    # Verificar logs recentes
    log_info "Últimas linhas dos logs:"
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" logs --tail=20 omaum-web
    
    log_success "Verificação de saúde concluída"
}

# Smoke tests
smoke_tests() {
    log_info "Executando smoke tests..."
    
    # Teste de conectividade
    if curl -f http://localhost/health/ &> /dev/null; then
        log_success "Health check: OK"
    else
        log_error "Health check: FALHOU"
        return 1
    fi
    
    # Verificar dados no banco
    TURMAS_COUNT=$(docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T omaum-web \
        python manage.py shell -c "from turmas.models import Turma; print(Turma.objects.count())")
    
    log_info "Turmas no banco: $TURMAS_COUNT"
    
    if [ "$TURMAS_COUNT" -gt 0 ]; then
        log_success "Dados verificados: OK"
    else
        log_warning "Nenhuma turma encontrada no banco"
    fi
    
    log_success "Smoke tests concluídos"
}

# Função principal
main() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  DEPLOY ZERO-DOWNTIME - OMAUM PRODUÇÃO"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Confirmação
    read -p "Iniciar deploy para produção? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Deploy cancelado pelo usuário"
        exit 0
    fi
    
    # Executar etapas
    check_prerequisites
    backup_database
    build_images
    import_dev_data
    apply_migrations
    collect_static
    rolling_restart
    health_check
    smoke_tests
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_success "DEPLOY CONCLUÍDO COM SUCESSO!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    log_info "Backup salvo em: $BACKUP_DIR"
    echo ""
}

# Executar
main "$@"
