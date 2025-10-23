from django.urls import path
from .views import show_detail, update_or_create_detail, delete_detail

app_name = 'detail_product'

urlpatterns = [
    # URL untuk menampilkan detail produk
    path('product/<int:pk>/', show_detail, name='show_detail'),
    
    # URL untuk memproses form Create atau Update
    path('product/<int:pk>/update/', update_or_create_detail, name='update_or_create_detail'),

    # URL untuk menghapus deskripsi
    path('product/<int:pk>/delete/', delete_detail, name='delete_detail'),
]