# Generated by Django 4.2.8 on 2023-12-27 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0016_remove_category_cid_remove_product_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
