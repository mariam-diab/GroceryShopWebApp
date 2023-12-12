from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'GroceryApp/index.html')

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

def login(request):
    return render(request, 'GroceryApp/login.html')

def register(request):
    return render(request, 'GroceryApp/register.html')



