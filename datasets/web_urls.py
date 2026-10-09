"""
Datasets Web/HTML Frontend URLs.
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('datasets/', TemplateView.as_view(template_name='datasets/list.html'), name='web_dataset_list'),
    path('datasets/upload/', TemplateView.as_view(template_name='datasets/upload.html'), name='web_dataset_upload'),
    path('datasets/<int:pk>/', TemplateView.as_view(template_name='datasets/detail.html'), name='web_dataset_detail'),
]
