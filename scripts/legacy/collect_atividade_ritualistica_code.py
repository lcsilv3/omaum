# Movido para scripts/legacy em 24/08/2025
# Script utilitário para revisão de código de atividades ritualísticas
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
root_dir = PROJECT_ROOT / "punicoes"


def collect_code(root_dir, output_file):
    # ...
    pass


if __name__ == "__main__":
    project_root = PROJECT_ROOT  # Atualize conforme necessário
    output_file = "atividade_ritualistica_code_review.md"
    collect_code(str(project_root), output_file)
    print(f"Code review file generated: {output_file}")
