from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import *

# Create your views here.
def category(request, cat):
    cat = cat.replace('_', ' ')

    #Grab category from url
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category': category})
    
    except:
        messages.success(request, ('Category Does Not Exist'))
        return redirect('home')
    

def product(request, pk):
    product= Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("Login Completed Successfully"))
            return redirect('home')
        
        else:
            messages.success(request, ("Something Went Wrong. Please Try Again"))
            return redirect('login')
        
    else:    

        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been Logged Out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #Login User
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("Registration Completed Successfully. You Are Now Logged into Your Account"))
            return redirect('home')
        
        else:
            messages.success(request,"Something Went wrong with Registration. Please Try again")
            return redirect('register')

    else:
        return render(request, 'register.html', {"form": form})