"""
Analysis Web URLs.
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard.html'), name='web_dashboard'),
    path('analyses/', TemplateView.as_view(template_name='analysis/list.html'), name='web_analysis_list'),
    path('analyses/<int:pk>/', TemplateView.as_view(template_name='analysis/detail.html'), name='web_analysis_detail'),
]
