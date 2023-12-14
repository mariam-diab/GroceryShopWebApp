from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

LoggedIN = False

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
    if request.method == 'POST':
         form = RegisterForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('/')
    else:
        form = RegisterForm()
        
    return render(request, 'userauths/register.html', {'form':form})


def logout_view(request):
    logout(request)
    messages.success(request, "You logged out successfully")
    return redirect("userauths:login")