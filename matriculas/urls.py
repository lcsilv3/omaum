from django.urls import path
from . import views

app_name = "matriculas"

urlpatterns = [
    path("", views.listar_matriculas, name="listar_matriculas"),
    path(
        "<int:id>/detalhes/",
        views.detalhar_matricula,
        name="detalhar_matricula",
    ),
    path("realizar/", views.realizar_matricula, name="realizar_matricula"),
    path(
        "<int:id>/cancelar/",
        views.cancelar_matricula,
        name="cancelar_matricula",
    ),
]
