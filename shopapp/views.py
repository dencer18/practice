from timeit import default_timer
from django.shortcuts import (
                            render, 
                            redirect, 
                            reverse, 
                            get_object_or_404
                            )
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse
from django.http import HttpRequest
from django.contrib.auth.models import Group
from .models import Product, Order
from .forms import (
                    GroupForm, 
                    ProductUpdateForm
                    )
#from django.views import View
from django.views.generic import (
                                View,
                                TemplateView, 
                                ListView,
                                FormView,
                                DetailView, 
                                CreateView,
                                UpdateView,
                                DeleteView,
                                )
#=========================================================
#1. Products
#=========================================================
class ProductsListView(ListView):
    model = Product
    context_object_name = "products"
    queryset = model.objects.filter(archived=False)

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"

class ProductCreateView(CreateView):
    model=Product
    fields="name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:product-list")    
    
class ProductUpdateView(UpdateView):
     model = Product
     fields="name", "price", "discount"
     template_name_suffix="_update_form"
     def get_success_url(self):
         return reverse(
             "shopapp:product-detail",
             kwargs={"pk": self.object.pk},
         )

class ProductArchivedView(DeleteView):
    model = Product
    template_name = 'shopapp/product_confirm_archive.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.archived = True
        self.object.save()
        return redirect(reverse('shopapp:product-detail', kwargs={'pk': self.object.pk}))

class ProductDeleteView(DeleteView):
    model = Product
    success_url =reverse_lazy("shopapp:product-list")

#=========================================================
#2. Orders
#=========================================================

class OrdersListView(ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderCreateView(CreateView):
    model=Order
    fields="delivery_adress", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:order-list") 

class OrderUpdateView(UpdateView):
    model = Order
    fields="delivery_adress", "promocode", "user", "products"
    template_name_suffix="_update_form"
    def get_success_url(self):
        return reverse(
             "shopapp:order-detail",
             kwargs={"pk": self.object.pk},
        )

class OrderDeleteView(DeleteView):
    model = Order
    #template_name = 'shopapp/order_confirm_delete.html'
    success_url =reverse_lazy("shopapp:order-list")


class ShopIndexView(View):
    def get(self, request: HttpRequest)-> HttpResponse:
        products =[
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartfhone', 999),
        ]

        context ={
            "time_running": default_timer(),
            "products": products,
        }

        return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context={"groups": Group.objects.prefetch_related('permissions').all()}
    return render(request, "shopapp/groups-list.html", context=context)


class GroupsListView(View):
    def get(self,  request: HttpRequest)-> HttpResponse:
        context={
            "form": GroupForm,
            "groups": Group.objects.prefetch_related('permissions').all(),
            }
        return render(request, "shopapp/groups-list.html", context=context)
    
    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

