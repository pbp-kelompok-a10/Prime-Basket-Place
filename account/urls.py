from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.show_profile, name='show_profile'),
    path('password/', views.change_password, name='password'),
    path('favorites/',views.show_favorites,name='favorites' ),
    # views.favorite_products, name='favorite'

]
