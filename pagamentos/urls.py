from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('', views.listar_pagamentos, name='listar_pagamentos'),
]
