from django.contrib import admin
from GroceryApp.models import *

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

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'order_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'product', 'image', 'quantity', 'price', 'total']  

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']     

class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'delivered_status']  

admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(BillingDetails, BillingDetailsAdmin)


class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']  

admin.site.register(ProductReviews, ProductReviewsAdmin)
















