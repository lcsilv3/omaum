"""
URLs do aplicativo Presencas seguindo o padrão do contrato.
"""

from django.urls import path
from .views_ext.multiplas import (
    registrar_presencas_multiplas,
    formulario_presencas_multiplas
)
from . import views
from .views_ext.registro_presenca import (
    registrar_presenca_dados_basicos,
    registrar_presenca_dados_basicos_ajax,
    registrar_presenca_totais_atividades,
    registrar_presenca_totais_atividades_ajax,
    registrar_presenca_dias_atividades,
    registrar_presenca_dias_atividades_ajax,
    registrar_presenca_alunos,
    registrar_presenca_alunos_ajax,
    registrar_presenca_confirmar,
    registrar_presenca_confirmar_ajax,
    turmas_por_curso_ajax,
    atividades_por_turma_ajax,
    obter_limites_calendario_ajax,
    editar_presenca_dados_basicos,
    editar_presenca_totais_atividades,
    editar_presenca_dias_atividades,
    editar_presenca_alunos,
    detalhar_presenca_dados_basicos,
    detalhar_presenca_totais_atividades,
    detalhar_presenca_dias_atividades,
    detalhar_presenca_alunos,
)

app_name = "presencas"

urlpatterns = [
    # URLs principais seguindo o padrão do contrato
    
    # Presenças Acadêmicas
    path("academicas/", views.listar_presencas_academicas, 
         name="listar_presencas_academicas"),
    path("academicas/criar/", views.registrar_presenca_academica, 
         name="criar_presenca_academica"),
    path("academicas/<int:presenca_id>/", views.detalhar_presenca_academica, 
         name="detalhar_presenca_academica"),
    path("academicas/<int:presenca_id>/editar/", views.editar_presenca_academica, 
         name="editar_presenca_academica"),
    path("academicas/<int:presenca_id>/excluir/", views.excluir_presenca_academica, 
         name="excluir_presenca_academica"),
    path("academicas/exportar/", views.exportar_presencas_academicas, 
         name="exportar_presencas_academicas"),
    path("academicas/importar/", views.importar_presencas_academicas, 
         name="importar_presencas_academicas"),

    # Presenças Ritualísticas
    path("ritualisticas/", views.listar_presencas_ritualisticas, 
         name="listar_presencas_ritualisticas"),
    path("ritualisticas/criar/", views.registrar_presenca_ritualistica, 
         name="criar_presenca_ritualistica"),
    path("ritualisticas/<int:presenca_id>/", views.detalhar_presenca_ritualistica, 
         name="detalhar_presenca_ritualistica"),
    path("ritualisticas/<int:presenca_id>/editar/", views.editar_presenca_ritualistica, 
         name="editar_presenca_ritualistica"),
    path("ritualisticas/<int:presenca_id>/excluir/", views.excluir_presenca_ritualistica, 
         name="excluir_presenca_ritualistica"),
    path("ritualisticas/exportar/", views.exportar_presencas_ritualisticas, 
         name="exportar_presencas_ritualisticas"),
    path("ritualisticas/importar/", views.importar_presencas_ritualisticas, 
         name="importar_presencas_ritualisticas"),

    # Observações de presença
    path("observacoes/", views.listar_observacoes_presenca, 
         name="listar_observacoes_presenca"),

    # Presenças múltiplas
    path("multiplas/", registrar_presencas_multiplas, 
         name="registrar_presencas_multiplas"),
    path("multiplas/formulario/", formulario_presencas_multiplas, 
         name="formulario_presencas_multiplas"),

    # Processo de registro multi-etapas
    path('registro/dados-basicos/', registrar_presenca_dados_basicos, 
         name='registrar_presenca_dados_basicos'),
    path('registro/dados-basicos/ajax/', registrar_presenca_dados_basicos_ajax, 
         name='registrar_presenca_dados_basicos_ajax'),

    path('registro/totais-atividades/', registrar_presenca_totais_atividades, 
         name='registrar_presenca_totais_atividades'),
    path('registro/totais-atividades/ajax/', registrar_presenca_totais_atividades_ajax, 
         name='registrar_presenca_totais_atividades_ajax'),

    path('registro/dias-atividades/', registrar_presenca_dias_atividades, 
         name='registrar_presenca_dias_atividades'),
    path('registro/dias-atividades/ajax/', registrar_presenca_dias_atividades_ajax, 
         name='registrar_presenca_dias_atividades_ajax'),

    path('registro/alunos/', registrar_presenca_alunos, 
         name='registrar_presenca_alunos'),
    path('registro/alunos/ajax/', registrar_presenca_alunos_ajax, 
         name='registrar_presenca_alunos_ajax'),

    path('registro/confirmar/', registrar_presenca_confirmar, 
         name='registrar_presenca_confirmar'),
    path('registro/confirmar/ajax/', registrar_presenca_confirmar_ajax, 
         name='registrar_presenca_confirmar_ajax'),

    # APIs de apoio
    path('ajax/turmas-por-curso/', turmas_por_curso_ajax, 
         name='turmas_por_curso_ajax'),
    path('ajax/atividades-por-turma/', atividades_por_turma_ajax, 
         name='atividades_por_turma_ajax'),
    path('ajax/limites-calendario/', obter_limites_calendario_ajax, 
         name='registrar_presenca_limites_calendario_ajax'),

    # Edição multi-etapas
    path('edicao/<int:presenca_id>/dados-basicos/', editar_presenca_dados_basicos, 
         name='editar_presenca_dados_basicos'),
    path('edicao/<int:presenca_id>/totais-atividades/', editar_presenca_totais_atividades, 
         name='editar_presenca_totais_atividades'),
    path('edicao/<int:presenca_id>/dias-atividades/', editar_presenca_dias_atividades, 
         name='editar_presenca_dias_atividades'),
    path('edicao/<int:presenca_id>/alunos/', editar_presenca_alunos, 
         name='editar_presenca_alunos'),

    # Detalhamento multi-etapas
    path('detalhes/<int:presenca_id>/dados-basicos/', detalhar_presenca_dados_basicos, 
         name='detalhar_presenca_dados_basicos'),
    path('detalhes/<int:presenca_id>/totais-atividades/', detalhar_presenca_totais_atividades, 
         name='detalhar_presenca_totais_atividades'),
    path('detalhes/<int:presenca_id>/dias-atividades/', detalhar_presenca_dias_atividades, 
         name='detalhar_presenca_dias_atividades'),
    path('detalhes/<int:presenca_id>/alunos/', detalhar_presenca_alunos, 
         name='detalhar_presenca_alunos'),
]
