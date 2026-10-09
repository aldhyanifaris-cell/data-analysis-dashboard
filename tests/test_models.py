"""
Model Tests for Datasets, Accounts, Analysis, and Visualizations.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from datasets.models import Dataset, DataColumn, DataSample
from analysis.models import Analysis, AnalysisResult
from visualizations.models import Chart

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='tester@test.com',
            username='tester',
            password='TestPassword123!',
            first_name='Test',
            last_name='User'
        )
        self.dataset = Dataset.objects.create(
            name='Test Sales Dataset',
            owner=self.user,
            file_format='csv',
            row_count=100,
            column_count=5
        )

    def test_custom_user_creation(self):
        self.assertEqual(self.user.email, 'tester@test.com')
        self.assertTrue(self.user.check_password('TestPassword123!'))

    def test_dataset_creation(self):
        self.assertEqual(self.dataset.name, 'Test Sales Dataset')
        self.assertEqual(self.dataset.row_count, 100)

    def test_data_column_creation(self):
        col = DataColumn.objects.create(
            dataset=self.dataset,
            name='revenue',
            data_type='numeric',
            mean_value=250.5
        )
        self.assertEqual(col.name, 'revenue')
        self.assertEqual(col.mean_value, 250.5)

    def test_analysis_creation(self):
        analysis = Analysis.objects.create(
            title='Descriptive Analysis',
            dataset=self.dataset,
            created_by=self.user,
            analysis_type='descriptive',
            status='completed'
        )
        self.assertEqual(analysis.title, 'Descriptive Analysis')
        self.assertEqual(analysis.status, 'completed')

    def test_chart_creation(self):
        chart = Chart.objects.create(
            title='Revenue Bar Chart',
            dataset=self.dataset,
            created_by=self.user,
            chart_type='bar',
            x_axis='category',
            y_axis='revenue'
        )
        self.assertEqual(chart.title, 'Revenue Bar Chart')
        self.assertEqual(chart.chart_type, 'bar')
