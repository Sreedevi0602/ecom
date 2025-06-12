from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

# Create your views here.

#Dashboard
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        order = Order.objects.get(id=pk)
        #get order items
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'orders.html', {"order": order, "items": items})
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')



def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "not_shipped_dash.html", {"orders": orders})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "shipped_dash.html", {"orders": orders})

    else:
        messages.success(request, 'Access has been denied to this page')
        return redirect('home')









def search(request):
    #Determine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']

        #Queuing the Product model
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(author__icontains = searched) | Q(category__name__icontains = searched) )

        #test for null
        if not searched:
            messages.success(request, 'No Result Found')
            return render(request, 'search.html', {})
        
        else:
            return render(request, 'search.html',{'searched': searched})
        
    else:
        return render(request,'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        #current user
        current_user = Profile.objects.get(user__id=request.user.id)
        #current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #get original user form
        info_form = UserInfoForm(request.POST or None, instance=current_user)
        #get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if info_form.is_valid() or shipping_form.is_valid():
            info_form.save()
            shipping_form.save()
            messages.success(request, 'Your Details Have Been Updated Successfully')
            return redirect('home')
        
        return render(request, 'update_info.html', {'info_form': info_form, 'shipping_form': shipping_form})
    
    else:
        messages.success(request, 'You need to Sign Up to have Access to This Page')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        #If they fillout the form and click the button
        if request.method == 'POST':
            password_form = ChangePasswordForm(current_user, request.POST)

            #If the form is valid
            if password_form.is_valid():
                password_form.save()
                messages.success(request,'Password Updated Successfully')
                login(request, current_user)
                return redirect('home')
            
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
                
        else:
            password_form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'password_form': password_form})

    else:
        messages.success(request,'You need to Sign Up to have Access to This Page')
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request,'Your Profile has been Updated Successfully')
            return redirect('home')
    
        return render(request, 'update_user.html', {'user_form': user_form})
    
    else:
        messages.success(request, 'You need to Sign Up to have Access to This Page')
        return redirect('home')


def category_summary(request):
    categories= Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

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

            #shopping cart - pulling it from db
            current_user = Profile.objects.get(user__id = request.user.id)

            #get their saved cart from db
            saved_cart = current_user.old_cart

            #convert db string to dictionary
            if saved_cart:
                #convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                #add the loaded cart dictionary to session
                cart = Cart(request)

                #loop throgh the cart and additems form db
                for key, value in converted_cart.items():
                    cart.db_add(product = key, quantity = value)

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
            messages.success(request, ("Registration Completed Successfully. You Are Now Logged into Your Account. Please Fill Out Your Billing Info"))
            return redirect('update_info')
        
        else:
            messages.success(request,"Something Went wrong with Registration. Please Try again")
            return redirect('register')

    else:
        return render(request, 'register.html', {"form": form})