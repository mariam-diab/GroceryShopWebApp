# Generated by Django 4.2.8 on 2023-12-28 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0020_cartorder_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cartorder',
            name='total_price',
        ),
        migrations.DeleteModel(
            name='ProductReviews',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
