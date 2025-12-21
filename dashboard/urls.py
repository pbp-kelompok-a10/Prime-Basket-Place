from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/',  create_product, name='create_product'),
    path('product/<int:id>/edit', edit_product, name='edit_product'),
    path('product/<int:id>/delete', delete_product, name='delete_product'),
    # path('product/<int:id>/detail', show_product, name='detail_product'),
    path('json/', show_json_dashboard, name='show_json_dashboard'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-product-flutter/', create_product_flutter, name='create_product_flutter'),
    path("update-product/<int:id>/", update_product_flutter, name='update_product_flutter'),
    path("delete-product/<int:id>/", delete_product_flutter, name='delete_product_flutter'),
    path("toggle-favorite/<int:id>/", toggle_favorite_flutter, name='toggle_favorite_flutter'),
]
