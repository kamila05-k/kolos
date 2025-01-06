import django_filters
from .models import Product, Category
from .choices import STATUS_CHOICES, UNIT_CHOICES

class ProductFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES, label='Status')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Category')
    unit = django_filters.ChoiceFilter(choices=UNIT_CHOICES, label='Unit')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Name')

    class Meta:
        model = Product
        fields = ['status', 'category', 'unit', 'name']
