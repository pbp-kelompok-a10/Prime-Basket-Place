from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import ProductForm
from detail_product.models import Product

def show_main(request):
    product_list = Product.objects.all()

    context = {
        'product_list': product_list
    }

    return render(request, "dashboard.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('dashboard:show_main')
    
    context = {
        'form' : form
    }
    
    return render(request, "create_product.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('dashboard:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('dashboard:show_main'))

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    context = {
        'product' : product
    }
    
    return render(request, "detail_product.html", context)