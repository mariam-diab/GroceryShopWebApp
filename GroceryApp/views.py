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
    categories = Category.objects.all()
    latest_products = Product.objects.all().order_by("-id")

    context = {
        "products" : products,
        "categories" : categories,
        "latest_products" : latest_products
    }
    return render(request, 'GroceryApp/shop-grid.html', context)

def shopping_cart(request):
    return render(request, 'GroceryApp/shoping-cart.html')





