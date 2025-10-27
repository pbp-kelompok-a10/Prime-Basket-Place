from django.urls import path
from . import views
app_name = 'Homepage'

urlpatterns = [
    path('', views.show_main, name='homepage'),
    path('slider/manage', views.manage_slider, name='manage_slider'),
    path('slider/delete/<int:id>/', views.delete_slider_product, name='delete_slider_product'),
]