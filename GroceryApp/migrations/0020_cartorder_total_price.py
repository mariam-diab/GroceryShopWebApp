# Generated by Django 4.2.8 on 2023-12-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0019_remove_cartorder_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=14, null=True),
        ),
    ]
