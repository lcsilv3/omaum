from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('lista/', views.lista_presencas, name='lista_presencas'),
]

