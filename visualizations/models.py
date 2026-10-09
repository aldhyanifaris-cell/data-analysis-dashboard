"""
Visualizations Models: Chart, ChartConfig, and SavedVisualization.
"""
from django.db import models
from django.conf import settings
from datasets.models import Dataset
from analysis.models import Analysis

class Chart(models.Model):
    CHART_TYPE_CHOICES = [
        ('line', 'Line Chart (Trend / Time-series)'),
        ('bar', 'Bar Chart (Categorical Comparison)'),
        ('scatter', 'Scatter Plot (2D Relationship)'),
        ('scatter3d', '3D Scatter Plot (3 Variables)'),
        ('histogram', 'Histogram (Distribution)'),
        ('box', 'Box Plot (Spread & Outliers)'),
        ('violin', 'Violin Plot (Density & Distribution)'),
        ('heatmap', 'Correlation / 2D Heatmap'),
        ('pie', 'Pie / Donut Chart (Proportions)'),
        ('treemap', 'Treemap (Hierarchical)'),
        ('bubble', 'Bubble Chart (3D Dimensions on 2D)'),
        ('density', 'Density Contour Plot'),
    ]

    ENGINE_CHOICES = [
        ('plotly', 'Plotly (Interactive JS)'),
        ('matplotlib', 'Matplotlib (Static High-Res)'),
        ('seaborn', 'Seaborn (Statistical Graphics)'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='charts')
    analysis = models.ForeignKey(Analysis, on_delete=models.SET_NULL, null=True, blank=True, related_name='charts')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='charts')

    chart_type = models.CharField(max_length=30, choices=CHART_TYPE_CHOICES, default='bar')
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES, default='plotly')

    # Dimensions configuration
    x_axis = models.CharField(max_length=100, blank=True, default='')
    y_axis = models.CharField(max_length=100, blank=True, default='')
    z_axis = models.CharField(max_length=100, blank=True, default='', help_text='For 3D plots')
    color_by = models.CharField(max_length=100, blank=True, default='', help_text='Category or metric for coloring')
    size_by = models.CharField(max_length=100, blank=True, default='', help_text='For bubble charts')

    config_options_json = models.JSONField(default=dict, blank=True)
    plotly_json = models.JSONField(default=dict, blank=True, help_text='Generated Plotly figure specification')
    static_image = models.ImageField(upload_to='visualizations/', null=True, blank=True)

    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.title} ({self.get_chart_type_display()})"

class SavedVisualization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_visualizations')
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name='saved_instances')
    custom_title = models.CharField(max_length=255, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
