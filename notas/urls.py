from django.urls import path
from . import views

app_name = "notas"

urlpatterns = [
    path("", views.listar_notas, name="listar_notas"),
    path("<int:nota_id>/", views.detalhar_nota, name="detalhar_nota"),
    path("criar/", views.criar_nota, name="criar_nota"),
    path("<int:nota_id>/editar/", views.editar_nota, name="editar_nota"),
    path("<int:nota_id>/excluir/", views.excluir_nota, name="excluir_nota"),
    path("exportar/csv/", views.exportar_notas_csv, name="exportar_notas_csv"),
    path("exportar/excel/", views.exportar_notas_excel, name="exportar_notas_excel"),
    path("dashboard/", views.dashboard_notas, name="dashboard_notas"),
]
