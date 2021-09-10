from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory, ProdPage, News


class MainappTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        category = ProductCategory.objects.create(name='cat_1')
        category1 = ProductCategory.objects.create(name='cat_2')
        self.product = Product.objects.create(name=f'game_1', category=category, quantity=210)
        product1 = Product.objects.create(name=f'prod_2', category=category1, quantity=50)
        ProdPage.objects.create(id_prod=self.product, img_1="1.jpj")
        ProdPage.objects.create(id_prod=product1, img_1="2.jpj")
        News.objects.create(title='News 1', short_desc='Lorem', description='Lorem Ipsum')

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/product_detail/{self.product.pk}/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/news_1/')
        self.assertEqual(response.status_code, 200)








