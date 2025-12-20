from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review, name='create_review'),
    path('update/<int:pk>/', views.update_review, name='update_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
<<<<<<< HEAD

    path('json/<int:product_id>/', views.get_reviews_json, name='get_reviews_json'),
    path('json/<int:product_id>/stats/', views.get_review_stats_json, name='get_review_stats_json'),
    path('create-flutter/<int:product_id>/', views.create_review_flutter, name='create_review_flutter'),
=======
>>>>>>> main
]
