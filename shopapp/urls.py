from django.urls import path
from .views import (ShopIndexView,
                    GroupsListView,
                    ProductDetailView, 
                    ProductsListView, 
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    ProductArchivedView,
                    OrdersListView,
                    OrderDetailView,
                    OrderCreateView,
                    OrderDeleteView,
                    OrderUpdateView,
                )       


#from shopapp.views import first_page

app_name = 'shopapp'

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('groups/', GroupsListView.as_view(), name ='groups-list'),
    path('products/', ProductsListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'), 
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/<int:pk>/archived/', ProductArchivedView.as_view(), name='product-archived'),
    path('orders/', OrdersListView.as_view(), name='order-list'),
    path('orders/create', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),

     
]