from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

#Create User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=500, blank=True)
    address2 = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=900, blank=True, null=True)

    def __str__(self):
        return self.user.username
    

#Create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance) #connecting the Profile model and the User model
        user_profile.save()

#Automate the profile thing
post_save.connect(create_profile, sender=User)



#Categories of Books
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/category', default='uploads/category/nonfiction.jpg')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

#Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


#All the products
class Product(models.Model):
    book_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    stock = models.IntegerField(null=True, blank=False, default=0)
    description = models.TextField(max_length=1000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product')
    # Add sale icon
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=9)

    def __str__(self):
        return self.name
    

#Customer orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=200, default='', blank='True')
    phone = models.CharField(max_length=10, default='', blank='True')
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product