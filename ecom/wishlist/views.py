from django.shortcuts import render, get_object_or_404
from .wishlist import Wishlist
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def wishlist_summary(request):
    #Get wishlist
    wishlist=Wishlist(request)
    wishlist_products=wishlist.get_prods

    return render(request,'wishlist_summary.html', {'wishlist_products':wishlist_products})


def wishlist_add(request):
    #get the wishlist
    wishlist=Wishlist(request)

    #test for post
    if request.POST.get('action')=='post':
        #get stuff
        product_id=int(request.POST.get('product_id'))
        #lookup for product in DB
        product=get_object_or_404(Product,id=product_id)

        #Save to session
        wishlist.add(product)


        #Get cart quantity
        wishlist_length=wishlist.__len__()
        response=JsonResponse({'len': wishlist_length})

        #Return response
        #response = JsonResponse({'Product Name:':product.name})
        messages.success(request, ('Wishlisted'))
        return response


def wishlist_delete(request):
    # Get the wishlist
    wishlist = Wishlist(request)

    # Test for POST
    if request.POST.get('action') == 'post':
        # Get product ID from request
        product_id = int(request.POST.get('product_id'))
        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Remove from wishlist
        wishlist.delete(product)

        # Get updated wishlist length
        wishlist_length = wishlist.__len__()
        response = JsonResponse({'len': wishlist_length})

        # Add success message
        messages.success(request, ('Removed from Wishlist'))

        return response
    

def wishlist_delete(request):
    wishlist=Wishlist(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id= int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)

        #Call delete function in wishlist
        wishlist.delete(product)
        response=JsonResponse({'product': product_id})

        # Get updated wishlist length
        wishlist_length = wishlist.__len__()
        response = JsonResponse({'len': wishlist_length})

        messages.success(request, ('Item Deleted from Your Cart'))

        return response
