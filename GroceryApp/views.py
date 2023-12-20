from django.http import HttpResponse
from django.shortcuts import render
from GroceryApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect





# Create your views here.
def index(request):
    products = Product.objects.raw("select * from GroceryApp_product")
    featured_products = Product.objects.raw("select * from GroceryApp_product where product_status='published' and featured= 1 ")
    latest_products = Product.objects.raw("select * from GroceryApp_product order by id desc")
    categories = Category.objects.raw("select * from GroceryApp_category")
    rated_products = ProductReviews.objects.raw("select * from GroceryApp_productreviews order by rating desc")


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

def shop_details(request, title):
    categories = Category.objects.raw("select * from GroceryApp_category")

    product = Product.objects.raw(f"select P.*, C.title as category_title from GroceryApp_product P \
                                  left join GroceryApp_category C on P.category_id = C.cid \
                                  where P.title = '{title}'")[0]
        
    product_imgs = ProductImages.objects.raw(f"select id, images from GroceryApp_productimages where product_id = {product.id}")

    related_products = Product.objects.raw(f"select * from GroceryApp_product where category_id = '{product.category_id}'")

    context = {
        "product" : product,
        "categories" : categories,
        "imgs" : product_imgs,
        "related_products" : related_products,
    }
    return render(request, 'GroceryApp/shop-details.html', context)

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


@login_required(login_url='/user/login/')
def shopping_cart(request):
    cur_user = request.user

    user_shopping_cart = Product.objects.raw(f"select * from GroceryApp_product p join GroceryApp_cartorderitems ct on ct.product_id =p.id join GroceryApp_cartorder co on co.id= ct.order_id where co.order_status = 'process' and wl.user_id in (select id from userauths_user where id ='{cur_user.id}')")

    categories = Category.objects.raw("select * from GroceryApp_category")

    context = {
        "categories" : categories,
        "user_shopping_cart" : user_shopping_cart,
    }
    return render(request, 'GroceryApp/shoping-cart.html', context)


@login_required(login_url='/user/login/')
def wish_list(request):
    cur_user = request.user

    user_wishlist = Product.objects.raw(f"select * from GroceryApp_product p join GroceryApp_wishlist wl on wl.product_id =p.id where wl.user_id in (select id from userauths_user where id ='{cur_user.id}')")
    products = Product.objects.raw("select * from GroceryApp_product")

    context = {
        'user_wishlist' : user_wishlist,
        'products' :products,
    }
    return render(request, 'GroceryApp/wish-list.html', context)

