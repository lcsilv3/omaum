from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "core"

urlpatterns = [
    path("", views.pagina_inicial, name="pagina_inicial"),
    path(
        "entrar/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="entrar",
    ),
    path("sair/", views.sair, name="sair"),
    path("painel-controle/", views.painel_controle, name="painel_controle"),
    path(
        "atualizar-configuracao/",
        views.atualizar_configuracao,
        name="atualizar_configuracao",
    ),
    path("csrf_check/", views.csrf_check, name="csrf_check"),
    path(
        "dashboard/", views.painel_controle, name="dashboard"
    ),  # Redireciona diretamente para a view
]
