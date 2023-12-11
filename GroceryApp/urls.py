from django.urls import path
from GroceryApp.views import index

app_name = "GroceryApp"

urlpatterns = [
    path("", index),
    ]