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
        if getattr(self, 'swagger_fake_view', False):
        # queryset just for schema generation metadata
            return Orderitem.objects.none()
        cart = Order.objects.get(user=self.request.user, state='CR')
        queryset = self.queryset.filter(order=cart)
        return queryset

    def perform_create(self, serializer):
        item_id = self.get_queryset().values_list('item_id', flat=True)
        if self.request.data['item'] in item_id:
            raise ValidationError('item is repeat')
        else:
            serializer.save()
            
    @swagger_auto_schema(operation_summary='列出在購物車內的所有物品資料',
        operation_description='')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='讀取購物車內的特定物品資料',
        operation_description='')    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='添加物品進入購物車內',
        operation_description='無法重複添加相同物品，若要更改數量請用update。\n \
        如果購買數量高過庫存，則無法購買。') 
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='更改購物車內的特定物品數量',
        operation_description='如果更改後購買數量高過庫存，則無法購買。') 
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='更改購物車內的特定物品數量',
        operation_description='如果更改後購買數量高過庫存，則無法購買。')     
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='刪除購物車內的特定物品')       
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
        # queryset just for schema generation metadata
            return Order.objects.none() 

        if self.action in ("update", "destroy"):
            queryset = self.queryset.filter(user=self.request.user, state='PR')
            if not queryset:
                raise ValidationError('There is no order in process state')
        else:    
            queryset = self.queryset.filter(user=self.request.user)
        return queryset 

    def get_serializer_class(self):        
        if self.action == "create":
            return OrderCreateSerializer
        else:
            return OrderSerializer
        
    @swagger_auto_schema(operation_summary='列出所有訂單資料，包括購物車',
        operation_description='列出所有使用者曾經下訂的訂單. "CR"(Cart)代表未成單的購物車狀態,\
        "PR"(Process) 代表正在處理的訂單狀態，使用者可改變訂單寄送資訊，或刪除訂單。 "FN" 代表已經 \
        完成的歷史訂單，無法修改.')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='讀取特定訂單資料，包括購物車',
        operation_description='列出所有使用者曾經下訂的訂單. "CR"(Cart)代表未成單的購物車狀態訂單,\
        "PR"(Process) 代表正在處理狀態的訂單，使用者可改變訂單寄送資訊，或刪除訂單。 "FN" 代表已經 \
        完成的歷史訂單，無法修改.')   
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='將購物車內所有產物形成訂單',
        operation_description='將未成單的購物車狀態訂單改為"PR"(Process)正在處理狀態的訂單，同時扣除 \
        相對應的物品庫存數量。如果購物車內物品的訂購數量高過庫存物品數量，則無法形成訂單。成功形成訂單後，\
        將透過信箱收到此次購買清單和總金額信件。')
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("Order is successfully created", status=status.HTTP_201_CREATED, headers=headers)
    
    @swagger_auto_schema(operation_summary='修改在處理狀態的訂單', 
        operation_description='使用者可以修改"PR"(Process)正在處理狀態的訂單，只能修改其通信資料，如寄件地址。\
        或者刪除整個訂單。但無法修改訂單內部購買物品的數量和總類。') 
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary='修改在處理狀態的訂單', 
        operation_description='使用者可以修改"PR"(Process)正在處理狀態的訂單，只能修改其通信資料，如寄件地址。\
        或者刪除整個訂單。但無法修改訂單內部購買物品的數量和總類。')  
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='刪除在處理狀態的訂單', )       
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
