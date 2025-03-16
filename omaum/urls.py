from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('atividades/', include('atividades.urls')),
    path('', RedirectView.as_view(pattern_name='atividades:atividade_academica_list'), name='home'),
    # Other URL patterns
]

# Add these imports at the top if they're not already there
from django.contrib.auth import views as auth_views

# Add these URL patterns to your urlpatterns list
urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
