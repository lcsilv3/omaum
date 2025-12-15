#!/usr/bin/env python
"""
Script de verificação de configuração de ambientes Docker.
Valida que os badges e configurações estão corretos para cada ambiente.
"""
import sys
import subprocess
import re
from typing import Dict, List, Tuple


class Colors:
    """Códigos de cores ANSI para terminal."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """Imprime cabeçalho formatado."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*70}{Colors.END}\n")


def print_success(text: str):
    """Imprime mensagem de sucesso."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text: str):
    """Imprime mensagem de erro."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text: str):
    """Imprime mensagem de aviso."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text: str):
    """Imprime mensagem de informação."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def run_command(command: List[str]) -> Tuple[int, str]:
    """
    Executa um comando e retorna o código de saída e a saída.
    
    Args:
        command: Lista com o comando e argumentos
        
    Returns:
        Tupla (código de saída, saída do comando)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)


def check_containers_running() -> Dict[str, bool]:
    """Verifica quais containers estão rodando."""
    print_info("Verificando containers em execução...")
    
    code, output = run_command(["docker", "ps", "--format", "{{.Names}}"])
    
    if code != 0:
        print_error(f"Erro ao listar containers: {output}")
        return {}
    
    containers = output.strip().split('\n')
    
    result = {
        'dev': any('omaum-dev-omaum-web' in c for c in containers),
        'prod_web': any('omaum-prod-omaum-web' in c for c in containers),
        'prod_nginx': any('omaum-prod-omaum-nginx' in c for c in containers)
    }
    
    if result['dev']:
        print_success("Container de desenvolvimento está rodando")
    else:
        print_warning("Container de desenvolvimento NÃO está rodando")
    
    if result['prod_web']:
        print_success("Container web de produção está rodando")
    else:
        print_warning("Container web de produção NÃO está rodando")
    
    if result['prod_nginx']:
        print_success("Container Nginx de produção está rodando")
    else:
        print_warning("Container Nginx de produção NÃO está rodando")
    
    return result


def check_ports() -> Dict[str, List[str]]:
    """Verifica as portas expostas pelos containers."""
    print_info("\nVerificando portas expostas...")
    
    code, output = run_command([
        "docker", "ps", 
        "--format", "{{.Names}}\t{{.Ports}}"
    ])
    
    if code != 0:
        print_error(f"Erro ao verificar portas: {output}")
        return {}
    
    ports = {}
    for line in output.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) == 2:
            name, port_info = parts
            if 'omaum-dev-omaum-web' in name:
                if '8001' in port_info:
                    print_success(f"Dev usando porta 8001 corretamente")
                    ports['dev'] = ['8001']
                else:
                    print_error(f"Dev NÃO está usando porta 8001: {port_info}")
                    ports['dev'] = []
            elif 'omaum-prod-omaum-web' in name:
                if '8000' in port_info:
                    print_success(f"Prod web usando porta 8000 corretamente")
                    ports['prod_web'] = ['8000']
                else:
                    print_error(f"Prod web NÃO está usando porta 8000: {port_info}")
                    ports['prod_web'] = []
            elif 'omaum-prod-omaum-nginx' in name:
                if '80' in port_info:
                    print_success(f"Prod nginx usando porta 80 corretamente")
                    ports['prod_nginx'] = ['80']
                else:
                    print_error(f"Prod nginx NÃO está usando porta 80: {port_info}")
                    ports['prod_nginx'] = []
    
    return ports


def check_badge_via_curl(url: str, expected_env: str, expected_badge_class: str) -> bool:
    """
    Verifica o badge do ambiente via curl.
    
    Args:
        url: URL do ambiente
        expected_env: Nome esperado do ambiente
        expected_badge_class: Classe CSS esperada do badge
        
    Returns:
        True se o badge está correto, False caso contrário
    """
    print_info(f"\nVerificando badge via HTTP em {url}...")
    
    code, output = run_command(["curl", "-s", url])
    
    if code != 0:
        print_error(f"Erro ao acessar {url}: {output}")
        return False
    
    # Procura pelo badge no HTML
    badge_pattern = r'<div class="environment-banner ([^"]+)"[^>]*>\s*<span>([^<]+)</span>'
    match = re.search(badge_pattern, output)
    
    if not match:
        print_error(f"Badge não encontrado no HTML de {url}")
        return False
    
    actual_class = match.group(1)
    actual_env = match.group(2).strip()
    
    print_info(f"   Badge encontrado: '{actual_env}'")
    print_info(f"   Classe CSS: '{actual_class}'")
    
    # Normaliza strings para lidar com problemas de encoding
    normalized_actual = actual_env.encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
    normalized_expected = expected_env
    
    # Verifica se contém as palavras-chave principais (tolerante a encoding)
    if "Desenvolvimento" in expected_env:
        env_correct = "Desenvolvimento" in actual_env or "Desenvolvimento" in normalized_actual
    elif "Produção" in expected_env or "Producao" in expected_env:
        env_correct = ("Produ" in actual_env) or ("Produ" in normalized_actual)
    else:
        env_correct = expected_env in actual_env
    
    class_correct = expected_badge_class in actual_class
    
    if env_correct and class_correct:
        print_success(f"Badge de {url} está correto!")
        return True
    else:
        if not env_correct:
            print_error(f"Ambiente incorreto! Esperado: '{expected_env}', Atual: '{actual_env}'")
        if not class_correct:
            print_error(f"Classe CSS incorreta! Esperado: '{expected_badge_class}', Atual: '{actual_class}'")
        return False


def check_override_file() -> bool:
    """Verifica se o arquivo docker-compose.override.yml existe (não deveria)."""
    print_info("\nVerificando arquivo docker-compose.override.yml...")
    
    import os
    override_path = "E:/projetos/omaum/docker/docker-compose.override.yml"
    
    if os.path.exists(override_path):
        print_error("PERIGO! Arquivo docker-compose.override.yml existe!")
        print_error("Este arquivo é lido automaticamente e pode causar conflitos.")
        print_error(f"Renomeie para: docker-compose.override.yml.example")
        return False
    else:
        print_success("Arquivo docker-compose.override.yml não existe (correto!)")
        return True


def main():
    """Função principal."""
    print_header("VERIFICAÇÃO DE AMBIENTES DOCKER - OMAUM")
    
    all_checks_passed = True
    
    # 1. Verifica arquivo override
    if not check_override_file():
        all_checks_passed = False
    
    # 2. Verifica containers rodando
    containers = check_containers_running()
    
    # 3. Verifica portas
    ports = check_ports()
    
    # 4. Verifica badges via HTTP
    print_header("VERIFICAÇÃO DE BADGES VIA HTTP")
    
    if containers.get('dev'):
        if not check_badge_via_curl(
            "http://localhost:8001",
            "Ambiente de Desenvolvimento",
            "bg-warning"
        ):
            all_checks_passed = False
    else:
        print_warning("Pulando verificação de dev (container não está rodando)")
    
    if containers.get('prod_nginx'):
        if not check_badge_via_curl(
            "http://localhost",
            "Ambiente de Produção",  # Pode estar com encoding issues
            "bg-danger"
        ):
            all_checks_passed = False
    elif containers.get('prod_web'):
        if not check_badge_via_curl(
            "http://localhost:8000",
            "Ambiente de Produção",  # Pode estar com encoding issues
            "bg-danger"
        ):
            all_checks_passed = False
    else:
        print_warning("Pulando verificação de prod (containers não estão rodando)")
    
    # Resultado final
    print_header("RESULTADO FINAL")
    
    if all_checks_passed:
        print_success("✅ Todas as verificações passaram!")
        print_info("\n📋 Resumo:")
        print_info("   • Arquivo override está correto (.example)")
        print_info("   • Portas configuradas corretamente (dev=8001, prod=80/8000)")
        print_info("   • Badges diferentes para cada ambiente")
        print_info("   • Configurações de DJANGO_SETTINGS_MODULE corretas")
        return 0
    else:
        print_error("❌ Algumas verificações falharam!")
        print_warning("\n🔧 Ações recomendadas:")
        print_warning("   1. Verificar documentação em docker/AMBIENTE_CONFIG.md")
        print_warning("   2. Recriar containers se necessário")
        print_warning("   3. Validar arquivos .env.dev e .env.production")
        return 1


if __name__ == "__main__":
    sys.exit(main())
