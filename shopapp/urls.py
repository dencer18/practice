from django.urls import path
from . import views
from .views import groups_list

#from shopapp.views import first_page

app_name = 'shopapp'

urlpatterns = [
    path('', views.shop_index, name='shop-index'),
    path('groups/', groups_list, name ='groups-list'),
    path('products/', views.products_list, name='products-list'),
    path('orders/', views.orders_list, name='orders-list'),   
]