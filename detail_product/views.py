from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import DetailForm

def show_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('reviews__user'), pk=pk)
    form = DetailForm(instance=product)
    context = { 'product': product, 'form': form }
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