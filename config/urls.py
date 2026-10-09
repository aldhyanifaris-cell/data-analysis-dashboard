"""
Root URL Configuration for Data Analysis Dashboard.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

admin.site.site_header = "Data Analysis Dashboard Admin"
admin.site.site_title = "Data Analysis Admin"
admin.site.index_title = "Dashboard Management Portal"

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Web Dashboard Views (HTML)
    path('', include('datasets.web_urls')),
    path('dashboard/', include('analysis.web_urls')),
    path('charts/', include('visualizations.web_urls')),
    path('accounts/', include('accounts.web_urls')),

    # REST API v1
    path('api/v1/', include([
        path('auth/', include([
            path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
            path('', include('accounts.urls')),
        ])),
        path('datasets/', include('datasets.urls')),
        path('analysis/', include('analysis.urls')),
        path('visualizations/', include('visualizations.urls')),
        path('', include('api.urls')),
    ])),

    # DRF browsable API auth
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
