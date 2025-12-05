import argparse
import shutil
import subprocess
from pathlib import Path


def ask_environment() -> str:
    prompt = "Selecione o ambiente ([D]esenvolvimento / [P]roducao) [padrao: D]: "
    while True:
        choice = input(prompt).strip().lower()
        if choice in {"", "d", "dev", "desenvolvimento"}:
            return "dev"
        if choice in {"p", "prod", "producao"}:
            return "prod"
        print("Opcao invalida. Informe D ou P.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inicializa o OMAUM via Docker (dev ou prod)",
    )
    parser.add_argument(
        "--env",
        choices=["dev", "prod"],
        help="Ambiente a ser iniciado (dev ou prod)",
    )
    parser.add_argument(
        "--app-url",
        help="URL personalizada para abrir o navegador",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    runner = repo_root / "scripts" / "run_omaum.ps1"
    if not runner.exists():
        print(f"Script não encontrado: {runner}")
        input("Pressione Enter para sair...")
        return

    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        print(
            "PowerShell não encontrado. Instale o PowerShell 7 ou habilite o Windows PowerShell."
        )
        input("Pressione Enter para sair...")
        return

    selected_env = args.env or ask_environment()

    command = [
        shell,
        "-ExecutionPolicy",
        "Bypass",
        "-NoLogo",
        "-File",
        str(runner),
        "-Environment",
        selected_env,
    ]
    if args.app_url:
        command.extend(["-AppUrl", args.app_url])

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(
            f"Ocorreu um erro ao acionar o script PowerShell (código {exc.returncode})."
        )
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
