from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review, name='create_review'),
    path('update/<int:pk>/', views.update_review, name='update_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
]
