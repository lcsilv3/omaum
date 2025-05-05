from django.urls import path
from . import views
from . import api_views

app_name = 'frequencias'

urlpatterns = [
    # Views principais
    path('', views.listar_frequencias, name='listar_frequencias'),
    path('criar/', views.criar_frequencia_mensal, name='criar_frequencia_mensal'),
    path('editar/<int:frequencia_id>/', views.editar_frequencia_mensal, name='editar_frequencia_mensal'),
    path('excluir/<int:frequencia_id>/', views.excluir_frequencia_mensal, name='excluir_frequencia_mensal'),
    path('detalhar/<int:frequencia_id>/', views.detalhar_frequencia_mensal, name='detalhar_frequencia_mensal'),
    path('recalcular/<int:frequencia_id>/', views.recalcular_carencias, name='recalcular_carencias'),
    
    # Carências
    path('carencias/', views.listar_carencias, name='listar_carencias'),
    path('carencias/editar/<int:carencia_id>/', views.editar_carencia, name='editar_carencia'),
    path('carencias/resolver/<int:carencia_id>/', views.resolver_carencia, name='resolver_carencia'),
    
    # Exportação e relatórios
    path('exportar/<int:frequencia_id>/', views.exportar_frequencia_csv, name='exportar_frequencia_csv'),
    path('painel/', views.painel_frequencias, name='painel_frequencias'),
    path('painel/visualizar/<int:turma_id>/<int:mes_inicio>/<int:ano_inicio>/<int:mes_fim>/<int:ano_fim>/', 
         views.visualizar_painel_frequencias, name='visualizar_painel_frequencias'),
    path('relatorio/', views.relatorio_frequencias, name='relatorio_frequencias'),
    
    # APIs
    path('api/dados-frequencia/<int:frequencia_id>/', api_views.obter_dados_frequencia, name='api_obter_dados_frequencia'),
    path('api/dados-painel-frequencias/', api_views.obter_dados_painel_frequencias, name='api_obter_dados_painel_frequencias'),
]
