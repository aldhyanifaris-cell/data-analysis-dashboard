"""
Datasets Serializers.
"""
from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from .models import Dataset, DataColumn, DataSample, DatasetShare, DataFilter

class DataColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataColumn
        fields = '__all__'

class DataSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSample
        fields = ['head_rows_json', 'tail_rows_json', 'random_sample_json']

class DatasetListSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    formatted_size = serializers.ReadOnlyField()

    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'description', 'file_format', 'file_size_bytes',
            'formatted_size', 'row_count', 'column_count', 'status',
            'missing_cells_percentage', 'is_public', 'is_favorite',
            'owner', 'tags', 'created_at', 'updated_at'
        ]

class DatasetDetailSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)
    columns = DataColumnSerializer(many=True, read_only=True)
    sample_data = DataSampleSerializer(read_only=True)
    formatted_size = serializers.ReadOnlyField()

    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'description', 'file', 'file_format',
            'file_size_bytes', 'formatted_size', 'row_count',
            'column_count', 'missing_cells_count', 'missing_cells_percentage',
            'duplicate_rows_count', 'memory_usage_bytes', 'status',
            'error_message', 'is_public', 'is_favorite', 'tags',
            'owner', 'columns', 'sample_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'file_size_bytes', 'row_count', 'column_count', 'status', 'error_message']

class DatasetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description', 'file', 'file_format', 'is_public', 'tags']

    def validate_file(self, value):
        valid_extensions = ['.csv', '.xlsx', '.xls', '.json', '.parquet', '.txt']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(f"Unsupported file format '{ext}'. Allowed: {', '.join(valid_extensions)}")
        return value

class DataFilterSerializer(serializers.ModelSerializer):
    created_by = UserPublicSerializer(read_only=True)

    class Meta:
        model = DataFilter
        fields = '__all__'
        read_only_fields = ['created_by', 'applied_count']
