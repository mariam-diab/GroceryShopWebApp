# Generated by Django 4.2.8 on 2023-12-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0015_billingdetails_zip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], db_collation='Arabic_CI_AI', default='Processing', max_length=30),
        ),
    ]
