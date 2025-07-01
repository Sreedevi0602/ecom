from .wishlist import Wishlist

def wishlist(request):
    wishlist = Wishlist(request)
    return {
        'wishlist': wishlist.wishlist  # or just 'wishlist': wishlist to use its methods
    }
