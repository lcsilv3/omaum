from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alunos/', include('alunos.urls')),
    path('turmas/', include('turmas.urls')),
    path('atividades/', include('atividades.urls')),
    path('frequencias/', include('frequencias.urls')),
    path('presencas/', include('presencas.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('cargos/', include('cargos.urls')),
    path('iniciacoes/', include('iniciacoes.urls')),
    path('punicoes/', include('punicoes.urls')),
    path('cursos/', include('cursos.urls')),
    path('professores/', include('professores.urls')),
    path('home/', include('home.urls')),
    path('', RedirectView.as_view(pattern_name='home'), name='root'),
]
