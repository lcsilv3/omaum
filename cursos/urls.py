from django.urls import path
from . import views

urlpatterns = [
    path('', views.CursoListView.as_view(), name='curso_list'),
    path('novo/', views.CursoCreateView.as_view(), name='curso_create'),
    path('<str:pk>/editar/', views.CursoUpdateView.as_view(), name='curso_update'),
    path('<str:pk>/excluir/', views.CursoDeleteView.as_view(), name='curso_delete'),
]