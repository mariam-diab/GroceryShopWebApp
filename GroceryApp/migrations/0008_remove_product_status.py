# Generated by Django 4.2.8 on 2023-12-27 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0007_rename_p_description_product_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
    ]