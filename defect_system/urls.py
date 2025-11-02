from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Аутентификация с явным указанием шаблонов
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html',
        next_page='/accounts/login/'
    ), name='logout'),

    # Приложения
    path('defects/', include('defects.urls')),
    path('projects/', include('projects.urls')),
    path('reports/', include('reports.urls')),
    path('users/', include('users.urls')),

    # Перенаправление корня на дефекты
    path('', include('defects.urls')),
]

# Правильное добавление статических файлов - БЕЗ дублирования
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)