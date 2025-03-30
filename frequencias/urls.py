from django.urls import path
from . import views

app_name = 'frequencias'

urlpatterns = [
    path('', views.listar_frequencias, name='listar_frequencias'),
    path('registrar/', views.registrar_frequencia, name='registrar_frequencia'),
    path('<int:id>/editar/', views.editar_frequencia, name='editar_frequencia'),
    path('<int:id>/excluir/', views.excluir_frequencia, name='excluir_frequencia'),
    path('<int:id>/detalhes/', views.detalhar_frequencia, name='detalhar_frequencia'),
    path('relatorio/', views.relatorio_frequencias, name='relatorio_frequencias'),
    path('exportar/', views.exportar_frequencias, name='exportar_frequencias'),
]
