from django.urls import path
from .views import show_detail, update_or_create_detail, delete_detail, show_detail_json, update_description_flutter, show_all_json

app_name = 'detail_product'

urlpatterns = [
    # URL untuk menampilkan detail produk
    path('product/<int:pk>/', show_detail, name='show_detail'),
    
    # URL untuk memproses form Create atau Update
    path('product/<int:pk>/update/', update_or_create_detail, name='update_or_create_detail'),

    # URL untuk menghapus deskripsi
    path('product/<int:pk>/delete/', delete_detail, name='delete_detail'),
    
    # URL flutter
    path('product/<int:pk>/detail-json/', show_detail_json, name='show_detail_json'),
    path('product/<int:pk>/update-flutter/', update_description_flutter, name='update_description_flutter'),
    path('products/jso/', show_all_json, name='show_all_json'),
]