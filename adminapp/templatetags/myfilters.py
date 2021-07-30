from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='user_img_filter')
def users_img_filter(string):
    if not string:
        string = 'users_avatars/default_avatar.png'
    return f'{settings.MEDIA_URL}{string}'