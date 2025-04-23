from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static  # Adicione esta importação

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("alunos/", include("alunos.urls")),
    path("atividades/", include("atividades.urls")),
    path("cargos/", include("cargos.urls")),
    path("cursos/", include("cursos.urls")),
    path("frequencias/", include("frequencias.urls")),
    path("iniciacoes/", include("iniciacoes.urls")),
    path("presencas/", include("presencas.urls")),
    path("punicoes/", include("punicoes.urls")),
    path("relatorios/", include("relatorios.urls", namespace="relatorios")),
    path("turmas/", include("turmas.urls")),
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
]

# Adicione este bloco no final do arquivo
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    # Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)