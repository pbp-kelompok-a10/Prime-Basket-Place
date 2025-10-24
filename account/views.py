from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from account.forms import AccountForm
from account.models import Account
from django.contrib.auth.models import User
from detail_product.models import Product

@login_required(login_url='login/')
def show_profile(request):
    """
    Halaman profile: menampilkan dan menyimpan Account (nickname, age, gender, profile_picture).
    Template path: account/templates/account/account_view.html
    """
    account, created = Account.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('account:show_profile')
    else:
        form = AccountForm(instance=account)

    context = {
        'form': form,
        'account': account,
        'user': request.user,
        'last_login': request.COOKIES.get('last_login', None),
    }
    return render(request, 'account_view.html', context)


def register_user(request):

    if request.user.is_authenticated:
        return redirect('account:show_profile')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # password sudah di-hash otomatis
            # buat Account kosong jika belum ada
            Account.objects.get_or_create(user=user)
            messages.success(request, 'Akun berhasil dibuat. Silakan login.')
            return redirect('account:login')
        else:
            # biarkan template menampilkan errors dari form
            pass
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    """
    Login menggunakan authenticate + login dari django.contrib.auth.
    Template path: account/templates/account/login.html
    """
    if request.user.is_authenticated:
        return redirect('account:show_profile')

    if request.method == 'POST':
        # AuthenticationForm membutuhkan request saat instansiasi untuk beberapa fitur
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse('account:show_profile'))
            # simpan cookie last_login agar konsisten dengan implementasimu
            response.set_cookie('last_login', str(datetime.datetime.now()))
            messages.success(request, f'Selamat datang, {user.username}!')
            return response
        else:
            messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    """
    Logout dan hapus cookie last_login.
    """
    logout(request)
    response = HttpResponseRedirect(reverse('account:login'))
    response.delete_cookie('last_login')
    messages.info(request, 'Kamu telah logout.')
    return response

@login_required(login_url='login/')
def change_password(request):
    """
    Menangani halaman ganti username dan password.
    Template path: account/templates/account/password.html
    """
    
    # Render template saat request GET
    if request.method != 'POST':
        return render(request, 'password.html')

    # --- Mulai Logika untuk request POST ---
    
    user = request.user
    new_username = request.POST.get('username')
    current_pass = request.POST.get('current_password')
    new_pass = request.POST.get('new_password')
    confirm_pass = request.POST.get('confirm_password')

    # 1. Validasi Password Lama
    # Kita gunakan user.check_password() untuk membandingkan password mentah
    # dengan hash yang ada di database.
    if not user.check_password(current_pass):
        messages.error(request, 'Password lama Anda salah. Silakan coba lagi.')
        return redirect('account:password') # Kembali ke halaman password

    # 2. Validasi Password Baru
    if new_pass != confirm_pass:
        messages.error(request, 'Password baru dan konfirmasi password tidak cocok.')
        return redirect('account:password') # Kembali ke halaman password
        
    # 3. Validasi Username (jika berubah)
    if new_username != user.username:
        # Cek apakah username baru sudah dipakai user lain
        if User.objects.filter(username=new_username).exists():
            messages.error(request, f'Username "{new_username}" sudah digunakan. Pilih yang lain.')
            return redirect('account:password') # Kembali ke halaman password
        
        # Jika lolos, update username
        user.username = new_username

    # 4. Update Password Baru
    # Gunakan set_password() agar password di-hash dengan benar
    user.set_password(new_pass)
    
    # 5. Simpan semua perubahan (username dan password) ke database
    user.save()

    # 6. Loginkan user kembali
    # PENTING: Mengubah password akan membuat user logout.
    # Kita harus me-login-kan mereka kembali agar sesi tetap berjalan.
    login(request, user)

    messages.success(request, 'Username dan password Anda berhasil diperbarui!')
    return redirect('account:show_profile') # Arahkan ke halaman profil utama

@login_required(login_url='account:login')
def toggle_favorite(request, product_id):
    """
    Menambah atau menghapus produk dari daftar favorit pengguna.
    """
    product = get_object_or_404(Product, id=product_id)
    account, created = Account.objects.get_or_create(user=request.user)
    
    if product in account.favorites.all():
        # Jika sudah ada, hapus dari favorit
        account.favorites.remove(product)
        messages.success(request, f'"{product.name}" telah dihapus dari favorit.')
    else:
        # Jika belum ada, tambahkan ke favorit
        account.favorites.add(product)
        messages.success(request, f'"{product.name}" telah ditambahkan ke favorit.')
        
    return redirect('detail_product:show_detail', pk=product_id)


@login_required(login_url='login/')
def show_favorites(request):
    """
    Menampilkan halaman 'Favourite'
    """
    try:
        account = request.user.account
        favorite_products = account.favorites.all()
    except Account.DoesNotExist:
        favorite_products = [] 

    context = {
        'favorite_products': favorite_products
    }
    return render(request, 'favorite.html', context)

@login_required(login_url='login/')
def delete_account(request):
    """
    Menghapus akun pengguna yang sedang login.
    """
    # Hanya izinkan metode POST untuk keamanan
    if request.method == 'POST':
        user = request.user
        
        # Logout pengguna terlebih dahulu
        logout(request)
        
        # Hapus objek user. 
        # Objek Account yang terkait akan terhapus otomatis 
        # karena on_delete=models.CASCADE.
        user.delete()
        
        messages.success(request, 'Akun Anda telah berhasil dihapus.')
        
        # Arahkan ke halaman login (atau homepage)
        return redirect('account:login') 
    
    # Jika ada yang mencoba mengakses via GET, arahkan kembali ke profil
    return redirect('account:show_profile')
