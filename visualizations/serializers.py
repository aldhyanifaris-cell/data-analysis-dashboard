"""
Visualizations Serializers.
"""
from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from datasets.serializers import DatasetListSerializer
from .models import Chart, SavedVisualization

class ChartSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)
    dataset_details = DatasetListSerializer(source='dataset', read_only=True)

    class Meta:
        model = Chart
        fields = [
            'id', 'title', 'description', 'dataset', 'dataset_details',
            'analysis', 'created_by', 'chart_type', 'engine',
            'x_axis', 'y_axis', 'z_axis', 'color_by', 'size_by',
            'config_options_json', 'plotly_json', 'static_image',
            'is_favorite', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'plotly_json', 'static_image']

class SavedVisualizationSerializer(serializers.ModelSerializer):
    chart = ChartSerializer(read_only=True)
    chart_id = serializers.PrimaryKeyRelatedField(queryset=Chart.objects.all(), source='chart', write_only=True)

    class Meta:
        model = SavedVisualization
        fields = ['id', 'user', 'chart', 'chart_id', 'custom_title', 'notes', 'created_at']
        read_only_fields = ['user']
