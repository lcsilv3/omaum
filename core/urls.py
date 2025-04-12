"""
Core URLs Configuration

Este arquivo define as URLs para o aplicativo 'core' do projeto OMAUM.
Localização: core/urls.py

Uso:
- Define os padrões de URL para as views do aplicativo core.
- Utiliza o namespace 'core' para evitar conflitos de nomes com outros aplicativos.
- É incluído no arquivo de URLs principal do projeto (omaum/urls.py).

As URLs definidas aqui são responsáveis pelas funcionalidades centrais do sistema,
como página inicial, login, logout, painel de controle, etc.

Para incluir estas URLs no arquivo principal, use:
path('', include('core.urls', namespace='core')),
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('entrar/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='entrar'),
    path('sair/', auth_views.LogoutView.as_view(next_page='/'), name='sair'),
    path('painel-controle/', views.painel_controle, name='painel_controle'),
    path('atualizar-configuracao/', views.atualizar_configuracao, name='atualizar_configuracao'),
    path('csrf_check/', views.csrf_check, name='csrf_check'),
    path('dashboard/', views.painel_controle, name='dashboard'),  # Redireciona diretamente para a view
]
