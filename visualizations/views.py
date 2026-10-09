"""
Visualizations API Views.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.files.base import ContentFile

from datasets.models import Dataset
from datasets.utils import load_dataframe_from_file
from .models import Chart, SavedVisualization
from .serializers import ChartSerializer, SavedVisualizationSerializer
from .generator import ChartGenerator

class ChartViewSet(viewsets.ModelViewSet):
    serializer_class = ChartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chart.objects.filter(
            models.Q(created_by=user) | models.Q(dataset__owner=user) | models.Q(dataset__is_public=True)
        ).distinct().select_related('created_by', 'dataset')

    def perform_create(self, serializer):
        chart = serializer.save(created_by=self.request.user)
        self._generate_chart_data(chart)

    def _generate_chart_data(self, chart: Chart):
        try:
            dataset = chart.dataset
            df = load_dataframe_from_file(dataset.file.path, dataset.file_format)
            generator = ChartGenerator(df)

            # Generate Plotly JSON spec
            plotly_spec = generator.generate_plotly_spec(
                chart_type=chart.chart_type,
                x=chart.x_axis or None,
                y=chart.y_axis or None,
                z=chart.z_axis or None,
                color=chart.color_by or None,
                size=chart.size_by or None,
                title=chart.title,
            )
            chart.plotly_json = plotly_spec

            # Generate and save static image preview
            img_bytes = generator.export_static_image(
                chart_type=chart.chart_type,
                x=chart.x_axis or None,
                y=chart.y_axis or None,
                title=chart.title,
            )
            filename = f"chart_{chart.id or 'temp'}.png"
            chart.static_image.save(filename, ContentFile(img_bytes), save=False)
            chart.save()

            if hasattr(self.request.user, 'profile'):
                self.request.user.profile.total_visualizations_created += 1
                self.request.user.profile.save()

        except Exception as e:
            chart.config_options_json['error'] = str(e)
            chart.save()

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        chart = self.get_object()
        fmt = request.query_params.get('format', 'png').lower()
        try:
            df = load_dataframe_from_file(chart.dataset.file.path, chart.dataset.file_format)
            generator = ChartGenerator(df)
            img_bytes = generator.export_static_image(
                chart_type=chart.chart_type,
                x=chart.x_axis or None,
                y=chart.y_axis or None,
                title=chart.title,
                format=fmt if fmt in ['png', 'svg', 'pdf'] else 'png'
            )
            content_types = {'png': 'image/png', 'svg': 'image/svg+xml', 'pdf': 'application/pdf'}
            return HttpResponse(img_bytes, content_type=content_types.get(fmt, 'image/png'))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
