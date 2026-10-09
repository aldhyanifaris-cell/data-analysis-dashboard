"""
Datasets Admin.
"""
from django.contrib import admin
from .models import Dataset, DataColumn, DataSample, DatasetShare, DataFilter

class DataColumnInline(admin.TabularInline):
    model = DataColumn
    extra = 0
    readonly_fields = ('name', 'data_type', 'raw_dtype', 'null_count', 'unique_count', 'mean_value')

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'file_format', 'formatted_size', 'row_count', 'column_count', 'status', 'is_public', 'created_at')
    list_filter = ('file_format', 'status', 'is_public', 'is_favorite', 'created_at')
    search_fields = ('name', 'description', 'tags', 'owner__email', 'owner__username')
    readonly_fields = ('row_count', 'column_count', 'missing_cells_count', 'missing_cells_percentage', 'duplicate_rows_count', 'memory_usage_bytes', 'created_at', 'updated_at')
    inlines = [DataColumnInline]

@admin.register(DataColumn)
class DataColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'dataset', 'data_type', 'null_count', 'unique_count', 'mean_value')
    list_filter = ('data_type', 'dataset')
    search_fields = ('name', 'dataset__name')

@admin.register(DataFilter)
class DataFilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'dataset', 'created_by', 'applied_count', 'created_at')
