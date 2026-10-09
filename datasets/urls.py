"""
Datasets API URLs.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
]
