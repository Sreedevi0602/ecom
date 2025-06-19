from django .urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name = 'update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('shop/', views.shop, name= 'shop'),
    path('category_summary/', views.category_summary, name = 'category_summary'),
    path('search/', views.search, name = 'search'),



    #dashboard
    path('shipped_dash', views.shipped_dash, name='shipped_dash'),
    path('not_shipped_dash', views.not_shipped_dash, name = 'not_shipped_dash'),
    path('orders/<int:pk>/', views.orders, name= 'orders'),
    path('booklist_dash/', views.booklist_dash, name='booklist_dash'),
    path('add_book_dash/', views.add_book_dash, name='add_book_dash'),
    path('create_category_dash/', views.create_category_dash, name='create_category_dash'),
    path('categorylist_dash/', views.categorylist_dash, name='categorylist_dash'),
    path('category_dash/<str:cat>/', views.category_dash, name='category_dash'),
    path('userslist_dash/', views.userslist_dash, name= 'userslist_dash'),
    path('profile_dash/<int:pk>/', views.profile_dash, name= 'profile_dash'),
    path('order_dash/<int:user>/', views.order_dash, name= 'order_dash'),
    path('customers_dash/', views.customers_dash, name= 'customers_dash'),
]