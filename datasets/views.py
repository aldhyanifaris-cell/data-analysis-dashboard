"""
Datasets API Views.
"""
import os
from django.db.models import Q
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Dataset, DataColumn, DataSample, DataFilter
from .serializers import (
    DatasetListSerializer,
    DatasetDetailSerializer,
    DatasetUploadSerializer,
    DataColumnSerializer,
    DataFilterSerializer,
)
from .permissions import IsDatasetOwnerOrSharedOrPublic
from .filters import DatasetFilter
from .utils import load_dataframe_from_file, profile_and_extract_metadata

class DatasetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsDatasetOwnerOrSharedOrPublic]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DatasetFilter
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['created_at', 'row_count', 'file_size_bytes', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Dataset.objects.filter(is_public=True)
        return Dataset.objects.filter(
            Q(owner=user) | Q(is_public=True) | Q(shares__shared_with=user)
        ).distinct().select_related('owner')

    def get_serializer_class(self):
        if self.action == 'create':
            return DatasetUploadSerializer
        elif self.action == 'list':
            return DatasetListSerializer
        return DatasetDetailSerializer

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('file')
        file_size = uploaded_file.size if uploaded_file else 0
        name = serializer.validated_data.get('name') or uploaded_file.name
        ext = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')
        
        dataset = serializer.save(
            owner=self.request.user,
            name=name,
            file_size_bytes=file_size,
            file_format=ext if ext in ['csv', 'xlsx', 'xls', 'json', 'parquet'] else 'csv',
            status='processing'
        )

        # Process and profile dataset synchronously / async ready
        try:
            df = load_dataframe_from_file(dataset.file.path, dataset.file_format)
            dataset_meta, columns_meta, sample_meta = profile_and_extract_metadata(df)

            for key, val in dataset_meta.items():
                setattr(dataset, key, val)
            dataset.status = 'ready'
            dataset.save()

            # Create columns
            DataColumn.objects.filter(dataset=dataset).delete()
            for col_info in columns_meta:
                DataColumn.objects.create(dataset=dataset, **col_info)

            # Create samples
            DataSample.objects.update_or_create(
                dataset=dataset,
                defaults=sample_meta
            )

            # Increment user stats
            if hasattr(self.request.user, 'profile'):
                self.request.user.profile.total_datasets_uploaded += 1
                self.request.user.profile.save()

        except Exception as e:
            dataset.status = 'failed'
            dataset.error_message = str(e)
            dataset.save()

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        dataset = self.get_object()
        limit = int(request.query_params.get('limit', 50))
        try:
            df = load_dataframe_from_file(dataset.file.path, dataset.file_format)
            clean_df = df.fillna("")
            return Response({
                'dataset_id': dataset.id,
                'name': dataset.name,
                'total_rows': dataset.row_count,
                'total_columns': dataset.column_count,
                'columns': list(df.columns),
                'rows': clean_df.head(limit).to_dict(orient='records'),
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def columns(self, request, pk=None):
        dataset = self.get_object()
        columns = dataset.columns.all()
        serializer = DataColumnSerializer(columns, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        dataset = self.get_object()
        dataset.is_favorite = not dataset.is_favorite
        dataset.save(update_fields=['is_favorite'])
        return Response({'status': 'success', 'is_favorite': dataset.is_favorite})
