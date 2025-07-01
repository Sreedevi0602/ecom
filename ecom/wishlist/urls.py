from django.urls import path
from . import views

urlpatterns = [
    path('wishlist_summary/', views.wishlist_summary, name = 'wishlist_summary'),
    path('wishlist_add/', views.wishlist_add, name = 'wishlist_add'),
    path('wishlist_delete/', views.wishlist_delete, name = 'wishlist_delete')
]