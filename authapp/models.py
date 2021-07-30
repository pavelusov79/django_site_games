from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
	avatar = models.ImageField(upload_to="users_avatars", blank=True)
	age = models.PositiveIntegerField(verbose_name="возраст", default=18)
	activation_key = models.CharField(max_length=128, blank=True)
	activation_key_expires = models.DateTimeField(default=(datetime.now() + timedelta(hours=48)))

	def is_activation_key_expired(self):
		if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activation_key_expires:
			return True
		else:
			return False


class ShopUserProfile(models.Model):
	MALE = 'M'
	FEMALE = 'W'
	GENDER_CHOICES = (
		(MALE, 'мужской'),
		(FEMALE, 'женский'),
	)

	user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, unique=True, null=False, db_index=True)
	tagline = models.CharField(max_length=128, blank=True, verbose_name='тэги')
	aboutMe = models.TextField(max_length=512, blank=True, verbose_name='о себе')
	gender = models.CharField(max_length=1, blank=True, verbose_name='пол', choices=GENDER_CHOICES)

	@receiver(post_save, sender=ShopUser)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			ShopUserProfile.objects.create(user=instance)

	@receiver(post_save, sender=ShopUser)
	def save_user_profile(sender, instance, **kwargs):
		instance.shopuserprofile.save()



