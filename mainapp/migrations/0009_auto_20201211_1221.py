# Generated by Django 3.1.1 on 2020-12-11 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_subscribe_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='checked',
            field=models.BooleanField(),
        ),
    ]