from datetime import datetime
from unicodedata import decimal

from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="название", max_length=64, unique=True)
    description = models.TextField(verbose_name="описание", blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="название игры", max_length=128)
    image = models.ImageField(upload_to="products_images", blank=True)
    description = models.TextField(verbose_name="описание игры", blank=True)
    price = models.DecimalField(verbose_name="стоимость игры", max_digits=8, decimal_places=2,
                                default=0)
    quantity = models.IntegerField(verbose_name="количество на складе", default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def disc_price(self):
        return round(self.price / 2, 2)

    @property
    def get_price(self):
        if self.quantity >= 200:
            return self.disc_price
        else:
            return self.price

    @staticmethod
    def select_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class ProdPage(models.Model):
    id_prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_1 = models.ImageField(upload_to="prod_page", blank=True)
    img_2 = models.ImageField(upload_to="prod_page", blank=True)
    img_3 = models.ImageField(upload_to="prod_page", blank=True)
    img_4 = models.ImageField(upload_to="prod_page", blank=True)

    def __str__(self):
        return self.id_prod.name


class News(models.Model):
    title = models.CharField(verbose_name="заголовок", max_length=64)
    published = models.DateField(verbose_name="опубликовано",
                                 default=datetime.now)
    updated = models.DateField(verbose_name='обновлено',
                               auto_now=True)
    short_desc = models.CharField(verbose_name="краткое описание",
                                  max_length=256)
    description = models.TextField(verbose_name="текст новости")
    img_1 = models.ImageField(upload_to="news", blank=True)
    img_2 = models.ImageField(upload_to="news", blank=True)
    img_3 = models.ImageField(upload_to="news", blank=True)
    is_active = models.BooleanField(verbose_name='активна',
                                    default=True)


class Subscribe(models.Model):
    client_email = models.EmailField(max_length=50, blank=False)
    is_active = models.BooleanField(verbose_name='активна', default=True)
    checked = models.BooleanField()

    def __str__(self):
        return self.client_email
