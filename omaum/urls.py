from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings  # Adicione esta linha

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alunos/', include('alunos.urls')),
    path('atividades/', include('atividades.urls')),
    path('cargos/', include('cargos.urls')),
    path('core/', include('core.urls')),
    path('cursos/', include('cursos.urls')),
    path('frequencias/', include('frequencias.urls')),
    path('iniciacoes/', include('iniciacoes.urls')),
    path('presencas/', include('presencas.urls')),
    path('professores/', include('professores.urls')),
    path('punicoes/', include('punicoes.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('turmas/', include('turmas.urls')),
    path('', RedirectView.as_view(pattern_name='core:pagina_inicial'), name='home'),
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

# Adicione este bloco no final do arquivo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
