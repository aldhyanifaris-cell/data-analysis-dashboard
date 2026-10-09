"""
Analysis Serializers.
"""
from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from datasets.serializers import DatasetListSerializer
from .models import Analysis, AnalysisResult, StatisticalResult

class StatisticalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticalResult
        fields = '__all__'

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = '__all__'

class AnalysisSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)
    result = AnalysisResultSerializer(read_only=True)
    statistical_results = StatisticalResultSerializer(many=True, read_only=True)
    dataset_details = DatasetListSerializer(source='dataset', read_only=True)

    class Meta:
        model = Analysis
        fields = [
            'id', 'title', 'description', 'dataset', 'dataset_details',
            'analysis_type', 'parameters_json', 'status',
            'execution_time_seconds', 'error_message', 'created_by',
            'result', 'statistical_results', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'execution_time_seconds', 'error_message', 'created_by']
