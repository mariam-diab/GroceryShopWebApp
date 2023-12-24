from django.http import HttpResponse
from django.shortcuts import render, redirect
from GroceryApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator



from django.db import connection



# Create your views here.
def index(request):
    cur_user = request.user
    products = Product.objects.raw("select * from GroceryApp_product")
    featured_products = Product.objects.raw("select P.*, C.title as category_title from GroceryApp_product P \
                                            left join GroceryApp_category C on P.category_id = C.cid \
                                            where P.product_status='published' and P.featured= 1 ")
    latest_products = Product.objects.raw("select top 6 * from GroceryApp_product order by id desc")
    categories = Category.objects.raw("select * from GroceryApp_category")
    rated_products = ProductReviews.objects.raw("select * from GroceryApp_productreviews order by rating desc")
    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    context = {
        "featured_products": featured_products,
        "products" : products,
        "categories" : categories,
        "latest_products": latest_products,
        "rated_products" : rated_products,
        "total_cart_items" :total_cart_items, 
    }
    return render(request, 'GroceryApp/index.html', context)

@login_required(login_url='/user/login/')
def checkout(request):
    cur_user = request.user
    sub_total_price = total_price_calc(cur_user)
    if not sub_total_price:
        return render(request, 'GroceryApp/shoping-cart.html')
    total_price = sub_total_price if sub_total_price >= 99 else sub_total_price + 50
    if request.method == "GET":
        cart_items = CartOrder.objects.raw(f"select Co.ct_ord_id, CI.ct_ord_it_id, P.id, P.title, CI.total from GroceryApp_cartorder Co \
                                                    left join  GroceryApp_cartorderitems CI \
                                                    on Co.ct_ord_id = CI.order_id \
                                                    left join GroceryApp_product P \
                                                    on P.id = CI.product_id \
                                                    where Co.order_status = 'processing' and \
                                                    CO.user_id = '{cur_user.id}'")
        context = {
            "user" : cur_user,
            "items" : cart_items,
            "sub_total_price" : sub_total_price, 
            "total_price" : total_price,
        }
        return render(request, 'GroceryApp/checkout.html', context)
    elif request.method == "POST":
        order_id = request.POST.get('order_id')
        data = {key: request.POST.get(key) for key in request.POST.keys()}
        if data['payment_method'] == "paypal":  
            to_be_paid = 0 
            payment_status = 1
        else: 
            to_be_paid = total_price
            payment_status = 0

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO dbo.GroceryApp_billingdetails \
                        (user_id, order_id, first_name, last_name, \
                        address, apartment, governorate, city, zip, phone, email, \
                        payment_method, payment_status, to_be_paid, delivered_status) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [cur_user.id, data["order_id"], data['first_name'], data['last_name'],
                        data['address'], data['apartment'], data['governorate'], data['city'], data['zip'], 
                        data['phone'], data['email'], data['payment_method'], payment_status, to_be_paid, False])
            cursor.execute(f"UPDATE GroceryApp_cartorder \
                            SET order_status = 'shipped', \
                            paid_status = '{payment_status}'\
                            WHERE user_id = '{cur_user.id}'")


            return render(request, 'GroceryApp/checkedout.html')


def contact(request):
    cur_user = request.user

    categories = Category.objects.raw("SELECT * FROM GroceryApp_category")
    # categories = Category.objects.all()

    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    context = {
        "categories":categories,
        "total_cart_items" : total_cart_items, 
        }
    
    return render(request, 'GroceryApp/contact.html', context )

def shop_details(request):
    cur_user = request.user
    title = request.GET.get('title', None)
    categories = Category.objects.raw("select * from GroceryApp_category")

    product = Product.objects.raw(f"select P.*, C.title as category_title from GroceryApp_product P \
                                  left join GroceryApp_category C on P.category_id = C.cid \
                                  where P.title = '{title}'")[0]
        
    product_imgs = ProductImages.objects.raw(f"select id, images from GroceryApp_productimages where product_id = {product.id}")

    related_products = Product.objects.raw(f"select * from GroceryApp_product where category_id = '{product.category_id}'")

    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    total_purchase = f"SELECT COUNT(order_id) AS total_count \
    FROM GroceryApp_cartorderitems \
    WHERE product_id = {product.id} \
    GROUP BY product_id \
    HAVING product_id = {product.id}"
    
    total_purchase_today = f"select count(CI.product_id) count_last_day from GroceryApp_cartorderitems CI \
    left join GroceryApp_cartorder C \
    on CI.order_id = C.ct_ord_id \
    where C.order_status = 'shipped' and C.order_date >= dateadd(hour, -24, getdate()) \
    group by product_id \
    having product_id = {product.id}"

    with connection.cursor() as cursor:
        cursor.execute(total_purchase)
        total_purchase = cursor.fetchall()
        cursor.execute(total_purchase_today)
        total_purchase_today = cursor.fetchall()

    total_purchase = total_purchase[0][0] if total_purchase else 0
    total_purchase_today = total_purchase_today[0][0] if total_purchase_today else 0


    context = {
        "product" : product,
        "categories" : categories,
        "imgs" : product_imgs,
        "related_products" : related_products,
        "total_cart_items" :total_cart_items,
        "total_purchase" : total_purchase,
        "total_purchase_today" : total_purchase_today,

    }
    return render(request, 'GroceryApp/shop-details.html', context)

