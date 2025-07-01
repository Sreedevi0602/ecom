import json
from store.models import Product, Profile


class Wishlist:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # get wishlisted product ids or initialize empty list
        wishlist = self.session.get('wishlist')

        if 'wishlist' not in request.session:
            wishlist = self.session['wishlist'] = []

        #Filter out invalid product ids
        self.wishlist = []

        for product_id in wishlist:
            try:
                Product.objects.get(id=product_id)
                self.wishlist.append(product_id)
            except Product.DoesNotExist:
                continue

        #Update session
        self.session['wishlist'] = self.wishlist
        self.session.modified = True


    def add(self,product):
        product_id=str(product.id)
        

        #Logic
        if product_id in self.wishlist:
            pass

        else:
            self.wishlist.append(product_id)
            self.session['wishlist'] = self.wishlist

            self.session.modified = True

            #Deal with logged in user
            if self.request.user.is_authenticated:
                #get current user profile
                current_user = Profile.objects.filter(user = self.request.user).first()
                if current_user:
                    current_user.old_wishlist = json.dumps(self.wishlist)
                    current_user.save()
            

           


    def __len__(self):
        return len(self.wishlist)
    

    def get_prods(self):
        return Product.objects.filter(id__in=self.wishlist)
    

    def delete(self, product):
            product_id = str(product.id)

            # Logic
            if product_id in self.wishlist:
                self.wishlist.remove(product_id)
                self.session['wishlist'] = self.wishlist
                self.session.modified = True

                # Deal with logged in user
                if self.request.user.is_authenticated:
                    current_user = Profile.objects.filter(user=self.request.user).first()
                    if current_user:
                        current_user.old_wishlist = json.dumps(self.wishlist)
                        current_user.save()



        
    