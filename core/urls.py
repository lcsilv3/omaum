from .views import home
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from .api_views import ConfiguracaoSistemaViewSet, LogAtividadeViewSet

app_name = "core"

# API Router
router = DefaultRouter()
router.register(r"api/configuracoes", ConfiguracaoSistemaViewSet)
router.register(r"api/logs", LogAtividadeViewSet)

urlpatterns = [
    path("", views.pagina_inicial, name="home"),
    path("pagina-inicial/", views.pagina_inicial, name="pagina_inicial"),
    path("home/", home, name="home_minimal"),
    # API URLs
    path("api/", include(router.urls)),
    # Template URLs
    path("inicio/", views.pagina_inicial, name="pagina_inicial_alt"),
    path("perfil/", views.perfil, name="perfil"),
    path(
        "alterar-senha/",
        auth_views.PasswordChangeView.as_view(
            template_name="core/alterar_senha.html", success_url="/core/senha-alterada/"
        ),
        name="alterar_senha",
    ),
    path(
        "senha-alterada/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="core/senha_alterada.html"
        ),
        name="senha_alterada",
    ),
    path("sair/", auth_views.LogoutView.as_view(next_page="/"), name="sair"),
    path("entrar/", views.CustomLoginView.as_view(), name="entrar"),
    path("painel-controle/", views.painel_controle, name="painel_controle"),
    path("configuracoes/", views.configuracoes, name="configuracoes"),
    path(
        "atualizar-configuracao/",
        views.atualizar_configuracao,
        name="atualizar_configuracao",
    ),
    path("csrf_check/", views.csrf_check, name="csrf_check"),
    path("dashboard/", views.painel_controle, name="dashboard"),
]
