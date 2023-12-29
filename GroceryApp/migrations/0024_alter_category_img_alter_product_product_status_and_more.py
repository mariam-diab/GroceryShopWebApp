# Generated by Django 4.2.8 on 2024-01-07 19:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("GroceryApp", "0023_alter_productimages_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="img",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("disabled", "Disabled"),
                    ("rejected", "Rejected"),
                    ("in_review", "In Review"),
                    ("published", "published"),
                ],
                default="published",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]