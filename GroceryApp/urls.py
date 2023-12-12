from django.urls import path
from GroceryApp.views import *

app_name = "GroceryApp"

urlpatterns = [
    path("", index),
    path("checkout", checkout),
    path("contact", contact),
    path("shop_details", shop_details),
    path("shop_grid", shop_grid),
    path("shopping_cart",shopping_cart),
    ]