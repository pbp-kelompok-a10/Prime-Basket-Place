from django.urls import path
from authentication.views import login,register,logout,account_json,admin_make_admin,admin_remove_admin, change_password

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path("list-users/", account_json),
    path("make-admin/", admin_make_admin),
    path("remove-admin/", admin_remove_admin),
    path("change-password/", change_password),
]