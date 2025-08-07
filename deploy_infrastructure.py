"""
FASE 3C: Script de deploy para infraestrutura avançada.
"""

import os
import sys
import time
import subprocess
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """
    Executa um comando e retorna se foi bem-sucedido.
    """
    print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro: {e.stderr}")
        return False


def check_requirements():
    """
    Verifica se os requisitos estão instalados.
    """
    print("🔍 Verificando requisitos...")
    
    requirements = [
        'redis-server --version',
        'postgresql --version',
        'python --version',
    ]
    
    for req in requirements:
        if not run_command(req, f"Verificando {req.split()[0]}"):
            print(f"⚠️  {req.split()[0]} não encontrado - pode precisar de instalação manual")
    
    return True


def setup_infrastructure():
    """
    Configura a infraestrutura avançada.
    """
    print("\n🏗️  SETUP DE INFRAESTRUTURA AVANÇADA")
    print("=" * 50)
    
    steps = [
        # 1. Instalar dependências Python
        ("pip install -r requirements-production.txt", "Instalando dependências Python"),
        
        # 2. Criar diretórios necessários
        ("mkdir -p logs staticfiles media", "Criando diretórios necessários"),
        
        # 3. Aplicar migrações
        ("python manage.py migrate", "Aplicando migrações do banco"),
        
        # 4. Criar índices do banco
        ("python manage.py migrate presencas 0009", "Criando índices otimizados"),
        
        # 5. Coletar arquivos estáticos
        ("python manage.py collectstatic --noinput", "Coletando arquivos estáticos"),
        
        # 6. Criar superusuário (se não existir)
        ("python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@omaum.com', 'admin123')\"", "Verificando usuário admin"),
        
        # 7. Verificar saúde do sistema
        ("python manage.py health_check --format=summary", "Verificando saúde do sistema"),
    ]
    
    success_count = 0
    
    for command, description in steps:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"⚠️  Falha em: {description}")
    
    print(f"\n📊 Resultado: {success_count}/{len(steps)} passos concluídos")
    
    if success_count == len(steps):
        print("🎉 Infraestrutura configurada com sucesso!")
        return True
    else:
        print("⚠️  Alguns passos falharam - verificar logs")
        return False


def start_services():
    """
    Inicia os serviços da infraestrutura.
    """
    print("\n🚀 INICIANDO SERVIÇOS")
    print("=" * 30)
    
    services = [
        # Redis (se não estiver rodando)
        ("redis-server --daemonize yes", "Iniciando Redis"),
        
        # Celery Worker
        ("celery -A omaum worker --loglevel=info --detach", "Iniciando Celery Worker"),
        
        # Celery Beat
        ("celery -A omaum beat --loglevel=info --detach", "Iniciando Celery Beat"),
        
        # Flower (monitoramento Celery)
        ("celery -A omaum flower --detach", "Iniciando Flower"),
    ]
    
    for command, description in services:
        run_command(command, description)
    
    print("\n🌐 Serviços iniciados!")
    print("Acesse:")
    print("  - Django: http://localhost:8000")
    print("  - Flower: http://localhost:5555")
    print("  - Admin: http://localhost:8000/admin")


def stop_services():
    """
    Para os serviços da infraestrutura.
    """
    print("\n🛑 PARANDO SERVIÇOS")
    print("=" * 25)
    
    # Parar processos Celery
    run_command("pkill -f celery", "Parando Celery")
    
    print("✅ Serviços parados")


def show_status():
    """
    Mostra o status dos serviços.
    """
    print("\n📊 STATUS DOS SERVIÇOS")
    print("=" * 30)
    
    checks = [
        ("redis-cli ping", "Redis"),
        ("pgrep -f 'celery.*worker'", "Celery Worker"),
        ("pgrep -f 'celery.*beat'", "Celery Beat"),
        ("pgrep -f 'celery.*flower'", "Flower"),
    ]
    
    for command, service in checks:
        if run_command(command, f"Verificando {service}"):
            print(f"✅ {service} - Rodando")
        else:
            print(f"❌ {service} - Parado")


def main():
    """
    Função principal do script de deploy.
    """
    if len(sys.argv) < 2:
        print("🔧 DEPLOY INFRAESTRUTURA OMAUM")
        print("=" * 40)
        print("Uso:")
        print("  python deploy_infrastructure.py setup    - Configurar infraestrutura")
        print("  python deploy_infrastructure.py start    - Iniciar serviços")
        print("  python deploy_infrastructure.py stop     - Parar serviços")
        print("  python deploy_infrastructure.py status   - Ver status")
        print("  python deploy_infrastructure.py health   - Verificar saúde")
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        check_requirements()
        setup_infrastructure()
        
    elif command == "start":
        start_services()
        
    elif command == "stop":
        stop_services()
        
    elif command == "status":
        show_status()
        
    elif command == "health":
        run_command("python manage.py health_check --format=summary", "Verificação de saúde")
        
    else:
        print(f"❌ Comando desconhecido: {command}")


if __name__ == "__main__":
    main()
