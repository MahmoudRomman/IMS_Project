from django.contrib import admin
from . import models
from django.contrib.auth.models import Group


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity')
    list_filter = ['category']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order)
#admin.site.unregister(Group)


