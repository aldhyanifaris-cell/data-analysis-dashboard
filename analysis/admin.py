"""
Analysis Admin.
"""
from django.contrib import admin
from .models import Analysis, AnalysisResult, StatisticalResult

class AnalysisResultInline(admin.StackedInline):
    model = AnalysisResult
    can_delete = False

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'dataset', 'analysis_type', 'status', 'execution_time_seconds', 'created_by', 'created_at')
    list_filter = ('analysis_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'dataset__name', 'created_by__email')
    inlines = [AnalysisResultInline]

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('analysis', 'created_at')
