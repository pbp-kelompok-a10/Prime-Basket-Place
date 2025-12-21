from django.shortcuts import render, redirect, get_object_or_404
from detail_product.models import Product
from .models import SliderProduct
from .forms import SliderProductForm
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from detail_product.models import Product
from django.contrib.auth.decorators import login_required
from account.decorators import admin_required

def show_json(request):
    # Mengambil semua produk yang sudah di-load ke database
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_main(request):
    product_catalog = Product.objects.all()
    slider_products = SliderProduct.objects.all()

    query = request.GET.get('q')
    search = request.GET.get('search')

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

    if search:
        product_catalog = product_catalog.filter(Q(name__icontains=search))

    context = {
        'product_catalog': product_catalog,
        'slider_products': slider_products,
    }
    return render(request, "homepage.html", context)

@login_required(login_url='account:login')
@admin_required
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

@login_required(login_url='account:login')
@admin_required
def delete_slider_product(request, id):
    product = get_object_or_404(SliderProduct, id=id)
    product.delete()
    return redirect('Homepage:manage_slider')
