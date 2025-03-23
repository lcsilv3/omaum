from django.urls import path
from . import views

app_name = 'professores'

urlpatterns = [
    path('', views.listar_professores, name='listar_professores'),
    path('cadastrar/', views.cadastrar_professor, name='cadastrar_professor'),
    path('<int:professor_id>/', views.detalhes_professor, name='detalhes_professor'),
    path('<int:professor_id>/editar/', views.editar_professor, name='editar_professor'),
    path('<int:professor_id>/excluir/', views.excluir_professor, name='excluir_professor'),
    path('exportar/csv/', views.exportar_professores_csv, name='exportar_professores_csv'),
    path('exportar/pdf/', views.exportar_professores_pdf, name='exportar_professores_pdf'),
]
