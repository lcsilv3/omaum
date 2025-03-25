from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('academicas/', views.atividade_academica_list, name='atividade_academica_list'),
    # Other URL patterns...
]