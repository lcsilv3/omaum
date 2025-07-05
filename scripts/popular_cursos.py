import sys
import os
import django

# Adicionar o caminho raiz do projeto ao sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Configurar o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from cursos.models import Curso


def popular_cursos():
    """
    Popula o banco de dados com uma lista predefinida de cursos.
    """
    cursos_a_criar = [
        {"nome": "Pré-Iniciático", "descricao": "Pré-Iniciático"},
        {"nome": "1º Grau", "descricao": "1º Grau"},
        {"nome": "2º Grau", "descricao": "2º Grau"},
        {"nome": "3º Grau", "descricao": "3º Grau"},
        {"nome": "4º Grau", "descricao": "4º Grau"},
        {"nome": "5º Grau", "descricao": "5º Grau"},
        {"nome": "Coleginho", "descricao": "Coleginho"},
        {"nome": "Colégio Sacerdotal", "descricao": "Colégio Sacerdotal"},
    ]

    print("Iniciando a população de cursos...")

    for dados_curso in cursos_a_criar:
        curso, criado = Curso.objects.get_or_create(
            nome=dados_curso["nome"],
            defaults={"descricao": dados_curso["descricao"], "ativo": True},
        )
        if criado:
            print(f"Curso '{curso.nome}' criado com sucesso.")
        else:
            print(f"Curso '{curso.nome}' já existe.")

    print("\nPopulação de cursos concluída!")


if __name__ == "__main__":
    popular_cursos()
