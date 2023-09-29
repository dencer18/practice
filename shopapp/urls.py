from django.urls import path
from . import views
from .views import groups_list

#from shopapp.views import first_page

app_name = 'shopapp'

urlpatterns = [
    path('', views.shop_index, name='shop_index'),
    path('groups/', groups_list, name ='groups_list'),
    path('products/', views.products_list, name='products_list'),
    path('orders/', views.orders_list, name='orders_list'),   
]