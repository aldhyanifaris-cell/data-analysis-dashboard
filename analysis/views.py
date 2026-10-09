"""
Analysis API Views.
"""
import time
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from datasets.models import Dataset
from datasets.utils import load_dataframe_from_file
from .models import Analysis, AnalysisResult, StatisticalResult
from .serializers import AnalysisSerializer, AnalysisResultSerializer
from .engine import DataAnalyzer

class AnalysisViewSet(viewsets.ModelViewSet):
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Analysis.objects.filter(
            models.Q(created_by=user) | models.Q(dataset__owner=user) | models.Q(dataset__is_public=True)
        ).distinct().select_related('created_by', 'dataset', 'result')

    def perform_create(self, serializer):
        analysis = serializer.save(created_by=self.request.user, status='running')
        self._execute_analysis(analysis)

    def _execute_analysis(self, analysis: Analysis):
        start_time = time.time()
        try:
            dataset = analysis.dataset
            df = load_dataframe_from_file(dataset.file.path, dataset.file_format)
            analyzer = DataAnalyzer(df)

            params = analysis.parameters_json or {}
            analysis_type = analysis.analysis_type

            summary_metrics = {}
            detailed_data = {}

            if analysis_type == 'descriptive':
                detailed_data = analyzer.compute_summary_statistics()
                summary_metrics = detailed_data.get('overview', {})
            elif analysis_type == 'correlation':
                method = params.get('method', 'pearson')
                detailed_data = analyzer.compute_correlations(method=method)
            elif analysis_type == 'outliers':
                method = params.get('method', 'iqr')
                threshold = float(params.get('threshold', 1.5))
                detailed_data = analyzer.detect_outliers(method=method, threshold=threshold)
            elif analysis_type == 'clustering':
                features = params.get('features')
                k = int(params.get('n_clusters', 3))
                detailed_data = analyzer.run_clustering(features=features, n_clusters=k)
            elif analysis_type == 'pca':
                n_comp = int(params.get('n_components', 2))
                detailed_data = analyzer.run_pca(n_components=n_comp)
            elif analysis_type == 'regression':
                target = params.get('target_column')
                features = params.get('feature_columns')
                detailed_data = analyzer.run_regression(target_col=target, feature_cols=features)
            else:
                # Full Profile
                detailed_data = {
                    'summary': analyzer.compute_summary_statistics(),
                    'correlations': analyzer.compute_correlations(),
                    'outliers': analyzer.detect_outliers(),
                }

            insights = analyzer.generate_automated_insights()
            recommendations = analyzer.generate_recommendations()

            # Save AnalysisResult
            AnalysisResult.objects.update_or_create(
                analysis=analysis,
                defaults={
                    'summary_metrics_json': summary_metrics,
                    'detailed_data_json': detailed_data,
                    'insights_list_json': insights,
                    'recommendations_list_json': recommendations,
                }
            )

            analysis.status = 'completed'
            analysis.execution_time_seconds = float(round(time.time() - start_time, 3))
            analysis.save()

            if hasattr(self.request.user, 'profile'):
                self.request.user.profile.total_analyses_run += 1
                self.request.user.profile.save()

        except Exception as e:
            analysis.status = 'failed'
            analysis.error_message = str(e)
            analysis.execution_time_seconds = float(round(time.time() - start_time, 3))
            analysis.save()

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        analysis = self.get_object()
        if hasattr(analysis, 'result'):
            return Response(analysis.result.detailed_data_json)
        return Response({'status': 'pending'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def insights(self, request, pk=None):
        analysis = self.get_object()
        if hasattr(analysis, 'result'):
            return Response(analysis.result.insights_list_json)
        return Response([])

    @action(detail=True, methods=['get'])
    def recommendations(self, request, pk=None):
        analysis = self.get_object()
        if hasattr(analysis, 'result'):
            return Response(analysis.result.recommendations_list_json)
        return Response([])
