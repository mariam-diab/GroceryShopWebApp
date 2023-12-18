from django.contrib import admin
from GroceryApp.models import Category, Product, ProductImages

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'old_price', 'featured', 'product_status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)











