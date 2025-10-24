from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import DetailForm
from reviews.models import Review 
from account.models import Account

def show_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('reviews__user'), pk=pk)
    form = DetailForm(instance=product)

    user_has_reviewed = False
    is_favorite = False 
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
        
        # Cek apakah produk ini ada di daftar favorit user
        account, created = Account.objects.get_or_create(user=request.user)
        is_favorite = product in account.favorites.all()

    context = {
        'product': product,
        'form': form,
        'user_has_reviewed': user_has_reviewed,
        'is_favorite': is_favorite, 
    }
    return render(request, 'detail_product/product_detail.html', context)

@login_required
def update_or_create_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = DetailForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
    return redirect('detail_product:show_detail', pk=pk)

@login_required
def delete_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.description = None
        product.save()
    return redirect('detail_product:show_detail', pk=pk)