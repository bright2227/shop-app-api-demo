from django.contrib import admin
from core.models import Orderitem, Order, Product
# Register your models here.

admin.site.register(Orderitem)
admin.site.register(Order)
admin.site.register(Product)
