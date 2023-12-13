from django.urls import path
from userauths.views import *

app_name = "userauths"

urlpatterns = [
    path("", register),
    path("login", login)
    
]