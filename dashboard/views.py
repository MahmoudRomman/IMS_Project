from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection

# Create your views here.




# I use the following property(decorator) which is @login_required
# to not access any pages in the app before login or register
@login_required(login_url='user-login')
def index(request):
    orders = models.Order.objects.all()
    products = models.Product.objects.all()
    users_number = models.User.objects.count()
    products_number = models.Product.objects.count()
    orders_number = models.Order.objects.count()
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            order_name = form.cleaned_data.get('product')
            quantity_oredered = form.cleaned_data.get('order_quantity')

            with connection.cursor() as cursor:
                cursor.execute(f"select quantity from dashboard_product where name='{order_name}'")
                quantity_sotred = cursor.fetchone()
            quantity_sotred = quantity_sotred[0]
            
            if quantity_oredered <= quantity_sotred:
                new_quantity = quantity_sotred - quantity_oredered

                with connection.cursor() as cursor: 
                    cursor.execute(f"update dashboard_product set quantity={new_quantity} where name='{order_name}'")
                messages.success(request, 'Your order has been added successfully, thank you.')

                            
                instance = form.save(commit=False)
                instance.staff = request.user
                instance.save()
                return redirect('dashboard-index')
            elif quantity_sotred == 0:
                messages.warning(request, f" Sorry, Your order, '{order_name}' is out of order right now!")
            else:
                messages.warning(request, f" Sorry, Your order, '{order_name}' has only amount of {quantity_sotred}.")
   
    else:
        form = forms.OrderForm()
    
    context = {
        'orders' : orders,
        'products' : products,
        'users_number' : users_number,
        'products_number' : products_number,
        'orders_number' : orders_number,
        'form' : form,
    }
    return render(request, 'dashboard/index.html', context)

    
@login_required(login_url='user-login')
def staff(request):
    workers = User.objects.all()
    users_number = models.User.objects.count()
    products_number = models.Product.objects.count()
    orders_number = models.Order.objects.count()
    context = {
        'workers' : workers,
        'users_number' : users_number,
        'products_number' : products_number,
        'orders_number' : orders_number,
    }
    return render(request, 'dashboard/staff.html', context)


@login_required(login_url='user-login')
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context = {
        'workers' : workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)



@login_required(login_url='user-login')
def product(request):
    items = models.Product.objects.all()    # Using ORM
    # items = models.Product.objects.raw('select * from dashboard_product')

    users_number = models.User.objects.count()
    products_number = models.Product.objects.count()
    orders_number = models.Order.objects.count()

    if request.method == "POST":
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')
    else:
        form = forms.ProductForm()

    context = {
        'items': items,
        'form' : form,
        'users_number' : users_number,
        'products_number' : products_number,
        'orders_number' : orders_number,
    }
    return render(request, 'dashboard/product.html', context)


# pk is the primary key which i use to delete the product by..
@login_required(login_url='user-login')
def product_delete(request, pk):
    item = models.Product.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')



# pk is the primary key which i use to update the product by..
@login_required(login_url='user-login')
def product_update(request, pk):
    item = models.Product.objects.get(id=pk)
    if request.method == "POST":
        form = forms.ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = forms.ProductForm(instance=item)
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/product_update.html', context)



@login_required(login_url='user-login')
def order(request):
    orders = models.Order.objects.all()
    users_number = models.User.objects.count()
    products_number = models.Product.objects.count()
    orders_number = models.Order.objects.count()
    context = {
        'orders' : orders,
        'users_number' : users_number,
        'products_number' : products_number,
        'orders_number' : orders_number,
    }
    return render(request, 'dashboard/order.html', context)





#     #################################################################################




# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from . import models
# from . import forms
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.db import connection

# # Create your views here.




# # I use the following property(decorator) which is @login_required
# # to not access any pages in the app before login or register
# @login_required(login_url='user-login')
# def index(request):
#     orders = models.Order.objects.all()
#     products = models.Product.objects.all()
#     users_number = models.User.objects.count()
#     products_number = models.Product.objects.count()
#     orders_number = models.Order.objects.count()


