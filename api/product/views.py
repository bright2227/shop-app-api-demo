from rest_framework import viewsets, generics, mixins, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from core.models import Product
from product.serializers import ProductSerializer
from product.filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size =1000

class ProductViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, 
                      viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_class = ProductFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name', 'id']
    
    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*0.5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(security=[])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(security=[])    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
