from django.urls import path
from .views_ext.listagem import listar_presencas
from .views_ext.atividade import registrar_presencas_atividade, editar_presenca
from .views_ext.multiplas import registrar_presencas_multiplas, formulario_presencas_multiplas
from . import views

app_name = "presencas"

urlpatterns = [
    # Presenças acadêmicas
    path("academicas/", views.listar_presencas_academicas, name="listar_presencas_academicas"),
    path("academicas/registrar/", views.registrar_presenca_academica, name="registrar_presenca_academica"),
    path("academicas/editar/<int:pk>/", views.editar_presenca_academica, name="editar_presenca_academica"),
    path("academicas/excluir/<int:pk>/", views.excluir_presenca_academica, name="excluir_presenca_academica"),
    path("academicas/detalhar/<int:pk>/", views.detalhar_presenca_academica, name="detalhar_presenca_academica"),
    path("academicas/exportar/", views.exportar_presencas_academicas, name="exportar_presencas_academicas"),
    path(
        "academicas/importar/",
        views.importar_presencas_academicas,
        name="importar_presencas_academicas"
    ),

    # Presenças ritualísticas
    path("ritualisticas/", views.listar_presencas_ritualisticas, name="listar_presencas_ritualisticas"),
    path("ritualisticas/registrar/", views.registrar_presenca_ritualistica, name="registrar_presenca_ritualistica"),
    path("ritualisticas/editar/<int:pk>/", views.editar_presenca_ritualistica, name="editar_presenca_ritualistica"),
    path("ritualisticas/excluir/<int:pk>/", views.excluir_presenca_ritualistica, name="excluir_presenca_ritualistica"),
    path("ritualisticas/detalhar/<int:pk>/", views.detalhar_presenca_ritualistica, name="detalhar_presenca_ritualistica"),
    path("ritualisticas/exportar/", views.exportar_presencas_ritualisticas, name="exportar_presencas_ritualisticas"),
    path(
        "ritualisticas/importar/",
        views.importar_presencas_ritualisticas,
        name="importar_presencas_ritualisticas"
    ),

    # Observações de presença
    path("observacoes/", views.listar_observacoes_presenca, name="listar_observacoes_presenca"),
    
    # Outras rotas dos submódulos, se necessário
    path("multiplas/", registrar_presencas_multiplas, name="registrar_presencas_multiplas"),
    path("multiplas/formulario/", formulario_presencas_multiplas, name="formulario_presencas_multiplas"),
    # etc.
]
