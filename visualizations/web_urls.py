"""
Visualizations Web URLs.
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='visualizations/list.html'), name='web_chart_list'),
    path('<int:pk>/', TemplateView.as_view(template_name='visualizations/detail.html'), name='web_chart_detail'),
]
