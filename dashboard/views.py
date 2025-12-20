from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from .forms import ProductForm
from detail_product.models import Product
from account.models import Account
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import requests, json

@login_required(login_url=reverse_lazy('account:login'))
def show_main(request):
    if request.user.is_superuser:
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)
        
    account, _ = Account.objects.get_or_create(user=request.user)
    is_favorite = account.favorites.all()

    context = {'product_list': product_list, 'is_favorite': is_favorite}
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
    
    if not request.user.is_staff and product.user != request.user:
        messages.error(request, "You don't have permission to edit this product.")
        return redirect('dashboard:show_main')
    
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

# def show_product(request, id):
#     product = get_object_or_404(Product, pk=id)
    
#     context = {
#         'product' : product
#     }
    
#     return render(request, "detail_product.html", context)

def show_json_dashboard(request):
    product_list = Product.objects.filter(user=request.user)
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method != 'POST':
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"},
            status=405
        )

    try:
        data = json.loads(request.body)
        fields = data.get("fields", {})

        name = strip_tags(fields.get("name", ""))
        brand = strip_tags(fields.get("brand", ""))
        category = fields.get("category", "Other")
        price = fields.get("price", 0)
        image_url = fields.get("image_url", "")
        description = strip_tags(fields.get("description", ""))

        product = Product.objects.create(
            name=name,
            brand=brand,
            category=category,
            price=price,
            image_url=image_url,
            description=description,
            user=request.user if request.user.is_authenticated else None
        )

        return JsonResponse(
            {
                "status": "success",
                "product_id": product.pk
            },
            status=201
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status=400
        )