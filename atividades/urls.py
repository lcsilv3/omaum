from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    # URLs para Atividades Acadêmicas
    path('academicas/', views.AcademicaListaView.as_view(), name='academica_lista'),
    path('academicas/criar/', views.AcademicaCriarView.as_view(), name='academica_criar'),
    path('academicas/<int:pk>/editar/', views.AcademicaEditarView.as_view(), name='academica_editar'),
    path('academicas/<int:pk>/excluir/', views.AcademicaExcluirView.as_view(), name='academica_excluir'),
    
    # URLs para Atividades Ritualísticas
    path('ritualisticas/', views.RitualisticaListaView.as_view(), name='ritualistica_lista'),
    path('ritualisticas/criar/', views.RitualisticaCriarView.as_view(), name='ritualistica_criar'),
    path('ritualisticas/<int:pk>/editar/', views.RitualisticaEditarView.as_view(), name='ritualistica_editar'),
    path('ritualisticas/<int:pk>/excluir/', views.RitualisticaExcluirView.as_view(), name='ritualistica_excluir'),
]