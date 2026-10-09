"""
Datasets FilterSet.
"""
import django_filters
from .models import Dataset

class DatasetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    file_format = django_filters.ChoiceFilter(choices=Dataset.FORMAT_CHOICES)
    status = django_filters.ChoiceFilter(choices=Dataset.STATUS_CHOICES)
    is_public = django_filters.BooleanFilter()
    is_favorite = django_filters.BooleanFilter()
    tags = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Dataset
        fields = ['name', 'file_format', 'status', 'is_public', 'is_favorite', 'tags']
