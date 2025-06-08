from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    shipping_full_name = models.CharField(max_length=300)
    shipping_email = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    shipping_address1 = models.CharField(max_length=500)
    shipping_address2 = models.CharField(max_length=500, null=True, blank=True)
    shipping_city = models.CharField(max_length=200)
    shipping_district = models.CharField(max_length=200)
    shipping_state = models.CharField(max_length=200)
    shipping_zipcode = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=200)

    #To not pluralize the address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
#create a user shipping address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user = instance)
        user_shipping.save()

#To automate the user shipping address thing
post_save.connect(create_shipping, sender=User)
    

#order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    full_name=models.CharField(max_length=300)
    email=models.EmailField(max_length=250)
    phone=models.CharField(max_length=20)
    ShippingAddress=models.CharField(max_length=10000)
    amount_paid=models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
    

#Order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'