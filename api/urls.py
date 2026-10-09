"""
API URLs.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.APIRootView.as_view(), name='api_root'),
    path('system-stats/', views.SystemStatsView.as_view(), name='system_stats'),
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
]
