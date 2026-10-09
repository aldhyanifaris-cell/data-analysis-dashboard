"""
Visualizations Admin.
"""
from django.contrib import admin
from .models import Chart, SavedVisualization

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'dataset', 'chart_type', 'engine', 'created_by', 'is_favorite', 'created_at')
    list_filter = ('chart_type', 'engine', 'is_favorite', 'created_at')
    search_fields = ('title', 'description', 'dataset__name', 'created_by__email')

@admin.register(SavedVisualization)
class SavedVisualizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'chart', 'custom_title', 'created_at')
