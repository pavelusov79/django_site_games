from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "basket")
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	quantity = models.PositiveIntegerField(verbose_name = "количество", default = 0)
	add_datetime = models.DateTimeField(verbose_name = "дата", auto_now_add = True)

	def __str__(self):
		return self.product.name

	@property
	def product_cost(self):
	# 	if(self.product.quantity >= 200):
	# 		return self.product.disc_price * self.quantity
	# 	else:
	# 		return self.product.price * self.quantity
		return self.product.get_price * self.quantity


	# @property
	# def product_cost_discount(self):
	# 	return self.product.disc_price * self.quantity

	@property
	def total_quantity(self):
		items = Basket.objects.filter(user = self.user)
		return sum(list(map(lambda x: x.quantity, items)))

	@property
	def total_cost(self):
		items = Basket.objects.filter(user=self.user)
		return sum(list(map(lambda x: x.product_cost, items)))

	@staticmethod
	def get_items(user):
		return Basket.objects.filter(user=user)

	@staticmethod
	def get_item(pk):
		return Basket.objects.filter(pk=pk).first()

