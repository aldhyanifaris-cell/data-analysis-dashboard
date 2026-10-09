"""
Management command to seed initial users, datasets, analyses, and visualizations.
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from datasets.models import Dataset, DataColumn, DataSample
from datasets.utils import load_dataframe_from_file, profile_and_extract_metadata
from analysis.models import Analysis, AnalysisResult
from analysis.engine import DataAnalyzer
from visualizations.models import Chart
from visualizations.generator import ChartGenerator

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample users, datasets, and analysis results.'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Create Superuser / Main Admin
        admin_user, _ = User.objects.get_or_create(
            email='admin@admin.com',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'organization': 'Data Science Lab',
                'role': 'Lead Data Scientist',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('Admin1234!')
        admin_user.save()
        self.stdout.write(self.style.SUCCESS(f"User created: {admin_user.email}"))

        # 2. Seed Sample Datasets
        sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'sample_data')
        
        sample_files = [
            ('sales_data.csv', 'Sales Performance & Revenue 2026', 'Comprehensive retail transaction dataset including categories, discounts, and regional profits.', 'csv', 'sales,finance,revenue'),
            ('student_grades.csv', 'Student Academic Performance & Study Habits', 'Dataset tracking study hours, attendance percentages, and exam outcomes.', 'csv', 'education,grades,performance'),
            ('weather_data.csv', 'Global Cities Weather & Air Quality Index', 'Environmental sensor dataset with temperature, humidity, wind, and pollution indices.', 'csv', 'weather,environment,aqi'),
            ('stock_prices.csv', 'Tech Stocks Daily Market Data', 'High-frequency stock market open, close, volume, and returns metrics.', 'csv', 'finance,stocks,market'),
        ]

        created_datasets = []
        for filename, title, desc, fmt, tags in sample_files:
            file_path = os.path.join(sample_dir, filename)
            if not os.path.exists(file_path):
                continue

            with open(file_path, 'rb') as f:
                dataset, created = Dataset.objects.get_or_create(
                    name=title,
                    owner=admin_user,
                    defaults={
                        'description': desc,
                        'file_format': fmt,
                        'tags': tags,
                        'is_public': True,
                        'is_favorite': True,
                        'status': 'processing',
                    }
                )
                if created:
                    dataset.file.save(filename, File(f), save=True)

            try:
                df = load_dataframe_from_file(dataset.file.path, dataset.file_format)
                d_meta, c_meta, s_meta = profile_and_extract_metadata(df)
                for k, v in d_meta.items():
                    setattr(dataset, k, v)
                dataset.status = 'ready'
                dataset.save()

                DataColumn.objects.filter(dataset=dataset).delete()
                for c in c_meta:
                    DataColumn.objects.create(dataset=dataset, **c)

                DataSample.objects.update_or_create(dataset=dataset, defaults=s_meta)
                created_datasets.append((dataset, df))
                self.stdout.write(f"  Processed dataset: {dataset.name}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Error processing {filename}: {e}"))

        # 3. Create Analyses & Visualizations for first dataset (Sales)
        if created_datasets:
            dataset, df = created_datasets[0]
            analyzer = DataAnalyzer(df)

            # Analysis 1: Descriptive
            analysis1 = Analysis.objects.create(
                title='Sales Revenue Descriptive Analytics',
                description='Automated descriptive and distribution metrics across sales categories.',
                dataset=dataset,
                created_by=admin_user,
                analysis_type='descriptive',
                status='completed',
                execution_time_seconds=0.12,
            )
            AnalysisResult.objects.create(
                analysis=analysis1,
                detailed_data_json=analyzer.compute_summary_statistics(),
                insights_list_json=analyzer.generate_automated_insights(),
                recommendations_list_json=analyzer.generate_recommendations(),
            )

            # Analysis 2: Correlation
            analysis2 = Analysis.objects.create(
                title='Units vs Revenue & Profit Correlation Matrix',
                description='Analysis of correlations between discount rates, unit prices, and overall profit.',
                dataset=dataset,
                created_by=admin_user,
                analysis_type='correlation',
                status='completed',
                execution_time_seconds=0.08,
            )
            AnalysisResult.objects.create(
                analysis=analysis2,
                detailed_data_json=analyzer.compute_correlations(),
                insights_list_json=analyzer.generate_automated_insights(),
                recommendations_list_json=analyzer.generate_recommendations(),
            )

            # Visualizations
            generator = ChartGenerator(df)
            
            # Chart 1: Revenue by Category
            chart1 = Chart.objects.create(
                title='Revenue by Product Category',
                dataset=dataset,
                created_by=admin_user,
                chart_type='bar',
                x_axis='product_category',
                y_axis='revenue',
                color_by='customer_segment',
                is_favorite=True,
            )
            chart1.plotly_json = generator.generate_plotly_spec('bar', x='product_category', y='revenue', color='customer_segment', title=chart1.title)
            chart1.save()

            # Chart 2: Profit vs Revenue Scatter
            chart2 = Chart.objects.create(
                title='Profit vs Revenue Correlation',
                dataset=dataset,
                created_by=admin_user,
                chart_type='scatter',
                x_axis='revenue',
                y_axis='profit',
                color_by='product_category',
                size_by='units_sold',
                is_favorite=True,
            )
            chart2.plotly_json = generator.generate_plotly_spec('scatter', x='revenue', y='profit', color='product_category', size='units_sold', title=chart2.title)
            chart2.save()

            self.stdout.write(self.style.SUCCESS("  Generated analyses and charts successfully."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
