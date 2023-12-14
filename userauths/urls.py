from django.urls import path
from userauths.views import *

app_name = "userauths"

urlpatterns = [
    path("register", register, name= 'register'),
    path("login/", login, name = 'login'),
    path("signout", logout_view, name = 'signout'),
    
]