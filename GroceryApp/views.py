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
    return render(request, 'GroceryApp/contact.html')

def shop_details(request):
    return render(request, 'GroceryApp/shop-details.html')

def shop_grid(request, title=None):
    if title:
        products = Product.objects.filter(category__title=title)
    else:
        products = Product.objects.all()

    min_price_range = min(p.price for p in products)
    max_price_range = max(p.price for p in products)
        
    categories = Category.objects.all()
    latest_products = Product.objects.all().order_by("-id")

    min_price = request.GET.get('minamount')
    max_price = request.GET.get('maxamount')

    if min_price and max_price:
        products = products.filter(price__range=(min_price, max_price))


    context = {
        "products" : products,
        "categories" : categories,
        "latest_products" : latest_products,
        "min_price" : min_price_range,
        "max_price" : max_price_range
    }
    return render(request, 'GroceryApp/shop-grid.html', context)

def shopping_cart(request):
    return render(request, 'GroceryApp/shoping-cart.html')





