from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('painel-controle/', views.painel_controle, name='painel_controle'),
    path('atualizar-configuracao/', views.atualizar_configuracao, name='atualizar_configuracao'),
    path('csrf_check/', views.csrf_check, name='csrf_check'),
]