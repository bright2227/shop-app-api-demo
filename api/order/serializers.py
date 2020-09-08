from rest_framework import serializers
from django.db import transaction
from core.models import Order, Orderitem, Product
from order.tasks import send_mail_task
from django.http import HttpResponse
# from django.db.models import Prefetch


class OrderitemSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
            view_name='shop:orderitem-detail',
            lookup_field='pk') 

    class Meta:
        model = Orderitem
        fields = ('id', 'item', 'quantity', 'url')
        read_only_fields = ('id', 'item', 'url')

    def validate_item(self, attr):
        # attr is an product objects            
        if attr.quantity < int(self.initial_data['quantity']):
            raise serializers.ValidationError('Item quantity is larger than product quantity')
        return attr
              
    def create(self, validated_data):
        validated_data['order']=Order.objects.get(user=self.context['request'].user, state='CR')
        item = Orderitem.objects.create(**validated_data)
        return item

    def update(self, instance, validated_data):
        # Not allow changing of item's id, if customer wants new item, they should use create
        # put, patch go through this func
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class OrderCreateSerializer(serializers.Serializer):
    address = serializers.CharField()

    def validate_address(self, attr):
        if len(attr)==0:
            raise serializers.ValidationError("address can't be empty")
        return attr

    def create(self, validated_data):
        # after selected_related, orderitem.values('id'), orderitem.values_list('id'), orderitem.get(id=id)  
        # still request data from sql

        order = Order.objects.get(user=self.context['request'].user, state='CR')
        orderitem = Orderitem.objects.filter(order=order).select_related('item')
        if not orderitem:
            raise serializers.ValidationError("nothing in the cart") 

        # still trigger user foreign key in order model even using 'defer', 'only'
        # pref = Prefetch('order_items', queryset=Orderitem.objects.all().select_related('item'))
        # order = Order.objects.prefetch_related(pref).get(user=self.context['request'].user, state='CR')
            
        out_of_stock, too_many_orderitem, reciept = '', '', ''
        validated_data['total'] =  0
        product_update = []
        for itm in orderitem:

            if itm.item.quantity <= 0:
                out_of_stock = out_of_stock + f"The storage quantity of {itm.item.name} is zero \n"
                continue

            if itm.quantity > itm.item.quantity:
                too_many_orderitem = too_many_orderitem + f"The order quantity({itm.quantity}) of {itm.item.name} \
                    is larger than storage quantity({itm.item.quantity}) \n"
                continue

            itm.item.quantity = itm.item.quantity - itm.quantity
            product_update.append(itm.item)
            reciept = reciept + f"{itm.item.name} has {itm.quantity} pcs\n"
            validated_data['total'] += itm.quantity * itm.item.price


        # handle quantity problem
        if (out_of_stock + too_many_orderitem != ''):
            raise serializers.ValidationError(out_of_stock + too_many_orderitem)

        # Create Order
        with transaction.atomic():
            order.total = validated_data['total']
            order.address = validated_data['address']
            order.state = 'PR'
            order.save()
            Order.objects.create(user=self.context['request'].user) # can't use bulk_update to update item in foreignkey
            Product.objects.bulk_update(product_update, ['quantity']) 

        # reciept = reciept + f"total bill is {validated_data['total']} \n Thank you for purchasing"
        # send_mail_task.delay(reciept, orderitem[0].user.username, orderitem[0].user.email)
        return order


class OrderSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
            view_name='shop:order-detail',
            lookup_field='pk')  
            
    orderitem_set = OrderitemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'address', 'total', 'orderitem_set', 'state', 'url')
        read_only_fields = ('id', 'total', 'orderitem_set', 'state', 'url') 
        