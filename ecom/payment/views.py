from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages



# Create your views here.
def process_order(request):
    if request.POST:

        #get the cart
        cart=Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals= cart.cart_total()

        #get billing info from prev. page
        payment_form = PaymentForm(request.POST or None)
        #get shipping session data
        my_shipping = request.session.get('my_shipping')
        

        #get order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        phone = my_shipping['shipping_phone']
        

        #create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_district']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            
            #logged in user
            user = request.user
            #create order
            create_order = Order(user=user, full_name=full_name, email=email, phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request, 'Order Placed Successfully')
            return redirect('home')
        else:
            #guest user
            create_order = Order(full_name=full_name, email=email,  phone=phone, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request, 'Order Placed Successfully')
            return redirect('home')


    else:
        messages.success(request, 'Access to this page has been denied')
        return redirect('home')



def billing_info(request):
    if request.POST:
        #get the cart
        cart=Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals= cart.cart_total()

        #create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #logged in user
        if request.user.is_authenticated:
            #get billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals': totals, 'shipping_info': request.POST, "billing_form": billing_form})

        else:
            #Guest user
            #get billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities':quantities, 'totals': totals, 'shipping_info': request.POST, "billing_form": billing_form})

        

    else:
        messages.success(request, "Access to this page has been denied.")
        return redirect("home")
    
   




def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    cart=Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals= cart.cart_total()

    if request.user.is_authenticated:
        #checkout as a logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request,'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'totals': totals, 'shipping_form': shipping_form})


    else:
        #checkout as a guest user
        shipping_form = ShippingForm(request.POST or None)

        return render(request,'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'totals': totals, 'shipping_form': shipping_form})


