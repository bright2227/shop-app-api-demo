from rest_framework import serializers
from core.models import Product


class ProductSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
            view_name='shop:product-detail',
            lookup_field='pk') # not id

    class Meta:
        model =  Product
        fields  = ('id', 'name', 'price', 'quantity', 'image', 'url')
        read_only_fields = ('id', 'name', 'price', 'quantity', 'image', 'url')
