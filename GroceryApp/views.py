from django.http import HttpResponse
from django.shortcuts import render
from GroceryApp.models import Category, Product, ProductImages


# Create your views here.
def index(request):
    products = Product.objects.all() 

    context = {
        "products" : products
    }
    return render(request, 'GroceryApp/index.html', context)

def checkout(request):
    return render(request, 'GroceryApp/checkout.html')

def contact(request):
    return render(request, 'GroceryApp/contact.html')

def shop_details(request):
    return render(request, 'GroceryApp/shop-details.html')

def shop_grid(request):
    return render(request, 'GroceryApp/shop-grid.html')

def shopping_cart(request):
    return render(request, 'GroceryApp/shoping-cart.html')





