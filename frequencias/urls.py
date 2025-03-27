from django.urls import path
from . import views

app_name = 'frequencias'

urlpatterns = [
    path('', views.listar_frequencias, name='listar_frequencias'),
    path('nova/', views.criar_frequencia, name='criar_frequencia'),
    path('<int:id>/editar/', views.editar_frequencia, name='editar_frequencia'),
    path('<int:id>/excluir/', views.excluir_frequencia, name='excluir_frequencia'),
    path('<int:id>/detalhes/', views.detalhe_frequencia, name='detalhe_frequencia'),
]
