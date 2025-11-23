import shutil
import subprocess
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    runner = repo_root / "scripts" / "run_omaum.ps1"
    if not runner.exists():
        print(f"Script não encontrado: {runner}")
        input("Pressione Enter para sair...")
        return

    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        print("PowerShell não encontrado. Instale o PowerShell 7 ou habilite o Windows PowerShell.")
        input("Pressione Enter para sair...")
        return

    command = [
        shell,
        "-ExecutionPolicy",
        "Bypass",
        "-NoLogo",
        "-File",
        str(runner),
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Ocorreu um erro ao acionar o script PowerShell (código {exc.returncode}).")
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
