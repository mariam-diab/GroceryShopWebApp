# Generated by Django 4.2.8 on 2023-12-22 09:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GroceryApp', '0011_rename_status_address_delivered_status_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address',
            new_name='BillingDetails',
        ),
        migrations.AlterModelOptions(
            name='billingdetails',
            options={'verbose_name_plural': 'Billing Details'},
        ),
    ]
