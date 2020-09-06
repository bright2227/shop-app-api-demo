from rest_framework import serializers
from core.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Product
        fields  = ('id', 'name', 'price', 'quantity',)
        read_only_fields = ('id', )