def shop_grid(request):
    cur_user = request.user
    category = request.GET.get('category') or "All"
    product = request.GET.get('product')
    brand_name = request.GET.get('brand_name')
    nationality = request.GET.get('nationality')
    if product:
        products = Product.objects.raw(f"select * from GroceryApp_product where title like '%%{product}%%' or brand_name like '%%{product}%%' or brand_nationality like '%%{product}%%'")
    # elif category != "All":
    #     products = Product.objects.raw(f"select * from GroceryApp_product where category_id in (select cid FROM GroceryApp_category where title = '{category}')")
    # else:
    #     products = Product.objects.raw(f"select * from GroceryApp_product")
    else:
        min_price = request.GET.get('minamount')
        max_price = request.GET.get('maxamount')
        sql_query = "SELECT * from GroceryApp_product where 1=1" 
        if category != "All":
            sql_query += f"and category_id in (select cid FROM GroceryApp_category where title = '{category}')"
        if min_price and max_price:
            sql_query += f"and price between {min_price} and {max_price}"
            # products = Product.objects.raw(f"select * from GroceryApp_product where price between {min_price} and {max_price}")
        if brand_name:
            sql_query += f"and brand_name = '{brand_name}'"
        if nationality:
            sql_query += f"and brand_nationality = '{nationality}'"

        products = Product.objects.raw(sql_query)

        
    categories = Category.objects.raw("select * from GroceryApp_category")
    latest_products = Product.objects.raw("select top 6 * from GroceryApp_product order by id desc")

    min_price_range = min((p.price for p in products), default=0)
    max_price_range = max((p.price for p in products), default=0)

    print(min_price_range, max)

    paginator = Paginator(products, 6) 
    page_number = request.GET.get('page')
    paginated_products = paginator.get_page(page_number) 

    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    context = {
        "products" : products,
        "categories" : categories,
        "latest_products" : latest_products,
        "min_price" : min_price_range,
        "max_price" : max_price_range,
        "paginated_products" : paginated_products,
        "category" : category,
        "total_cart_items" : total_cart_items,
        "brands": set(p.brand_name for p in products),
        "nationalities": set(p.brand_nationality for p in products)
    }
    return render(request, 'GroceryApp/shop-grid.html', context)

