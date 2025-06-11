from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend our Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "phone", "shipping_address", "amount_paid", "date_ordered", "shipped"]
    inlines = [OrderItemInline]

#unregister order model
admin.site.unregister(Order)

#reregister Order and OrderAdmin
admin.site.register(Order, OrderAdmin)
