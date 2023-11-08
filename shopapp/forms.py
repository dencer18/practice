from django import forms
from django.core import validators
from .models import Product
from django.forms import ModelForm
from django.contrib.auth.models import Group
    


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "discount"]


    