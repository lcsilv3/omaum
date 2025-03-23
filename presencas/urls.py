from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('lista/', views.lista_presencas, name='lista_presencas'),
    path('editar/<int:id>/', views.editar_presenca, name='editar_presenca'),
    path('excluir/<int:id>/', views.excluir_presenca, name='excluir_presenca'),
]