def total_price_calc(cur_user):
    total_price_query = """
        SELECT SUM(p.price * ct.quantity) 
        FROM GroceryApp_product p 
        JOIN GroceryApp_cartorderitems ct ON ct.product_id = p.id 
        JOIN GroceryApp_cartorder co ON co.ct_ord_id = ct.order_id 
        WHERE co.order_status = 'processing' 
            AND ct.quantity > 0 
            AND co.user_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(total_price_query, [cur_user.id])
        total_price = cursor.fetchone()[0]

    return total_price

@login_required(login_url='/user/login/')
def calculate_total_price(request):
    cur_user = request.user
    total_price_view = total_price_calc(cur_user)
    return JsonResponse({'total_price_view': total_price_view})


def items_calc(cur_user):
    query = f"select count(p.id) from GroceryApp_product p join GroceryApp_cartorderitems ct on ct.product_id =p.id join GroceryApp_cartorder co on co.ct_ord_id= ct.order_id where co.order_status = 'processing' and ct.quantity >0 and co.user_id in (select id from userauths_user where id ='{cur_user.id}')"

    with connection.cursor() as cursor:
        cursor.execute(query)
        total_cart_items = cursor.fetchone()[0]
    return total_cart_items

@login_required(login_url='/user/login/')
def base_view(request):
    cur_user = request.user
    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    context ={
        "total_cart_items": total_cart_items,
        
    }
    return render(request, 'partials/base.html', context)

@login_required(login_url='/user/login/')
def items_in_cart_calc(request):
    cur_user = request.user


    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0
    return JsonResponse({'total_cart_items': total_cart_items})

@login_required(login_url='/user/login/')
def shopping_cart(request):
    cur_user = request.user

    user_shopping_cart = Product.objects.raw(f"select * from GroceryApp_product p join GroceryApp_cartorderitems ct on ct.product_id =p.id join GroceryApp_cartorder co on co.ct_ord_id= ct.order_id where co.order_status = 'processing' and ct.quantity >0 and co.user_id in (select id from userauths_user where id ='{cur_user.id}')")

    categories = Category.objects.raw("select * from GroceryApp_category")

    total_price = total_price_calc(cur_user)
    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    context = {
        "categories" : categories,
        "user_shopping_cart" : user_shopping_cart,
        "total_price": total_price,
        "total_cart_items" : total_cart_items, 
    }
    return render(request, 'GroceryApp/shoping-cart.html', context)





@login_required(login_url='/user/login/')
def wish_list(request):
    cur_user = request.user

    user_wishlist = Product.objects.raw(f"select * from GroceryApp_product p join GroceryApp_wishlist wl on wl.product_id =p.id where wl.user_id in (select id from userauths_user where id ='{cur_user.id}')")
    products = Product.objects.raw("select * from GroceryApp_product")

    items_cnt_query = f"select * from GroceryApp_product p join GroceryApp_wishlist wl on wl.product_id =p.id where wl.user_id in (select id from userauths_user where id ='{cur_user.id}')"

    with connection.cursor() as cursor:
        cursor.execute(items_cnt_query)
        wishlist_cnt = cursor.fetchone()[0]

    if cur_user.is_authenticated:
        total_cart_items = items_calc(cur_user)
    else:
        total_cart_items= 0

    context = {
        'user_wishlist' : user_wishlist,
        'products' :products,
        'wishlist_cnt' : wishlist_cnt, 
        "total_cart_items" :total_cart_items, 
    }
    return render(request, 'GroceryApp/wish-list.html', context)





def update_order(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get("order_id")
            new_quantity = request.POST.get("new_quantity")
            product_id = request.POST.get("product_id")
            print(f"New Quantity: {new_quantity}")
            print(f"order_id: {order_id}")
            query = f"update GroceryApp_cartorderitems set quantity = {new_quantity} where order_id = {order_id} and product_id = {product_id}"

            with connection.cursor() as cursor:
                cursor.execute(query)

            response_data = {'status': 'success', 'message': 'Order updated successfully'}
            return JsonResponse(response_data)

        except Exception as e:
            print(f"Error updating order: {e}")
            response_data = {'status': 'error', 'message': 'Failed to update order'}
            return JsonResponse(response_data, status=500)

    else:
        response_data = {'status': 'error', 'message': 'Method Not Allowed'}
        return JsonResponse(response_data, status=405)
    
def remove_order(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get("order_id")
            product_id = request.POST.get("product_id")        
            print(f"order_id: {order_id}")
            print(f"product_id: {product_id}")
            query = f"update GroceryApp_cartorderitems set quantity = {0} where order_id = {order_id} and product_id ={product_id}"

            with connection.cursor() as cursor:
                cursor.execute(query)
    
            response_data = {'status': 'success', 'message': 'Order updated successfully'}
            return JsonResponse(response_data)
    

        except Exception as e:
            print(f"Error updating order: {e}")
            response_data = {'status': 'error', 'message': 'Failed to update order'}
            return JsonResponse(response_data, status=500)

    else:
        response_data = {'status': 'error', 'message': 'Method Not Allowed'}
        return JsonResponse(response_data, status=405)
    

    
from django.http import JsonResponse

from django.views.decorators.http import require_POST

@login_required
def add_to_cart(request):  
    product_id = request.POST.get('id')
    quantity = int(request.POST.get('qty'))

    cart_order = CartOrder.objects.filter(user=request.user, paid_status=False, order_status= 'processing').first()
    # print(cart_order)

    if not cart_order:
        cart_order = CartOrder.objects.create(user=request.user, paid_status=False, order_status= 'processing')
        cart_order.save()

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartOrderItems.objects.get_or_create(order=cart_order, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.price = product.price
    cart_item.total = cart_item.price * cart_item.quantity
    cart_item.image = product.img
    cart_item.product_status = product.product_status

    cart_item.save()
    
    
    print("Cart item saved successfully")

    response_data = {'status': 'success', 'message': 'Order added successfully'}
    return JsonResponse(response_data)
  
@login_required(login_url='/user/login/')
def add_to_cart_view(request, product_id):
    cart_order = CartOrder.objects.filter(user=request.user, paid_status=False, order_status= 'processing').first()

    if not cart_order:
        cart_order = CartOrder.objects.create(user=request.user, paid_status=False, order_status= 'processing')
        cart_order.save()

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartOrderItems.objects.get_or_create(order=cart_order, product=product)

    quantity =1

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.price = product.price
    cart_item.total = cart_item.price * cart_item.quantity
    cart_item.image = product.img
    cart_item.product_status = product.product_status

    cart_item.save()

    return redirect('GroceryApp:shopping_cart') 

    