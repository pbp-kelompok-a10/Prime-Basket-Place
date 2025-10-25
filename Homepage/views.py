from django.shortcuts import render
from detail_product.models import Product
from .models import SliderProduct
from django.db.models import Q

def show_main(request):
    product_catalog = Product.objects.all()
    slider_products = SliderProduct.objects.all()

    # Ambil kata kunci filter dari URL, contoh: /?q=men
    query = request.GET.get('q')

    if query:
        # Ubah query menjadi huruf kecil untuk konsistensi
        query = query.lower()
        if query == 'men':
            # Jika query 'men', tampilkan produk 'men' ATAU 'unisex'
            product_catalog = product_catalog.filter(
                Q(name__iregex=r'\bmen\b') | Q(name__iregex=r'\bunisex\b')
            )
        elif query == 'women':
            # Jika query 'women', tampilkan produk 'women' ATAU 'unisex'
            product_catalog = product_catalog.filter(
                Q(name__iregex=r'\bwomen\b') | Q(name__iregex=r'\bunisex\b')
            )
        else:
            # Untuk query lain seperti 'kids', cari kata kunci yang cocok
            product_catalog = product_catalog.filter(name__iregex=r'\b{}\b'.format(query))

    context = {
        'product_catalog': product_catalog,
        'slider_products': slider_products,
    }
    return render(request, "homepage.html", context)