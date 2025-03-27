from django.urls import path
from . import views

app_name = 'punicoes'

urlpatterns = [
    path('', views.listar_punicoes, name='listar_punicoes'),
    path('nova/', views.criar_punicao, name='criar_punicao'),
    path('<int:id>/editar/', views.editar_punicao, name='editar_punicao'),
    path('<int:id>/excluir/', views.excluir_punicao, name='excluir_punicao'),
    path('<int:id>/detalhes/', views.detalhe_punicao, name='detalhe_punicao'),
]
