from django.http import HttpResponse
from django.shortcuts import render
from GroceryApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator






# Create your views here.
def index(request):
    products = Product.objects.raw("select * from GroceryApp_product")
    featured_products = Product.objects.raw("select P.*, C.title as category_title from GroceryApp_product P \
                                            left join GroceryApp_category C on P.category_id = C.cid \
                                            where P.product_status='published' and P.featured= 1 ")
    latest_products = Product.objects.raw("select top 6 * from GroceryApp_product order by id desc")
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

def shop_details(request):
    title = request.GET.get('title', None)
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

def shop_grid(request):
    category = request.GET.get('category') or "All"
    product = request.GET.get('product', '')
    if product:
        products = Product.objects.raw("select * from GroceryApp_product where title like %s", ['%' + product + '%'])
    elif category != "All":
        products = Product.objects.raw(f"select * from GroceryApp_product where category_id in (select cid FROM GroceryApp_category where title = '{category}')")
    else:
        products = Product.objects.raw(f"select * from GroceryApp_product") 

        
    categories = Category.objects.raw("select * from GroceryApp_category")
    latest_products = Product.objects.raw("select top 6 * from GroceryApp_product order by id desc")

    min_price = request.GET.get('minamount')
    max_price = request.GET.get('maxamount')

    if min_price and max_price:
        products = Product.objects.raw(f"select * from GroceryApp_product where price between {min_price} and {max_price}")

    min_price_range = min((p.price for p in products), default=0)
    max_price_range = max((p.price for p in products), default=0)

    paginator = Paginator(products, 6) 
    page_number = request.GET.get('page')
    paginated_products = paginator.get_page(page_number) 

    context = {
        "products" : products,
        "categories" : categories,
        "latest_products" : latest_products,
        "min_price" : min_price_range,
        "max_price" : max_price_range,
        "paginated_products" : paginated_products,
        "category" : category,
    }
    return render(request, 'GroceryApp/shop-grid.html', context)


@login_required(login_url='/user/login/')
def shopping_cart(request):
    categories = Category.objects.raw("select * from GroceryApp_category")
    return render(request, 'GroceryApp/shoping-cart.html', {"categories":categories})


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

