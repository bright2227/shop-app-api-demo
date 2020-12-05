from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=False,
    )

    class Meta(AbstractUser.Meta):
        pass


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.name


class OrderState(models.TextChoices):
    cart = 'CR', _('Cart')
    order = 'PR', _('Process')
    finish = 'FN', _('Finish')


class Order(models.Model):
    total = models.FloatField(blank=True, null=True)
    address = models.CharField(default='', max_length=40)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=2,
        choices=OrderState.choices,
        default=OrderState.cart,)
    order_items = models.ManyToManyField(Product, through="Orderitem")

    def __str__(self):
        return str(self.user.username) + ' ' + str(self.total) + ' ' + str(self.state)

# def create_order_as_cart(sender, created, instance, **kwargs):
#     if created:
#         order = Order.objects.create(user=instance)
# post_save.connect(create_order_as_cart, sender=get_user_model())


class Orderitem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # status = models.

    def __str__(self):
        return str(self.order.id) + ' ' + str(self.item) + ' ' + str(self.quantity) + 'pcs'
