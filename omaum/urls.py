"""
Configuração de URLs do projeto OMAUM.

A lista `urlpatterns` roteia URLs para views. Para mais informações, consulte:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("alunos/", include("alunos.urls", namespace="alunos")),
    path("atividades/", include("atividades.urls", namespace="atividades")),
    path("cargos/", include("cargos.urls", namespace="cargos")),
    path("cursos/", include("cursos.urls", namespace="cursos")),
    path("frequencias/", include("frequencias.urls", namespace="frequencias")),
    path("iniciacoes/", include("iniciacoes.urls", namespace="iniciacoes")),
    path("matriculas/", include("matriculas.urls", namespace="matriculas")),
    path("notas/", include("notas.urls", namespace="notas")),
    path("pagamentos/", include("pagamentos.urls", namespace="pagamentos")),
    path("presencas/", include("presencas.urls", namespace="presencas")),
    path("punicoes/", include("punicoes.urls", namespace="punicoes")),
    path("relatorios/", include("relatorios.urls", namespace="relatorios")),
    path("turmas/", include("turmas.urls", namespace="turmas")),
    # URLs de autenticação do Django
    path('accounts/', include('django.contrib.auth.urls')),
]

# Configurações para ambiente de desenvolvimento
if settings.DEBUG:
    # Adicionar URLs do Django Debug Toolbar
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    # Servir arquivos de mídia em desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
