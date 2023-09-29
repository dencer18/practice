from timeit import default_timer
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.contrib.auth.models import Group
from .models import Product
from .models import Order

def page1(request: HttpResponse):
    print("Path -",request.path)
    return   HttpResponse("<h1>Hello World</h1>") 

def shop_index(request:HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartfon', 999)
    ]
    context ={
        "time_runing": default_timer(),
        "products":products,
    }
    return   render(request, "shopapp/shop-index.html", context=context)

def groups_list(request: HttpRequest):
    context={"groups": Group.objects.prefetch_related('permissions').all()}
    return render(request, "shopapp/groups-list.html", context=context)


def products_list(request:HttpRequest):
    context={"products": Product.objects.all()}
    return render(request, "shopapp/product-list.html", context=context)

def orders_list(request:HttpRequest):
    context={
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, "shopapp/order-list.html", context=context)