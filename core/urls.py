from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/<int:aluno_id>/', views.detalhe_aluno, name='detalhe_aluno'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:categoria_id>/', views.detalhe_categoria, name='detalhe_categoria'),
    path('itens/', views.lista_itens, name='lista_itens'),
    path('itens/<int:item_id>/', views.detalhe_item, name='detalhe_item'),
    path('atividades/', views.academica_lista, name='academica_lista'),
    path('atividades/<int:atividade_id>/', views.academica_detalhe, name='academica_detalhe'),
    path('atividades/ritualistica/', views.ritualistica_lista, name='ritualistica_lista'),
    path('atividades/ritualistica/<int:atividade_id>/', views.ritualistica_detalhe, name='ritualistica_detalhe'),
]