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
    path('toggle-favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    # views.favorite_products, name='favorite'
    path('delete/', views.delete_account, name='delete_account'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('make-admin/<int:user_id>/', views.make_admin, name='make_admin'),
    path('remove-admin/<int:user_id>/', views.remove_admin, name='remove_admin'),
    path('create-admin/', views.create_admin, name='create_admin'),
    path('json/', views.show_allJson, name='show_allJson'),
    path('proxy-image/', views.proxy_image, name='proxy_image'),
]
