#!/bin/bash
################################################################################
# Script de Transferência de Arquivos para Servidor de Produção (Linux/Mac)
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Funções auxiliares
log_info() { echo -e "${CYAN}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[AVISO]${NC} $1"; }
log_error() { echo -e "${RED}[ERRO]${NC} $1"; }

# Configurações
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
EXPORT_DIR="$SCRIPT_DIR/exports"

# Parâmetros
SERVER_HOST="${1:-}"
SERVER_USER="${2:-}"
SERVER_PATH="${3:-/var/www/omaum}"

# Encontrar arquivo de exportação mais recente
find_latest_export() {
    local latest_file=$(ls -t "$EXPORT_DIR"/dev_data_*.json 2>/dev/null | head -1)
    
    if [ -z "$latest_file" ]; then
        log_error "Nenhum arquivo de exportacao encontrado!"
        log_error "Execute primeiro: python scripts/deploy/01_export_dev_data.py"
        exit 1
    fi
    
    echo "$latest_file"
}

# Verificar SCP disponível
check_scp() {
    if ! command -v scp &> /dev/null; then
        log_error "SCP nao esta instalado!"
        exit 1
    fi
}

# Transferir arquivo
transfer_file() {
    local file="$1"
    local destination="$2"
    
    log_info "Transferindo via SCP..."
    log_info "Arquivo: $(basename "$file")"
    log_info "Destino: $destination"
    
    scp "$file" "${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/scripts/deploy/exports/"
    
    if [ $? -eq 0 ]; then
        log_success "Arquivo transferido com sucesso!"
        return 0
    else
        log_error "Erro ao transferir arquivo!"
        return 1
    fi
}

# Função principal
main() {
    echo ""
    echo "================================================================"
    echo "  TRANSFERENCIA DE DADOS PARA PRODUCAO"
    echo "================================================================"
    echo ""
    
    # Encontrar arquivo mais recente
    export_file=$(find_latest_export)
    file_size=$(du -h "$export_file" | cut -f1)
    
    log_info "Arquivo encontrado:"
    echo "  Nome: $(basename "$export_file")"
    echo "  Tamanho: $file_size"
    echo "  Data: $(date -r "$export_file" '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Solicitar informações do servidor se não fornecidas
    if [ -z "$SERVER_HOST" ]; then
        read -p "Digite o IP ou hostname do servidor: " SERVER_HOST
    fi
    
    if [ -z "$SERVER_USER" ]; then
        read -p "Digite o usuario SSH: " SERVER_USER
    fi
    
    if [ -z "$SERVER_PATH" ]; then
        read -p "Digite o caminho no servidor [/var/www/omaum]: " user_path
        SERVER_PATH="${user_path:-/var/www/omaum}"
    fi
    
    echo ""
    log_info "Configuracao:"
    echo "  Servidor: ${SERVER_USER}@${SERVER_HOST}"
    echo "  Destino: ${SERVER_PATH}/scripts/deploy/exports/"
    echo ""
    
    # Confirmar transferência
    read -p "Iniciar transferencia? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Transferencia cancelada pelo usuario"
        exit 0
    fi
    
    echo ""
    
    # Verificar SCP
    check_scp
    
    # Transferir arquivo
    if transfer_file "$export_file" "${SERVER_USER}@${SERVER_HOST}:${SERVER_PATH}/scripts/deploy/exports/"; then
        echo ""
        echo "================================================================"
        log_success "TRANSFERENCIA CONCLUIDA COM SUCESSO!"
        echo "================================================================"
        echo ""
        log_info "Proximo passo no servidor:"
        echo "  ssh ${SERVER_USER}@${SERVER_HOST}"
        echo "  cd ${SERVER_PATH}"
        echo "  ./scripts/deploy/02_deploy_to_production.sh"
        echo ""
    else
        exit 1
    fi
}

# Executar
main "$@"
