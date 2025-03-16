from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from core import views as core_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('atividades/', include('atividades.urls')),
    path('', include('core.urls')),
]

urlpatterns += [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

urlpatterns += i18n_patterns(
    # Apps
    path('alunos/', include('alunos.urls')),
    path('cursos/', include('cursos.urls')),
    path('turmas/', include('turmas.urls')),
    path('presencas/', include('presencas.urls')),
    path('cargos/', include('cargos.urls')),
    path('relatorios/', include('relatorios.urls')),

    # Authentication
    path('accounts/', include([
        path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
        path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ])),
    prefix_default_language=False
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Adicione quaisquer configurações específicas de produção aqui
    pass

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'

# Configurações de segurança adicionais
from django.views.decorators.cache import cache_page
from django.views.decorators.clickjacking import xframe_options_exempt

# Exemplo de como aplicar cache a uma view específica
# urlpatterns += [path('cached-view/', cache_page(60 * 15)(core_views.cached_view), name='cached_view')]

# Exemplo de como permitir que uma view específica seja carregada em um iframe
# urlpatterns += [path('iframe-view/', xframe_options_exempt(core_views.iframe_view), name='iframe_view')]
