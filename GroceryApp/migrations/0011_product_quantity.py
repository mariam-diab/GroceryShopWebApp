# Generated by Django 4.2.8 on 2023-12-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0010_product_unit_quantity_product_unit_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
