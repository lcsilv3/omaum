from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('alunos/', include('alunos.urls')),
    path('atividades/', include('atividades.urls')),
    path('turmas/', include('turmas.urls')),
    path('presencas/', include('presencas.urls')),
    path('relatorios/', include('relatorios.urls')),
    # Add other apps here
]

from django.contrib.auth import views as auth_views
urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
