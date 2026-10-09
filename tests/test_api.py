"""
API Endpoints Integration Tests.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datasets.models import Dataset

User = get_user_model()

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='api_user@test.com',
            username='api_user',
            password='TestPass1234!',
            first_name='API',
            last_name='Tester'
        )
        self.client.force_authenticate(user=self.user)

    def test_health_check_endpoint(self):
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')

    def test_api_root_endpoint(self):
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('endpoints', response.data)

    def test_system_stats_endpoint(self):
        response = self.client.get('/api/v1/system-stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('datasets', response.data)
        self.assertIn('analyses', response.data)

    def test_dataset_list_endpoint(self):
        response = self.client.get('/api/v1/datasets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
