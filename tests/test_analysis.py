"""
Unit Tests for the Core Data Analysis Engine.
"""
from django.test import TestCase
import pandas as pd
import numpy as np
from analysis.engine import DataAnalyzer

class DataAnalyzerEngineTests(TestCase):
    def setUp(self):
        # Sample synthetic dataset
        self.data = pd.DataFrame({
            'feature_a': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
            'feature_b': [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0],
            'category': ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'C', 'A'],
        })
        self.analyzer = DataAnalyzer(self.data)

    def test_summary_statistics(self):
        stats = self.analyzer.compute_summary_statistics()
        self.assertIn('overview', stats)
        self.assertEqual(stats['overview']['total_rows'], 10)
        self.assertIn('numeric_columns', stats)
        self.assertIn('feature_a', stats['numeric_columns'])
        self.assertEqual(stats['numeric_columns']['feature_a']['mean'], 55.0)

    def test_correlation_analysis(self):
        corr = self.analyzer.compute_correlations()
        self.assertIn('matrix', corr)
        self.assertIn('strongest_correlations', corr)
        self.assertEqual(len(corr['strongest_correlations']), 1)
        # feature_a and feature_b are perfectly correlated (1.0)
        self.assertAlmostEqual(corr['strongest_correlations'][0]['correlation'], 1.0, places=2)

    def test_outlier_detection(self):
        outliers = self.analyzer.detect_outliers(method='iqr')
        self.assertIn('summary', outliers)
        self.assertIn('total_outlier_rows', outliers)

    def test_clustering_kmeans(self):
        clustering = self.analyzer.run_clustering(n_clusters=2)
        self.assertIn('cluster_profiles', clustering)
        self.assertEqual(clustering['n_clusters'], 2)

    def test_pca(self):
        pca_res = self.analyzer.run_pca(n_components=2)
        self.assertIn('explained_variance_percentage', pca_res)

    def test_regression(self):
        reg = self.analyzer.run_regression(target_col='feature_b', feature_cols=['feature_a'])
        self.assertIn('r2_score', reg)
        self.assertAlmostEqual(reg['r2_score'], 1.0, places=2)

    def test_automated_insights(self):
        insights = self.analyzer.generate_automated_insights()
        self.assertTrue(len(insights) > 0)
        self.assertIn('title', insights[0])
