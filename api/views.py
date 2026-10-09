"""
Consolidated API Views and Endpoints.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count, Sum

from datasets.models import Dataset
from analysis.models import Analysis
from visualizations.models import Chart

class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'message': 'Welcome to the Data Analysis Dashboard API v1',
            'version': '1.0.0',
            'endpoints': {
                'auth_register': '/api/v1/auth/register/',
                'auth_token': '/api/v1/auth/token/',
                'auth_profile': '/api/v1/auth/profile/',
                'datasets': '/api/v1/datasets/',
                'analyses': '/api/v1/analysis/',
                'visualizations': '/api/v1/visualizations/',
                'system_stats': '/api/v1/system-stats/',
                'health': '/api/v1/health/',
            }
        })

class SystemStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_datasets = Dataset.objects.filter(owner=user)
        user_analyses = Analysis.objects.filter(created_by=user)
        user_charts = Chart.objects.filter(created_by=user)

        return Response({
            'user': user.email,
            'datasets': {
                'total': user_datasets.count(),
                'total_rows': user_datasets.aggregate(total=Sum('row_count'))['total'] or 0,
                'ready': user_datasets.filter(status='ready').count(),
                'processing': user_datasets.filter(status='processing').count(),
                'favorites': user_datasets.filter(is_favorite=True).count(),
            },
            'analyses': {
                'total': user_analyses.count(),
                'completed': user_analyses.filter(status='completed').count(),
                'by_type': user_analyses.values('analysis_type').annotate(count=Count('id')),
            },
            'visualizations': {
                'total': user_charts.count(),
                'by_type': user_charts.values('chart_type').annotate(count=Count('id')),
            }
        })

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'status': 'healthy', 'service': 'Data Analysis Dashboard API'})
