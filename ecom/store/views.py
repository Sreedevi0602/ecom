from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
import datetime

# Create your views here.

#Dashboard
def customer_order_dash(request, email):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(email=email)
        items = OrderItem.objects.filter(order__in=orders)
        return render(request, 'customer_order_dash.html', {'orders': orders, 'items': items})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def orderin_dash(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        order = Order.objects.get(id=pk)
        #get order items
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'orderin_dash.html', {"order": order, "items": items})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def orders_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all()
        return render(request, 'orders_dash.html', {'orders': orders})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def customers_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        all_orders = Order.objects.order_by('-date_ordered')  # latest first

        seen_emails = set()
        unique_orders = []
        customer_email = []

        for order in all_orders:
            if order.email not in seen_emails:
                unique_orders.append(order)
                customer_email.append(order.email)
                seen_emails.add(order.email)

        return render(request, 'customers_dash.html', {'orders': unique_orders, 'email': customer_email})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def order_dash(request, user):
    if request.user.is_authenticated and request.user.is_superuser:
        user_instance = get_object_or_404(User, id=user)

        orders = Order.objects.filter(user=user_instance)
        items = OrderItem.objects.filter(order__in=orders)

        return render(request, 'order_dash.html', {'orders': orders, 'user_instance': user_instance, 'items': items})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def profile_dash(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        profile = Profile.objects.get(id=pk)
        return render(request, 'profile_dash.html', {'profile': profile})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def userslist_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.all()
        user_data = []
        

        for user in users:
            profile = Profile.objects.filter(user=user).first()
            has_orders = Order.objects.filter(user=user).exists()
            user_data.append({
                'user': user, 
                'profile': profile,
                'has_orders': has_orders
            })
            
            
            
        return render(request, 'userslist_dash.html', {'user_data': user_data})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def category_dash(request, cat):
    if request.user.is_authenticated and request.user.is_superuser:
        cat = cat.replace('_', ' ')

        #Grab category from url
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category_dash.html', {'products':products, 'category': category})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')
    


def categorylist_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        categories = Category.objects.all()
        return render(request, 'categorylist_dash.html', {'categories': categories})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def create_category_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            cat_form = CategoryForm(request.POST, request.FILES)
            if cat_form.is_valid():
                cat_form.save()
                return redirect('create_categories')
        else:
            cat_form = CategoryForm()
        return render(request, 'create_category_dash.html', {'cat_form': cat_form})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def add_book_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            book_form = BooksForm(request.POST, request.FILES)
            if book_form.is_valid():
                book_form.save()
                return redirect('booklist_dash')  
        else:
            book_form = BooksForm()
        
        return render(request, 'add_book_dash.html', {'book_form': book_form})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def booklist_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        books = Product.objects.all()
        return render(request, 'booklist_dash.html', {'books': books})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get the order
        order = Order.objects.get(id=pk)
        #get order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            #check if true or false
            if status == "true":
                #get the order
                order = Order.objects.filter(id=pk)
                #update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                #get the order
                order = Order.objects.filter(id=pk)
                #update the status
                
                order.update(shipped=False)

            messages.success(request, "Shipping status updated")
            return redirect('home')

        return render(request, 'orders.html', {"order": order, "items": items})
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')



def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            #get the order
            order = Order.objects.filter(id=num)
            #update the status
            now = datetime.datetime.now()
            #update the order
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping status updated")
            return redirect('home')
        
        return render(request, "not_shipped_dash.html", {"orders": orders})
    
    else:
        messages.success(request, 'Access denied to this page')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            #get the order
            order = Order.objects.filter(id=num)
            #update the status
            now = datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request, "Shipping status updated")
            return redirect('home')

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