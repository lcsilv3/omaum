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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('alunos/', include('alunos.urls', namespace='alunos')),
    path('cursos/', include('cursos.urls', namespace='cursos')),
    path('turmas/', include('turmas.urls', namespace='turmas')),
    path('matriculas/', include('matriculas.urls', namespace='matriculas')),
    path('frequencias/', include('frequencias.urls', namespace='frequencias')),
    path('atividades/', include('atividades.urls', namespace='atividades')),
    path('presencas/', include('presencas.urls', namespace='presencas')),
    path('iniciacoes/', include('iniciacoes.urls', namespace='iniciacoes')),
    path('cargos/', include('cargos.urls', namespace='cargos')),
    path('punicoes/', include('punicoes.urls', namespace='punicoes')),
    path('relatorios/', include('relatorios.urls', namespace='relatorios')),
    path('notas/', include('notas.urls', namespace='notas')),
    path('pagamentos/', include('pagamentos.urls', namespace='pagamentos')),
    # URLs de autenticação do Django
    path('accounts/', include('django.contrib.auth.urls')),
    # Adicionar rota para 'entrar/'
    path('entrar/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Adicionar rota para 'register'
    path('register/', core_views.registro_usuario, name='register'),
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
