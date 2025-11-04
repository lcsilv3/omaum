#!/usr/bin/env python3
"""
Script para verificar o status do servidor Docker do projeto OMAUM.

Este script verifica se os containers Docker do projeto estão ativos e saudáveis.
Pode ser executado diretamente ou importado como módulo.

Uso:
    python scripts/verificar_docker.py [opções]

Opções:
    --verbose, -v     Saída detalhada
    --quiet, -q       Apenas mostra status resumido
    --json            Saída em formato JSON
    --help, -h        Mostra esta mensagem de ajuda

Exemplos:
    python scripts/verificar_docker.py
    python scripts/verificar_docker.py --verbose
    python scripts/verificar_docker.py --json

Autor: Sistema OMAUM
Data: Janeiro 2024
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class Colors:
    """Códigos de cores ANSI para saída colorida no terminal."""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


class DockerChecker:
    """Classe para verificar o status dos containers Docker do projeto OMAUM."""

    def __init__(self, verbose=False, quiet=False):
        """
        Inicializa o verificador de Docker.

        Args:
            verbose (bool): Se True, mostra informações detalhadas
            quiet (bool): Se True, mostra apenas status resumido
        """
        self.verbose = verbose
        self.quiet = quiet
        self.project_root = Path(__file__).parent.parent
        self.compose_file = self.project_root / "docker" / "docker-compose.yml"

        # Serviços críticos esperados no docker-compose
        # Nota: nginx e celery são serviços opcionais (profiles) e não são verificados
        self.expected_services = {
            "omaum-web": "Servidor Web Django",
            "omaum-db": "Banco de Dados PostgreSQL",
            "omaum-redis": "Cache Redis",
        }

    def _run_command(self, command):
        """
        Executa um comando shell e retorna o resultado.

        Args:
            command (list): Lista com o comando e argumentos

        Returns:
            tuple: (stdout, stderr, returncode)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=15,
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Comando expirou após 15 segundos", 1
        except Exception as e:
            return "", str(e), 1

    def check_docker_installed(self):
        """
        Verifica se Docker está instalado.

        Returns:
            dict: Informações sobre a instalação do Docker
        """
        stdout, stderr, returncode = self._run_command(["docker", "--version"])

        if returncode == 0:
            return {
                "installed": True,
                "version": stdout,
                "message": "Docker instalado",
            }
        else:
            return {
                "installed": False,
                "version": None,
                "message": f"Docker não encontrado: {stderr}",
            }

    def check_docker_compose_installed(self):
        """
        Verifica se Docker Compose está instalado.

        Returns:
            dict: Informações sobre a instalação do Docker Compose
        """
        stdout, stderr, returncode = self._run_command(["docker", "compose", "version"])

        if returncode == 0:
            return {
                "installed": True,
                "version": stdout,
                "message": "Docker Compose instalado",
            }
        else:
            return {
                "installed": False,
                "version": None,
                "message": f"Docker Compose não encontrado: {stderr}",
            }

    def check_containers_status(self):
        """
        Verifica o status dos containers do projeto.

        Returns:
            dict: Informações sobre os containers
        """
        if not self.compose_file.exists():
            return {
                "error": True,
                "message": f"Arquivo docker-compose.yml não encontrado em {self.compose_file}",
                "containers": [],
            }

        stdout, stderr, returncode = self._run_command(
            ["docker", "compose", "-f", str(self.compose_file), "ps", "--format", "json"]
        )

        if returncode != 0:
            return {
                "error": True,
                "message": f"Erro ao verificar containers: {stderr}",
                "containers": [],
            }

        # Parse JSON output
        containers = []
        if stdout:
            for line in stdout.split("\n"):
                if line.strip():
                    try:
                        container_data = json.loads(line)
                        containers.append(
                            {
                                "name": container_data.get("Name", ""),
                                "service": container_data.get("Service", ""),
                                "state": container_data.get("State", ""),
                                "status": container_data.get("Status", ""),
                                "health": container_data.get("Health", ""),
                            }
                        )
                    except json.JSONDecodeError:
                        continue

        return {
            "error": False,
            "message": "Status dos containers verificado",
            "containers": containers,
            "total": len(containers),
            "running": sum(1 for c in containers if c["state"] == "running"),
        }

    def get_service_health(self, service_name):
        """
        Verifica a saúde de um serviço específico.

        Args:
            service_name (str): Nome do serviço

        Returns:
            dict: Informações de saúde do serviço
        """
        stdout, stderr, returncode = self._run_command(
            [
                "docker",
                "compose",
                "-f",
                str(self.compose_file),
                "ps",
                "--format",
                "json",
                service_name,
            ]
        )

        if returncode != 0 or not stdout:
            return {
                "healthy": False,
                "status": "not found",
                "message": f"Serviço {service_name} não encontrado",
            }

        try:
            lines = stdout.split("\n")
            if not lines or not lines[0].strip():
                return {
                    "healthy": False,
                    "status": "not found",
                    "message": f"Serviço {service_name} não encontrado",
                }
            container_data = json.loads(lines[0])
            state = container_data.get("State", "")
            health = container_data.get("Health", "")

            is_healthy = state == "running"
            if health:
                is_healthy = is_healthy and health == "healthy"

            return {
                "healthy": is_healthy,
                "status": state,
                "health": health,
                "message": f"Serviço {service_name}: {state}" + (f" ({health})" if health else ""),
            }
        except (json.JSONDecodeError, IndexError):
            return {
                "healthy": False,
                "status": "error",
                "message": f"Erro ao verificar saúde do serviço {service_name}",
            }

    def print_status(self, status_data):
        """
        Imprime o status de forma formatada.

        Args:
            status_data (dict): Dados de status coletados
        """
        if self.quiet:
            # Modo silencioso: apenas status resumido
            is_healthy = (
                status_data["docker"]["installed"]
                and status_data["docker_compose"]["installed"]
                and status_data["containers"]["running"] > 0
            )
            print("✓ ATIVO" if is_healthy else "✗ INATIVO")
            return

        # Cabeçalho
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(
            f"{Colors.BOLD}{Colors.BLUE}Verificação do Servidor Docker - Projeto OMAUM{Colors.END}"
        )
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

        # Status do Docker
        docker_status = status_data["docker"]
        if docker_status["installed"]:
            print(f"{Colors.GREEN}✓{Colors.END} Docker: {docker_status['version']}")
        else:
            print(f"{Colors.RED}✗{Colors.END} Docker: {docker_status['message']}")

        # Status do Docker Compose
        compose_status = status_data["docker_compose"]
        if compose_status["installed"]:
            print(f"{Colors.GREEN}✓{Colors.END} Docker Compose: {compose_status['version']}")
        else:
            print(f"{Colors.RED}✗{Colors.END} Docker Compose: {compose_status['message']}")

        print()

        # Status dos Containers
        containers_data = status_data["containers"]
        if containers_data["error"]:
            print(f"{Colors.RED}✗{Colors.END} Containers: {containers_data['message']}")
        else:
            total = containers_data["total"]
            running = containers_data["running"]

            if running > 0:
                print(
                    f"{Colors.GREEN}✓{Colors.END} Containers: {running}/{total} em execução"
                )
            elif total > 0:
                print(
                    f"{Colors.YELLOW}⚠{Colors.END} Containers: {running}/{total} em execução"
                )
            else:
                print(f"{Colors.YELLOW}⚠{Colors.END} Containers: Nenhum container encontrado")

            # Lista detalhada de containers
            if self.verbose and containers_data["containers"]:
                print(f"\n{Colors.BOLD}Detalhes dos Containers:{Colors.END}")
                for container in containers_data["containers"]:
                    state = container["state"]
                    color = Colors.GREEN if state == "running" else Colors.RED

                    status_line = f"  • {container['name']}"
                    status_line += f" ({container['service']})"
                    status_line += f" - {color}{state}{Colors.END}"

                    if container.get("health"):
                        health_color = (
                            Colors.GREEN
                            if container["health"] == "healthy"
                            else Colors.YELLOW
                        )
                        status_line += f" [{health_color}{container['health']}{Colors.END}]"

                    print(status_line)

        # Verificação de serviços críticos
        print(f"\n{Colors.BOLD}Serviços Críticos:{Colors.END}")
        for service_name, description in self.expected_services.items():
            health = status_data["services"].get(service_name, {})
            if health.get("healthy"):
                print(f"{Colors.GREEN}✓{Colors.END} {description}: {health['status']}")
            else:
                status = health.get("status", "não verificado")
                print(f"{Colors.RED}✗{Colors.END} {description}: {status}")

        # Status final
        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
        all_healthy = (
            docker_status["installed"]
            and compose_status["installed"]
            and containers_data["running"] > 0
            and all(
                status_data["services"].get(s, {}).get("healthy", False)
                for s in self.expected_services.keys()
            )
        )

        if all_healthy:
            print(
                f"{Colors.GREEN}{Colors.BOLD}✓ Servidor OMAUM está ATIVO e SAUDÁVEL{Colors.END}"
            )
        else:
            print(
                f"{Colors.YELLOW}{Colors.BOLD}⚠ Servidor OMAUM está INATIVO ou com problemas{Colors.END}"
            )
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    def check_all(self):
        """
        Executa todas as verificações.

        Returns:
            dict: Dados completos de status
        """
        status_data = {
            "timestamp": datetime.now().isoformat(),
            "docker": self.check_docker_installed(),
            "docker_compose": self.check_docker_compose_installed(),
            "containers": self.check_containers_status(),
            "services": {},
        }

        # Verificar serviços críticos
        for service_name in self.expected_services.keys():
            status_data["services"][service_name] = self.get_service_health(service_name)

        return status_data


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Verificar status do servidor Docker do projeto OMAUM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s                    Verificação padrão
  %(prog)s --verbose          Saída detalhada
  %(prog)s --quiet            Apenas status resumido
  %(prog)s --json             Saída em formato JSON
        """,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Mostra informações detalhadas",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Mostra apenas status resumido",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Saída em formato JSON",
    )

    args = parser.parse_args()

    # Criar verificador
    checker = DockerChecker(verbose=args.verbose, quiet=args.quiet)

    # Executar verificações
    status_data = checker.check_all()

    # Saída
    if args.json:
        print(json.dumps(status_data, indent=2, ensure_ascii=False))
    else:
        checker.print_status(status_data)

    # Código de saída
    is_healthy = (
        status_data["docker"]["installed"]
        and status_data["docker_compose"]["installed"]
        and status_data["containers"]["running"] > 0
    )

    sys.exit(0 if is_healthy else 1)


if __name__ == "__main__":
    main()
