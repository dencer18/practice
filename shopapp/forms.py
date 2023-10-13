from django import forms
from django.core import validators
from .models import Product, Order
from django.forms import ModelForm
from django.contrib.auth.models import Group
    

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields="delivery_adress", "promocode", "user", "products"

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


    