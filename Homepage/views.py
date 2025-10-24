from django.shortcuts import render
from detail_product.models import Product
from .models import SliderProduct

def show_main(request):
    product_catalog = Product.objects.all() #TODO

    slider_products = SliderProduct.objects.all()

    context = {
        'product_catalog': product_catalog,
        'slider_products': slider_products,
    }
    return render(request, "homepage.html", context)
