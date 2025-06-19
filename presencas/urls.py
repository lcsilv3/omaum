from django.urls import path
from .views_ext.listagem import listar_presencas
from .views_ext.atividade import registrar_presencas_atividade, editar_presenca
from .views_ext.multiplas import registrar_presencas_multiplas, formulario_presencas_multiplas
from . import views
from importlib import import_module

registro_presenca_views = import_module('presencas.views_ext.registro_presenca')

app_name = "presencas"

urlpatterns = [
    # Presenças acadêmicas
    path("academicas/", views.listar_presencas_academicas, name="listar_presencas_academicas"),
    path("academicas/registrar/", views.registrar_presenca_academica, name="registrar_presenca_academica"),
    path("academicas/editar/<int:pk>/", views.editar_presenca_academica, name="editar_presenca_academica"),
    path("academicas/excluir/<int:pk>/", views.excluir_presenca_academica, name="excluir_presenca_academica"),
    path("academicas/detalhar/<int:pk>/", views.detalhar_presenca_academica, name="detalhar_presenca_academica"),
    path("academicas/exportar/", views.exportar_presencas_academicas, name="exportar_presencas_academicas"),
    path("academicas/importar/", views.importar_presencas_academicas, name="importar_presencas_academicas"),

    # Presenças ritualísticas
    path("ritualisticas/", views.listar_presencas_ritualisticas, name="listar_presencas_ritualisticas"),
    path("ritualisticas/registrar/", views.registrar_presenca_ritualistica, name="registrar_presenca_ritualistica"),
    path("ritualisticas/editar/<int:pk>/", views.editar_presenca_ritualistica, name="editar_presenca_ritualistica"),
    path("ritualisticas/excluir/<int:pk>/", views.excluir_presenca_ritualistica, name="excluir_presenca_ritualistica"),
    path("ritualisticas/detalhar/<int:pk>/", views.detalhar_presenca_ritualistica, name="detalhar_presenca_ritualistica"),
    path("ritualisticas/exportar/", views.exportar_presencas_ritualisticas, name="exportar_presencas_ritualisticas"),
    path("ritualisticas/importar/", views.importar_presencas_ritualisticas, name="importar_presencas_ritualisticas"),

    # Observações de presença
    path("observacoes/", views.listar_observacoes_presenca, name="listar_observacoes_presenca"),

    # Outras rotas dos submódulos, se necessário
    path("multiplas/", registrar_presencas_multiplas, name="registrar_presencas_multiplas"),
    path("multiplas/formulario/", formulario_presencas_multiplas, name="formulario_presencas_multiplas"),

    # Registro de presença - dados básicos
    path('registrar-presenca/dados-basicos/', registro_presenca_views.registrar_presenca_dados_basicos, name='registrar_presenca_dados_basicos'),
    path('registrar-presenca/dados-basicos/ajax/', registro_presenca_views.registrar_presenca_dados_basicos_ajax, name='registrar_presenca_dados_basicos_ajax'),

    # Registro de presença - totais por atividades
    path('registrar-presenca/totais-atividades/', registro_presenca_views.registrar_presenca_totais_atividades, name='registrar_presenca_totais_atividades'),
    path('registrar-presenca/totais-atividades/ajax/', registro_presenca_views.registrar_presenca_totais_atividades_ajax, name='registrar_presenca_totais_atividades_ajax'),

    # Registro de presença - dias/atividades (GET e POST)
    path('registrar-presenca/dias-atividades/', registro_presenca_views.registrar_presenca_dias_atividades, name='registrar_presenca_dias_atividades'),
    path('registrar-presenca/dias-atividades/ajax/', registro_presenca_views.registrar_presenca_dias_atividades_ajax, name='registrar_presenca_dias_atividades_ajax'),

    # Registro de presença - alunos
    path('registrar-presenca/alunos/', registro_presenca_views.registrar_presenca_alunos, name='registrar_presenca_alunos'),
    path('registrar-presenca/alunos/ajax/', registro_presenca_views.registrar_presenca_alunos_ajax, name='registrar_presenca_alunos_ajax'),

    # Confirmação de registro de presença
    path('registrar-presenca/confirmar/', registro_presenca_views.registrar_presenca_confirmar, name='registrar_presenca_confirmar'),
    path('registrar-presenca/confirmar/ajax/', registro_presenca_views.registrar_presenca_confirmar_ajax, name='registrar_presenca_confirmar_ajax'),

    # Turmas por curso - AJAX
    path('registrar-presenca/turmas-por-curso/', registro_presenca_views.turmas_por_curso_ajax, name='turmas_por_curso_ajax'),
    path('registrar-presenca/atividades-por-turma/', registro_presenca_views.atividades_por_turma_ajax, name='atividades_por_turma_ajax'),

    # Limites do calendário - AJAX
    path('registrar-presenca/limites-calendario/', registro_presenca_views.obter_limites_calendario_ajax, name='registrar_presenca_limites_calendario_ajax'),
]
