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
    path('shipped_dash', views.shipped_dash, name='shipped_dash'),      #To view shipped items in the dashboard
    path('not_shipped_dash', views.not_shipped_dash, name = 'not_shipped_dash'),    #To view unshipped items in the dashboard
    path('orders/<int:pk>/', views.orders, name= 'orders'),     #To view all the details of shipped as well as unshipped items in the dashboard
    path('booklist_dash/', views.booklist_dash, name='booklist_dash'),      #To view all the books in the dashboard
    path('add_book_dash/', views.add_book_dash, name='add_book_dash'),      #To add new books through the dashboard
    path('create_category_dash/', views.create_category_dash, name='create_category_dash'),     #To add new categories through the dashboard
    path('categorylist_dash/', views.categorylist_dash, name='categorylist_dash'),      #To view all the categories in the dashboard
    path('category_dash/<str:cat>/', views.category_dash, name='category_dash'),        #To view all the books in each categories in the dashboard
    path('userslist_dash/', views.userslist_dash, name= 'userslist_dash'),      #To view all the signedup users in the dashboard
    path('profile_dash/<int:pk>/', views.profile_dash, name= 'profile_dash'),       #To view profiles of all the signedup users in the dashboard
    path('order_dash/<int:user>/', views.order_dash, name= 'order_dash'),       #To view the orders of each signedup users in the dashboard
    path('customers_dash/', views.customers_dash, name= 'customers_dash'),      #To view all the customers in the dashboard
    path('customer_order_dash/<str:email>/', views.customer_order_dash, name= 'customer_order_dash'),
    path('orders_dash/', views.orders_dash, name= 'orders_dash'),       #To view all the orders in the dashboard
    path('orderin_dash/<int:pk>/', views.orderin_dash, name= 'orderin_dash'),       #To view the complete details of all the orders in the dashboard
]