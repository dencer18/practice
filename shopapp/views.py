from timeit import default_timer
from django.shortcuts import (
                            render, 
                            redirect, 
                            reverse, 
                            get_object_or_404
                            )
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse
from django.http import HttpRequest, JsonResponse
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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
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

class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required="shopapp.add_product" 
    model=Product
    fields="name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:product-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    fields="name", "price", "discount"
    template_name_suffix="_update_form"
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        self.object = self.get_object()
        has_edit_perm = self.request.user.has_perm("shopapp.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

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

class OrdersListView(LoginRequiredMixin,ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required="shopapp.view_order"
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


class ProductsDataExportView(View):
    def get(self, request: HttpRequest)-> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})


