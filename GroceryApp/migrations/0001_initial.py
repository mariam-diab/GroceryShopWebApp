# Generated by Django 4.2.8 on 2023-12-18 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=10,
                        max_length=20,
                        prefix="cat",
                        unique=True,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                    ),
                ),
                ("img", models.ImageField(blank=True, null=True, upload_to="category")),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=10,
                        max_length=20,
                        prefix="",
                        unique=True,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "img",
                    models.ImageField(
                        blank=True, null=True, upload_to="user_directory_path"
                    ),
                ),
                (
                    "p_description",
                    models.TextField(
                        blank=True, default="This is the product", null=True
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=1.99, max_digits=20),
                ),
                (
                    "old_price",
                    models.DecimalField(decimal_places=2, default=2.99, max_digits=20),
                ),
                ("specifications", models.TextField(blank=True, null=True)),
                (
                    "product_status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("disabled", "Disabled"),
                            ("rejected", "Rejected"),
                            ("in_review", "In Review"),
                            ("published", "published"),
                        ],
                        default="in_review",
                        max_length=10,
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("in_stock", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=True)),
                ("digital", models.BooleanField(default=True)),
                (
                    "sku",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=10,
                        max_length=20,
                        prefix="sku",
                        unique=True,
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="GroceryApp.category",
                        to_field="cid",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductImages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("images", models.ImageField(upload_to="product-images")),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="GroceryApp.product",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Product Images",
            },
        ),
    ]
