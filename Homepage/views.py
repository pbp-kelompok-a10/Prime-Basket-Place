# Homepage/views.py

from django.shortcuts import render, redirect, get_object_or_404
from detail_product.models import Product
from .models import SliderProduct
from .forms import SliderProductForm
from django.db.models import Q

def show_main(request):
    product_catalog = Product.objects.all()
    slider_products = SliderProduct.objects.all()

    query = request.GET.get('q')

    if query:
        query = query.lower()
        if query == 'men':
            product_catalog = product_catalog.filter(
                Q(name__icontains='men') | Q(name__icontains='unisex')
            )
        elif query == 'women':
            product_catalog = product_catalog.filter(
                Q(name__icontains='women') | Q(name__icontains='unisex')
            )
        else:
            product_catalog = product_catalog.filter(name__icontains=query)

    context = {
        'product_catalog': product_catalog,
        'slider_products': slider_products,
    }
    return render(request, "homepage.html", context)

def manage_slider(request):
    slider_products = SliderProduct.objects.all()

    if request.method == 'POST':
        form = SliderProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Homepage:manage_slider')
        
    else:
        form = SliderProductForm

    context = {
        'form': form,
        'slider_products': slider_products,
    }
    return render(request, 'manage_slider.html', context)

def delete_slider_product(request, id):
    product = get_object_or_404(SliderProduct, id=id)
    product.delete()
    return redirect('Homepage:manage_slider')