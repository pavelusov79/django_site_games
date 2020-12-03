from django.db.models import Q
from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory


class MainappTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        category = ProductCategory.objects.create(name='cat_1')
        category1 = ProductCategory.objects.create(name='cat_2')
        for i in range(10):
            Product.objects.create(name=f'prod_{i}', category=category, quantity=210)
        for j in range(11, 21):
            Product.objects.create(name=f'prod_{j}', category=category1, quantity=50)

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/page/1')
        self.assertEqual(response.status_code, 200)

    def test_products_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/catalog/{product.pk}')
            self.assertEqual(response.status_code, 200)

    def test_discount_products_urls(self):
        for discount_product in Product.objects.filter(Q(category__is_active=True) & Q(quantity__gte=200)):
            response = self.client.get(f'/discount/{discount_product.pk}/')
            self.assertEqual(response.status_code, 200)




