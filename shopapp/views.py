from timeit import default_timer
from django.shortcuts import render
from django.shortcuts import HttpResponse

def page1(request: HttpResponse):
    print("Path -",request.path)
    return   HttpResponse("<h1>Hello World</h1>") 

def page2(request):
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

