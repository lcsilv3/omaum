"""
Configuração de URLs do projeto OMAUM.
A lista `urlpatterns` roteia URLs para views. Para mais informações, consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("alunos/", include("alunos.urls")),
    path("cursos/", include("cursos.urls")),
    path("turmas/", include("turmas.urls")),
    path("matriculas/", include("matriculas.urls")),
    path("frequencias/", include("frequencias.urls")),
    path("atividades/", include("atividades.urls")),
    path("presencas/", include("presencas.urls")),
    path(
        "relatorios-presenca/",
        include("relatorios_presenca.urls"),
    ),
    path("notas/", include("notas.urls")),
    path("pagamentos/", include("pagamentos.urls")),
    # URLs de autenticação do Django
    path("accounts/login/", core_views.CustomLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    # Adicionar rota para 'entrar/' (opcional, pode apontar para CustomLoginView também)
    path("entrar/", core_views.CustomLoginView.as_view(), name="entrar"),
    # Adicionar rota para 'register'
    path("register/", core_views.registro_usuario, name="register"),
    # Rota do django-select2 para widgets AJAX
    path("select2/", include("django_select2.urls")),
]

# Configurações para ambiente de desenvolvimento
if settings.DEBUG:
    # Servir arquivos de mídia em desenvolvimento
    # Servir arquivos de mídia em desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
