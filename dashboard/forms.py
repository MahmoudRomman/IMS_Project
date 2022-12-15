from django import forms
from . import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['product', 'order_quantity']

