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
from .forms import OrderForm, GroupForm
#from django.views import View
from django.views.generic import (
                                View,
                                TemplateView, 
                                ListView, 
                                DetailView, 
                                CreateView,
                                UpdateView,
                                DeleteView,
                                )


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


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"


class ProductUpdateView(UpdateView):
    model = Product
    fields="name", "price", "discount"
    template_name_suffix="_update_form"
    #success_url =reverse_lazy("shopapp:products-list")
    
    def get_success_url(self):
        return reverse(
            "shopapp:product-detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url =reverse_lazy("shopapp:products-list")


class ProductsListView(ListView):
    model = Product
    context_object_name = "products"
    queryset = model.objects.filter(archived=False)


class ProductCreateView(CreateView):
    model=Product
    fields="name", "price", "description", "discount"
    success_url =reverse_lazy("shopapp:products-list")


class ProductArchivedView(View):
    model = Product
    fields="archived",
    template_name_suffix="_archived_form"
    
    def get(self, request, *args, **kwargs):
        pass
#       form =  ProductForm()
    
#     context={
#             "form": form,
#             }
#     return render(request,"shopapp/create-product.html", context=context)

#         return HttpResponse("result")

    def post(self, request, *args, **kwargs):
        # p=Product.objects.Filter(id=id)
        # p.archived=True
        # p.save
        # return redirect()
        pass

    # def get_object(self):
    #     obj = super().get_object()
    #     obj.arhived = True
    #     obj.save()
    #     return obj

    # def get_success_url(self):
    #     return reverse(
    #         "shopapp:product-detail",
    #         kwargs={"pk": self.object.pk},
    #     )
    #queryset = model.objects.r(archived=False)

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


def create_order(request:HttpRequest)->HttpResponse():
    if request.method =="POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:orders-list')
            return redirect(url)
    else:
        form =  OrderForm()
    
    context={
            "form": form,
            }
    return render(request,"shopapp/create-order.html", context=context)


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