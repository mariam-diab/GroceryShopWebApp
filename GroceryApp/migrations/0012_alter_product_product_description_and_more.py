# Generated by Django 4.2.8 on 2023-12-27 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0011_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.TextField(blank=True, default='This is the product', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
