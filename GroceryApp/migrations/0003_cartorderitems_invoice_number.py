# Generated by Django 4.2.8 on 2023-12-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0002_cartorder_wishlist_cartorderitems_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
