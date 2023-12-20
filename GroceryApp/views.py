from django.http import HttpResponse
from django.shortcuts import render
from GroceryApp.models import *


# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    featured_products = Product.objects.filter(product_status= "published", featured= True)
    products = Product.objects.all()
    latest_products = Product.objects.all().order_by("-id")
    categories = Category.objects.all()
    rated_products = ProductReviews.objects.all().order_by("-rating")

    context = {
        "featured_products": featured_products,
        "products" : products,
        "categories" : categories,
        "latest_products": latest_products,
        "rated_products" : rated_products,
    }
    return render(request, 'GroceryApp/index.html', context)

def checkout(request):
    return render(request, 'GroceryApp/checkout.html')

def contact(request):
    categories = Category.objects.raw("select * from GroceryApp_category")
    return render(request, 'GroceryApp/contact.html', {"categories":categories})

def shop_details(request):
    categories = Category.objects.raw("select * from GroceryApp_category")
    return render(request, 'GroceryApp/shop-details.html', {"categories":categories})

def shop_grid(request, title=None):
    if title:
        products = Product.objects.raw(f"select * from GroceryApp_product where category_id in (select cid FROM GroceryApp_category where title = '{title}')")
    else:
        products = Product.objects.raw(f"select * from GroceryApp_product")    
    
    min_price_range = min(p.price for p in products)
    max_price_range = max(p.price for p in products)

        
    categories = Category.objects.raw("select * from GroceryApp_category")
    latest_products = Product.objects.raw("select top 6 * from GroceryApp_product order by id desc")

    min_price = request.GET.get('minamount')
    max_price = request.GET.get('maxamount')

    if min_price and max_price:
        products = Product.objects.raw(f"select * from GroceryApp_product where price between {min_price} and {max_price}")

    context = {
        "products" : products,
        "categories" : categories,
        "latest_products" : latest_products,
        "min_price" : min_price_range,
        "max_price" : max_price_range
    }
    return render(request, 'GroceryApp/shop-grid.html', context)

def shopping_cart(request):
    categories = Category.objects.raw("select * from GroceryApp_category")
    return render(request, 'GroceryApp/shoping-cart.html', {"categories":categories})

# from django.db import connection
# def execute_query(query):
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         return cursor.fetchall()





