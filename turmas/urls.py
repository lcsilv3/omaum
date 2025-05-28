"""
Configuração de URLs para o módulo de Turmas.

Padrão de Nomenclatura:
- Usamos 'turma_id' como nome do parâmetro nas URLs para identificar o ID da turma
- Para URLs que envolvem múltiplos modelos, usamos nomes específicos para cada ID
  (ex: 'turma_id', 'aluno_cpf')

Exemplos:
- path('<int:turma_id>/', views.detalhar_turma, name='detalhar_turma')
- path('<int:turma_id>/cancelar-matricula/<str:aluno_cpf>/', views.cancelar_matricula, name='cancelar_matricula')
"""
from django.urls import path
from . import views

app_name = "turmas"

urlpatterns = [
    # URLs existentes
    path("", views.listar_turmas, name="listar_turmas"),
    path("criar/", views.criar_turma, name="criar_turma"),
    path("<int:turma_id>/", views.detalhar_turma, name="detalhar_turma"),
    path("<int:turma_id>/editar/", views.editar_turma, name="editar_turma"),
    path("<int:turma_id>/excluir/", views.excluir_turma, name="excluir_turma"),
    
    # URLs para gerenciamento de alunos na turma
    path("<int:turma_id>/alunos/", views.listar_alunos_turma, name="listar_alunos_turma"),
    path("<int:turma_id>/matricular/", views.matricular_aluno, name="matricular_aluno"),
    path("<int:turma_id>/remover-aluno/<str:aluno_id>/", views.remover_aluno_turma, name="remover_aluno_turma"),
    
    # URLs para gerenciamento de instrutores
    path("<int:turma_id>/instrutores/", views.atualizar_instrutores, name="atualizar_instrutores"),
    path("<int:turma_id>/remover-instrutor/<str:tipo>/", views.remover_instrutor, name="remover_instrutor"),
    
    # URLs para gerenciamento de atividades
    path("<int:turma_id>/atividades/", views.listar_atividades_turma, name="listar_atividades_turma"),
    path("<int:turma_id>/adicionar-atividade/", views.adicionar_atividade_turma, name="adicionar_atividade_turma"),
    
    # URLs para frequência
    path("<int:turma_id>/registrar-frequencia/", views.registrar_frequencia_turma, name="registrar_frequencia_turma"),
    path("<int:turma_id>/relatorio-frequencia/", views.relatorio_frequencia_turma, name="relatorio_frequencia_turma"),
    
    # URLs para exportação e relatórios
    path("exportar/", views.exportar_turmas, name="exportar_turmas"),
    path("importar/", views.importar_turmas, name="importar_turmas"),
    path("relatorio/", views.relatorio_turmas, name="relatorio_turmas"),
    path("dashboard/", views.dashboard_turmas, name="dashboard_turmas"),
    
    # API endpoints
    path("api/turmas-por-curso/", views.turmas_por_curso, name="turmas_por_curso"),
]