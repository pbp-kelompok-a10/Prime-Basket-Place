from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
import requests
from django.core import serializers
from django.http import HttpResponse
from account.models import Account
from account.forms import AccountForm
from account.decorators import admin_required
from detail_product.models import Product


# ===========================
# ADMIN AREA
# ===========================

@login_required(login_url='account:login')
@admin_required
def manage_users(request):
    users = User.objects.all().order_by("id")
    return render(request, "manage_users.html", {"users": users})


@login_required(login_url='account:login')
@admin_required
def make_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)

    account, _ = Account.objects.get_or_create(user=user)
    account.roles = "Admin"
    account.save()

    messages.success(request, f"{user.username} is now an Admin.")
    return redirect("account:manage_users")


@login_required(login_url='account:login')
@admin_required
def remove_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)

    account, _ = Account.objects.get_or_create(user=user)
    account.roles = "User"
    account.save()

    messages.success(request, f"Admin role removed from {user.username}.")
    return redirect("account:manage_users")


def create_admin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Password does not match.")
            return redirect("account:create_admin")

        # Create User
        user = User.objects.create_user(username=username, password=password)

        # Create Account with role Admin
        Account.objects.create(user=user, roles="Admin")

        messages.success(request, "Admin created successfully.")
        return redirect("account:manage_users")

    return render(request, "create_admin.html")


# ===========================
# USER & PROFILE
# ===========================

@login_required(login_url='account:login')
def show_profile(request):
    account, _ = Account.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil berhasil diperbarui!")
            return redirect("account:show_profile")
    else:
        form = AccountForm(instance=account)

    context = {
        "form": form,
        "account": account,
        "user": request.user,
        "last_login": request.COOKIES.get("last_login", None),
    }
    return render(request, "account_view.html", context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect("account:show_profile")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.get_or_create(user=user, roles="User")
            messages.success(request, "Akun berhasil dibuat. Silakan login.")
            return redirect("account:login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect("account:show_profile")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            response = HttpResponseRedirect(reverse("account:show_profile"))
            response.set_cookie("last_login", str(datetime.datetime.now()))

            messages.success(request, f"Selamat datang, {user.username}!")
            return response

        messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("account:login"))
    response.delete_cookie("last_login")
    messages.info(request, "Kamu telah logout.")
    return response


# ===========================
# PASSWORD & USERNAME CHANGE
# ===========================

@login_required(login_url='account:login')
def change_password(request):
    if request.method != "POST":
        return render(request, "password.html")

    user = request.user
    new_username = request.POST.get("username")
    current_pass = request.POST.get("current_password")
    new_pass = request.POST.get("new_password")
    confirm_pass = request.POST.get("confirm_password")

    # Validate old password
    if not user.check_password(current_pass):
        messages.error(request, "Password lama salah.")
        return redirect("account:password")

    # Validate new passwords match
    if new_pass != confirm_pass:
        messages.error(request, "Password baru tidak cocok.")
        return redirect("account:password")

    # Validate new username (if changed)
    if new_username != user.username:
        if User.objects.filter(username=new_username).exists():
            messages.error(request, "Username sudah dipakai.")
            return redirect("account:password")
        user.username = new_username

    # Update password
    user.set_password(new_pass)
    user.save()

    login(request, user)
    messages.success(request, "Username dan password berhasil diperbarui!")
    return redirect("account:show_profile")


# ===========================
# FAVORITES
# ===========================

@login_required(login_url='account:login')
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    account, _ = Account.objects.get_or_create(user=request.user)

    if product in account.favorites.all():
        account.favorites.remove(product)
        messages.success(request, f'"{product.name}" dihapus dari favorit.')
    else:
        account.favorites.add(product)
        messages.success(request, f'"{product.name}" ditambahkan ke favorit.')

    return redirect("detail_product:show_detail", pk=product_id)


@login_required(login_url='account:login')
def show_favorites(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    favorites = account.favorites.all()

    return render(request, "favorite.html", {"favorite_products": favorites})


# ===========================
# DELETE ACCOUNT
# ===========================

@login_required(login_url='account:login')
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()

        messages.success(request, "Akun Anda telah dihapus.")
        return redirect("account:login")

    return redirect("account:show_profile")

def account_json(request):
    # Mengambil SEMUA data account
    data = Account.objects.all()
    # Mengembalikan data dalam bentuk JSON
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
