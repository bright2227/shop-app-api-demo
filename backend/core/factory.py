import factory
import random
from django.contrib.auth import get_user_model
from core.models import Product


User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name', locale = 'en_US')
    last_name = factory.Faker('last_name', locale = 'en_US')
    password = factory.Faker('password')
    email = factory.Faker('email')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    # description = factory.Faker('catch_phrase')
    # choice = factory.fuzzy.FuzzyChoice(["A", "B"])
    name = factory.Sequence(lambda n: f"product_{n}")
    price = factory.LazyAttribute(lambda x: random.randrange(2, 10))
    quantity = factory.LazyAttribute(lambda x: random.randrange(200, 901))
    image = factory.Sequence(lambda n: f"/products/product{n}.png")

# python manage.py shell
# from core.factory import UserFactory, ProductFactory
# UserFactory.create_batch(5)
