"""
Analysis Models: Analysis, AnalysisResult, and StatisticalResult.
"""
from django.db import models
from django.conf import settings
from datasets.models import Dataset

class Analysis(models.Model):
    ANALYSIS_TYPE_CHOICES = [
        ('descriptive', 'Descriptive & Summary Statistics'),
        ('correlation', 'Correlation Matrix & Heatmap'),
        ('outliers', 'Outlier Detection (IQR / Z-Score)'),
        ('regression', 'Regression Analysis (Linear / Multi)'),
        ('classification', 'Classification Model (Decision Tree / Logistic)'),
        ('clustering', 'K-Means Clustering'),
        ('pca', 'Principal Component Analysis (PCA)'),
        ('timeseries', 'Time Series & Trend Analysis'),
        ('data_quality', 'Data Quality & Missing Values Report'),
        ('full_profile', 'Comprehensive Data Profile'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='analyses')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses')
    analysis_type = models.CharField(max_length=30, choices=ANALYSIS_TYPE_CHOICES, default='descriptive')
    parameters_json = models.JSONField(default=dict, blank=True, help_text='Input parameters (e.g. target_column, features, k_clusters)')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_time_seconds = models.FloatField(default=0.0)
    error_message = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.title} ({self.get_analysis_type_display()})"

class AnalysisResult(models.Model):
    analysis = models.OneToOneField(Analysis, on_delete=models.CASCADE, related_name='result')
    summary_metrics_json = models.JSONField(default=dict, blank=True)
    detailed_data_json = models.JSONField(default=dict, blank=True)
    insights_list_json = models.JSONField(default=list, blank=True)
    recommendations_list_json = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Results for: {self.analysis.title}"

class StatisticalResult(models.Model):
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='statistical_results')
    metric_name = models.CharField(max_length=150)
    metric_value = models.FloatField(null=True, blank=True)
    metric_text = models.CharField(max_length=255, blank=True, default='')
    p_value = models.FloatField(null=True, blank=True)
    is_significant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
