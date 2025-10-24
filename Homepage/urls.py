from django.urls import path
from . import views
app_name = 'Homepage'

urlpatterns = [
    path('', views.show_main, name='homepage'),
]