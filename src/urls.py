from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import index


urlpatterns = [
    path('', index, name='index'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]

if settings.ENVIRONMENT != 'production':
    schema_view = get_schema_view(
        openapi.Info(
            title='PhotoHub',
            default_version='v1',
            description='API',
        ),
        url='',
        public=True,
        permission_classes=[permissions.AllowAny],
    )
    urlpatterns = [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
