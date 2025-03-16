from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_iniciacoes, name='listar_iniciacoes'),
    path('criar/', views.criar_iniciacao, name='criar_iniciacao'),
    path('<int:id>/', views.detalhe_iniciacao, name='detalhe_iniciacao'),
    path('<int:id>/editar/', views.editar_iniciacao, name='editar_iniciacao'),
    path('<int:id>/excluir/', views.excluir_iniciacao, name='excluir_iniciacao'),
]
