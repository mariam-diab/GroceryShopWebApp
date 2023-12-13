from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect('/')

        else:
            messages.error(request, "Wrong email or password!")
            return render(request, 'userauths/login.html')
    else:
        return render(request, 'userauths/login.html')

def register(request):
    return render(request, 'userauths/register.html')
