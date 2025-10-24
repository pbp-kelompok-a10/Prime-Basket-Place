from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Review
from .forms import ReviewForm
from detail_product.models import Product 


@login_required
def create_review(request, product_id):
    """Membuat review baru untuk produk tertentu."""
    product = get_object_or_404(Product, id=product_id)

    # Cegah user yang sudah pernah review produk ini
    existing = Review.objects.filter(product=product, user=request.user).first()
    if existing:
        messages.warning(request, "Kamu sudah pernah memberi review untuk produk ini.")
        return redirect('detail_product:show_detail', pk=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review berhasil dikirim!")
            return redirect('detail_product:show_detail', pk=product.id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
        'title': 'Tulis Review',
    }
    return render(request, 'reviews/review_form.html', context)


@login_required
def update_review(request, pk):
    """Mengedit review milik user."""
    review = get_object_or_404(Review, pk=pk)

    # Cegah update review orang lain
    if review.user != request.user:
        return HttpResponseForbidden("Kamu tidak punya izin untuk mengedit review ini.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review berhasil diperbarui.")
            return redirect('detail_product:show_detail', pk=review.product.id)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'title': 'Edit Review',
    }
    return render(request, 'reviews/review_form.html', context)


@login_required
def delete_review(request, pk):
    """Menghapus review milik user."""
    review = get_object_or_404(Review, pk=pk)

    # Cegah hapus review orang lain
    if review.user != request.user:
        return HttpResponseForbidden("Kamu tidak punya izin untuk menghapus review ini.")

    if request.method == 'POST':
        product_id = review.product.id
        review.delete()
        messages.success(request, "Review berhasil dihapus.")
        return redirect('detail_product:show_detail', pk=product_id)

    context = {
        'review': review,
        'title': 'Hapus Review',
    }
    return render(request, 'reviews/review_confirm_delete.html', context)
