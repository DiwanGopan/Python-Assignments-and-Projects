# Generated by Django 3.0 on 2022-05-19 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_product_quantity'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Authenticate',
            new_name='Seller_Authenticate',
        ),
    ]