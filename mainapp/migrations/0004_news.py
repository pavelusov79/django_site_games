# Generated by Django 3.0.4 on 2020-10-11 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_product_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='заголовок')),
                ('published', models.DateField(auto_now_add=True, verbose_name='опубликовано')),
                ('updated', models.DateField(auto_now=True, verbose_name='обновлено')),
                ('short_desc', models.CharField(max_length=256, verbose_name='краткое описание')),
                ('description', models.TextField(verbose_name='текст новости')),
                ('img_1', models.ImageField(blank=True, upload_to='news')),
                ('img_2', models.ImageField(blank=True, upload_to='news')),
                ('img_3', models.ImageField(blank=True, upload_to='news')),
                ('is_active', models.BooleanField(default=True, verbose_name='активна')),
            ],
        ),
    ]
