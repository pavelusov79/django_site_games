from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product, ProdPage
from authapp.models import ShopUser
# from django.contrib.auth.models import User

import json, os


JSON_PATH = 'mainapp/json'

def loadFromJSON(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)



class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = loadFromJSON('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()
        
        
        products = loadFromJSON('products')
        
        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        prod_pages = loadFromJSON('prod_page')

        ProdPage.objects.all().delete()
        for prod_page in prod_pages:
            id_prod = prod_page["id_prod"]
            _name = Product.objects.get(name = id_prod)
            prod_page["id_prod"] = _name
            new_prod_page = ProdPage(**prod_page)
            new_prod_page.save()

        # Создаем суперпользователя при помощи менеджера модели
        super_user = ShopUser.objects.create_superuser('django', '', 'geekbrains', age=18)
        

