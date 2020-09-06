import django_filters
from core.models import Product


class ProductFilter(django_filters.rest_framework.FilterSet):

    pricemin = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    # names = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['pricemin', 'pricemax', ]
