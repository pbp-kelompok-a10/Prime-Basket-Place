from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/',  create_product, name='create_product'),
    path('product/<int:id>/edit', edit_product, name='edit_product'),
    path('product/<int:id>/delete', delete_product, name='delete_product'),
    # path('product/<int:id>/detail', show_product, name='detail_product'),
]
