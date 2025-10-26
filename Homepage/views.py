# Homepage/views.py

from django.shortcuts import render
from detail_product.models import Product
from .models import SliderProduct
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