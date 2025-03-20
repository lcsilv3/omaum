from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('atividades/', include('atividades.urls')),
    path('turmas/', include('turmas.urls')),
    path('alunos/', include('alunos.urls')),
    path('presencas/', include('presencas.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('cargos/', include('cargos.urls')),
    path('', RedirectView.as_view(pattern_name='turmas:listar_turmas'), name='home'),
]

# URLs de autenticação
urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
from django.urls import path
from .views import RegisterView

urlpatterns += [
    path('accounts/registro/', RegisterView.as_view(), name='registro'),
]
