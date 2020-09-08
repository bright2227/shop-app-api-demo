from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Order, Orderitem, Product
from order.serializers import OrderCreateSerializer
import time


ORDER_URL = reverse('shop:order-list')


class PrivateOrderCreateTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user = get_user_model().objects.create(username='testname',
             password='testpass', email = 'wofopa7788@trufilth.com')
        self.order = Order.objects.create(user=self.user)
        
        self.user2 = get_user_model().objects.create(username='testname2',
             password='testpass2')
        self.order2 = Order.objects.create(user=self.user2)
        
        self.client.force_authenticate(self.user)

    def test_create_order_nothing_in_cart(self):
        res = self.client.post(ORDER_URL, {"address": "somewhere"})        
        self.assertIn(b'nothing in the cart', res.content)

    def test_create_order_zero_product_quantity(self):
        test_item = Product.objects.create(name='testprod', quantity=0, price=1.00)
        Orderitem.objects.create(item=test_item, quantity=2, order=self.order)

        res = self.client.post(ORDER_URL, {"address": "somewhere"})
        self.assertIn(b'is zero', res.content)

    def test_create_order_too_many_quantity(self):
        test_item = Product.objects.create(name='testprod', quantity=1, price=1.00)
        Orderitem.objects.create(item=test_item, quantity=5, order=self.order)

        res = self.client.post(ORDER_URL, {"address": "somewhere"})
        self.assertIn(b' is larger than storage quantity', res.content)

    def test_create_order_success(self):
        test_item = Product.objects.create(name='testprod', quantity=10, price=1.00)
        test_item2 = Product.objects.create(name='testprod2', quantity=10, price=1.00)
        Orderitem.objects.create(item=test_item, quantity=3, order=self.order)
        Orderitem.objects.create(item=test_item2, quantity=2, order=self.order)

        start_time = time.time()
        res = self.client.post(ORDER_URL, {"address": "somewhere"})
        print(time.time()-start_time)

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

