from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from .models import Review
from .forms import ReviewForm
from detail_product.models import Product
import json

@login_required
def create_review(request, product_id):
    """Membuat review baru untuk produk tertentu."""
    product = get_object_or_404(Product, id=product_id)
    
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

def get_reviews_json(request, product_id):
    """API endpoint untuk mendapatkan semua review produk (untuk Flutter)"""
    reviews = Review.objects.filter(product_id=product_id).select_related('user', 'product').order_by('-created_at')
    review_list = []
    
    for review in reviews:
        review_data = {
            'id': str(review.id),
            'user_name': review.user.username if review.user else 'Anonymous',
            'rating': review.rating,
            'comment': review.comment,
            'images': [request.build_absolute_uri(review.photo.url)] if review.photo else [],
            'created_at': review.created_at.isoformat(),
        }
        review_list.append(review_data)
    
    return JsonResponse(review_list, safe=False)

def get_review_stats_json(request, product_id):
    """API endpoint untuk mendapatkan statistik review produk (untuk Flutter)"""
    reviews = Review.objects.filter(product_id=product_id)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    stats = {
        'average_rating': round(float(avg_rating), 1) if avg_rating else 0.0,
        'total_reviews': reviews.count(),
    }
    return JsonResponse(stats)

@csrf_exempt
def create_review_flutter(request, product_id):
    """API endpoint untuk membuat review dari Flutter - REQUIRES AUTHENTICATION"""
    
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid method'
        }, status=405)
    
    # CRITICAL: Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required. Please login first.'
        }, status=401)
    
    try:
        data = json.loads(request.body)
        
        # Validasi product exists
        product = get_object_or_404(Product, id=product_id)
        
        # Cek apakah user sudah pernah review produk INI
        existing = Review.objects.filter(
            product=product,
            user=request.user
        ).first()
        
        if existing:
            return JsonResponse({
                'status': 'error',
                'message': 'Kamu sudah pernah memberi review untuk produk ini.'
            }, status=400)
        
        # Validasi rating
        rating = data.get('rating')
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return JsonResponse({
                'status': 'error',
                'message': 'Rating must be between 1 and 5'
            }, status=400)
        
        # Validasi comment
        comment = data.get('comment', '').strip()
        if not comment:
            return JsonResponse({
                'status': 'error',
                'message': 'Comment cannot be empty'
            }, status=400)
        
        # Buat review baru
        review = Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment,
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Review created successfully',
            'review_id': review.id,
            'product_id': product.id,
            'user': request.user.username,
        }, status=201)
        
    except Product.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Product not found'
        }, status=404)
    except KeyError as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Missing required field: {str(e)}'
        }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }, status=500)