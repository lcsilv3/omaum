from django.urls import path
from . import views

app_name = 'iniciacoes'

urlpatterns = [
    path('', views.listar_iniciacoes, name='listar_iniciacoes'),
    path('nova/', views.criar_iniciacao, name='criar_iniciacao'),
    path('<int:id>/editar/', views.editar_iniciacao, name='editar_iniciacao'),
    path('<int:id>/excluir/', views.excluir_iniciacao, name='excluir_iniciacao'),
    path('<int:id>/detalhes/', views.detalhe_iniciacao, name='detalhe_iniciacao'),
]
