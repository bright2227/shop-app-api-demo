from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from core.models import Product, Orderitem, Order
from order.serializers import OrderitemSerializer, OrderCreateSerializer, OrderSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = Orderitem.objects.all()
    serializer_class = OrderitemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Order.objects.get(user=self.request.user, state='CR')
        queryset = self.queryset.filter(order=cart)
        return queryset

    def perform_create(self, serializer):
        item_id = self.get_queryset().values_list('item_id', flat=True)
        if self.request.data['item'] in item_id:
            raise ValidationError('item is repeat')
        else:
            serializer.save()
            
    @swagger_auto_schema(operation_description='List all orderitem in cart stage.')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='get certain orderitem in cart stage.')    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='The creating repeat orderitem is not allowed.\
        You can change quantity by update original item.') 
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='You can change quantity of orderitem in cart stage.\
        if you want to get new item, please use create method.') 
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description='You can change quantity of orderitem in cart stage.\
        if you want to get new item, please use create method.')     
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description='Delete orderitem in cart stage.')       
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        queryset = self.queryset.filter(user=self.request.user)
        return queryset 

    def get_serializer_class(self):        
        if self.action == "create":
            return OrderCreateSerializer
        else:
            return OrderSerializer
        
    @swagger_auto_schema(operation_description='All your order. "CR" means in the cart stage, \
        "FN" means the order has already created.')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description='get certain order. for "CR" cart stage and "FN" \
        finished stage.')    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="Take all orderitem in the cart into order. If item is out of stock \
        or lower than the demanding quantity, You can't buy this item.\n  \
        The receipt will be sent after order is successfully created.")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("Order is successfully created", status=status.HTTP_201_CREATED, headers=headers)
    
    @swagger_auto_schema(operation_description="You are only allowed to change order information.\
        But the information of orderitem can't be changed. If something wrong about \
        your orderitem, you have to delete the order and add orderitem.") 
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="You are only allowed to change order information.\
        But the information of orderitem can't be changed. If something wrong about \
        your orderitem, you have to delete the order and add orderitem.")  
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description=' Delete whole order.')       
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
