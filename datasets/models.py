"""
Datasets Models: Dataset, DataColumn, DataSample, DatasetShare, and DataFilter.
"""
import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def dataset_upload_path(instance, filename):
    return os.path.join('uploads', f"user_{instance.owner.id}", filename)

class Dataset(models.Model):
    FORMAT_CHOICES = [
        ('csv', 'CSV (Comma Separated Values)'),
        ('xlsx', 'Excel (XLSX)'),
        ('xls', 'Excel (XLS)'),
        ('json', 'JSON (JavaScript Object Notation)'),
        ('parquet', 'Apache Parquet'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Processing'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Analysis'),
        ('failed', 'Processing Failed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    file = models.FileField(upload_to=dataset_upload_path)
    file_format = models.CharField(max_length=15, choices=FORMAT_CHOICES, default='csv')
    file_size_bytes = models.BigIntegerField(default=0)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='datasets')
    is_public = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, default='')

    # Metadata extracted by engine
    row_count = models.PositiveIntegerField(default=0)
    column_count = models.PositiveIntegerField(default=0)
    missing_cells_count = models.PositiveIntegerField(default=0)
    missing_cells_percentage = models.FloatField(default=0.0)
    duplicate_rows_count = models.PositiveIntegerField(default=0)
    memory_usage_bytes = models.BigIntegerField(default=0)

    tags = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated tags')
    is_favorite = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['is_public']),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.row_count} rows, {self.column_count} cols)"

    @property
    def formatted_size(self) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size_bytes < 1024.0:
                return f"{self.file_size_bytes:.1f} {unit}"
            self.file_size_bytes /= 1024.0
        return f"{self.file_size_bytes:.1f} TB"

class DataColumn(models.Model):
    DATA_TYPE_CHOICES = [
        ('numeric', 'Numeric (Continuous/Discrete)'),
        ('categorical', 'Categorical (String/Object)'),
        ('datetime', 'Datetime / Timestamp'),
        ('boolean', 'Boolean (True/False)'),
        ('text', 'Free Text'),
        ('unknown', 'Unknown / Mixed'),
    ]

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, default='unknown')
    raw_dtype = models.CharField(max_length=50, blank=True, default='')
    column_index = models.PositiveIntegerField(default=0)

    # Statistical properties
    null_count = models.PositiveIntegerField(default=0)
    null_percentage = models.FloatField(default=0.0)
    unique_count = models.PositiveIntegerField(default=0)
    unique_percentage = models.FloatField(default=0.0)

    # For numeric columns
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    mean_value = models.FloatField(null=True, blank=True)
    median_value = models.FloatField(null=True, blank=True)
    std_dev = models.FloatField(null=True, blank=True)
    skewness = models.FloatField(null=True, blank=True)
    kurtosis = models.FloatField(null=True, blank=True)

    # For categorical columns (top values stored as JSON)
    top_values_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['column_index']
        unique_together = ('dataset', 'name')

    def __str__(self) -> str:
        return f"{self.dataset.name} -> {self.name} ({self.data_type})"

class DataSample(models.Model):
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name='sample_data')
    head_rows_json = models.JSONField(default=list, blank=True, help_text='First 20 rows of the dataset')
    tail_rows_json = models.JSONField(default=list, blank=True, help_text='Last 20 rows of the dataset')
    random_sample_json = models.JSONField(default=list, blank=True, help_text='Random 20 rows sample')

    def __str__(self) -> str:
        return f"Samples for {self.dataset.name}"

class DatasetShare(models.Model):
    PERMISSION_CHOICES = [('view', 'Can View & Analyze'), ('edit', 'Can Edit & Export')]
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='shares')
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_datasets')
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='view')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dataset', 'shared_with')

class DataFilter(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='filters')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='data_filters')
    name = models.CharField(max_length=150)
    filter_rules_json = models.JSONField(default=dict, help_text='Structured filtering criteria')
    applied_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Filter '{self.name}' on {self.dataset.name}"