#     order_name = form.cleaned_data.get('product')
#     quantity_oredered = form.cleaned_data.get('order_quantity')

#     with connection.cursor() as cursor:
#         cursor.execute(f"select quantity from dashboard_product where name='{order_name}'")
#         quantity_sotred = cursor.fetchone()
#     quantity_sotred = quantity_sotred[0]
            
#     if quantity_oredered <= quantity_sotred:
#         new_quantity = quantity_sotred - quantity_oredered

#         connection.cursor() 
#         cursor.execute(f"update dashboard_product set quantity={new_quantity} where name='{order_name}'")
#         cursor.commit()
#         cursor.close()

#         if request.method == "POST":
#             form = forms.OrderForm(request.POST)
#             if form.is_valid():                
#                 instance = form.save(commit=False)
#                 instance.staff = request.user
#                 instance.save()
#                 return redirect('dashboard-index')
#         else:
#             form = forms.OrderForm()
#     else:
#         messages.warning(request, f'{order_name} has only amount of {quantity_sotred}')


#     context = {
#         'orders' : orders,
#         'products' : products,
#         'users_number' : users_number,
#         'products_number' : products_number,
#         'orders_number' : orders_number,
#         'form' : form,
#     }
#     return render(request, 'dashboard/index.html', context)

    
# @login_required(login_url='user-login')
# def staff(request):
#     workers = User.objects.all()
#     users_number = models.User.objects.count()
#     products_number = models.Product.objects.count()
#     orders_number = models.Order.objects.count()
#     context = {
#         'workers' : workers,
#         'users_number' : users_number,
#         'products_number' : products_number,
#         'orders_number' : orders_number,
#     }
#     return render(request, 'dashboard/staff.html', context)


# @login_required(login_url='user-login')
# def staff_detail(request, pk):
#     workers = User.objects.get(id=pk)
#     context = {
#         'workers' : workers,
#     }
#     return render(request, 'dashboard/staff_detail.html', context)



# @login_required(login_url='user-login')
# def product(request):
#     items = models.Product.objects.all()    # Using ORM
#     # items = models.Product.objects.raw('select * from dashboard_product')

#     users_number = models.User.objects.count()
#     products_number = models.Product.objects.count()
#     orders_number = models.Order.objects.count()

#     if request.method == "POST":
#         form = forms.ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             product_name = form.cleaned_data.get('name')
#             messages.success(request, f'{product_name} has been added')
#             return redirect('dashboard-product')
#     else:
#         form = forms.ProductForm()

#     context = {
#         'items': items,
#         'form' : form,
#         'users_number' : users_number,
#         'products_number' : products_number,
#         'orders_number' : orders_number,
#     }
#     return render(request, 'dashboard/product.html', context)


# # pk is the primary key which i use to delete the product by..
# @login_required(login_url='user-login')
# def product_delete(request, pk):
#     item = models.Product.objects.get(id=pk)
#     if request.method == "POST":
#         item.delete()
#         return redirect('dashboard-product')
#     return render(request, 'dashboard/product_delete.html')



# # pk is the primary key which i use to update the product by..
# @login_required(login_url='user-login')
# def product_update(request, pk):
#     item = models.Product.objects.get(id=pk)
#     if request.method == "POST":
#         form = forms.ProductForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard-product')
#     else:
#         form = forms.ProductForm(instance=item)
#     context = {
#         'form' : form,
#     }
#     return render(request, 'dashboard/product_update.html', context)



# @login_required(login_url='user-login')
# def order(request):
#     orders = models.Order.objects.all()
#     users_number = models.User.objects.count()
#     products_number = models.Product.objects.count()
#     orders_number = models.Order.objects.count()
#     context = {
#         'orders' : orders,
#         'users_number' : users_number,
#         'products_number' : products_number,
#         'orders_number' : orders_number,
#     }
#     return render(request, 'dashboard/order.html', context)