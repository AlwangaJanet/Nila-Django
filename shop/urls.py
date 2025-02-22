from django.contrib import admin
from django.urls import path,include
from .views import * 

urlpatterns = [

   
    path('homepage/', view_users,name='homepage'),
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('orders/',view_orders, name='view_orders'),
    path('new_product/',new_product, name='new_product'),
    path('add_or_update_product/',add_or_update_product, name='add_or_update_product'),
    path('products/', product_list, name='product_list'),
    path('pre_products/', Pre_product_list, name='pre_product_list'),
    #  path('new/', new_product, name='new_product'),
]
