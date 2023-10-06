from django.urls import path
from . import views

#from shopapp.views import first_page

app_name = 'shopapp'

urlpatterns = [
    path('', views.shop_index, name='shop-index'),
    path('groups/', views.groups_list, name ='groups-list'),
    path('products/', views.products_list, name='products-list'),
    path('products/create/', views.create_product, name='product-create'), 
    path('orders/', views.orders_list, name='orders-list'),
    path('orders/create', views.create_order, name='order-create'),
     
]