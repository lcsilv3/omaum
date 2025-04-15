from django.urls import path
from . import views

app_name = "alunos"

urlpatterns = [
    path("", views.listar_alunos, name="listar_alunos"),
    path("criar/", views.criar_aluno, name="criar_aluno"),
    path(
        "cadastrar/", views.criar_aluno, name="cadastrar_aluno"
    ),  # Alias para compatibilidade
    path("<str:cpf>/detalhes/", views.detalhar_aluno, name="detalhar_aluno"),
    path("<str:cpf>/editar/", views.editar_aluno, name="editar_aluno"),
    path("<str:cpf>/excluir/", views.excluir_aluno, name="excluir_aluno"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("exportar/", views.exportar_alunos, name="exportar_alunos"),
    path("importar/", views.importar_alunos, name="importar_alunos"),
    path("relatorio/", views.relatorio_alunos, name="relatorio_alunos"),
    path("search/", views.search_alunos, name="search_alunos"),
    # Nova URL para confirmação de remoção de instrutoria
    path(
        "<str:cpf>/confirmar-remocao-instrutoria/<str:nova_situacao>/",
        views.confirmar_remocao_instrutoria,
        name="confirmar_remocao_instrutoria",
    ),
    path(
        "api/search-instrutores/",
        views.search_instrutores,
        name="search_instrutores",
    ),
    path("api/get-aluno/<str:cpf>/", views.get_aluno, name="get_aluno"),
]
