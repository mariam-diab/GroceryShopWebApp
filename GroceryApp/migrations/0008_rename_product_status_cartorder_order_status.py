# Generated by Django 4.2.8 on 2023-12-20 18:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("GroceryApp", "0007_alter_cartorderitems_invoice_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartorder",
            old_name="product_status",
            new_name="order_status",
        ),
    ]
