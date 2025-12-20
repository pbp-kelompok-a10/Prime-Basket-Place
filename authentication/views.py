from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from account.models import Account
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash


# ===========================
# LOGIN
# ===========================
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return JsonResponse({
            "status": False,
            "message": "Missing username or password."
        }, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)

    if not user.is_active:
        return JsonResponse({
            "status": False,
            "message": "Login failed, account is disabled."
        }, status=401)
        
    account, created = Account.objects.get_or_create(user=user,
                                                     defaults={
                                                       'nickname': '',
                                                       'age': None,
                                                       'profile_picture': '',
                                                       'roles': 'User'
                                                   })

    # Login OK
    auth_login(request, user)

    return JsonResponse({
        "username": user.username,
        "nickname": account.nickname,
        "age": account.age,
        "profile_picture": account.profile_picture,
        "favorites": list(account.favorites.values_list('id', flat=True)),
        "role": account.roles,
        "status": True,
        "message": "Login successful!"
    }, status=200)


# ===========================
# REGISTER
# ===========================
@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": "failed",
            "message": "Invalid request method."
        }, status=400)

    # Try reading JSON
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({
            "status": "failed",
            "message": "Invalid JSON format."
        }, status=400)

    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    # Validation
    if not username or not password1:
        return JsonResponse({
            "status": "failed",
            "message": "Missing required fields."
        }, status=400)

    if password1 != password2:
        return JsonResponse({
            "status": "failed",
            "message": "Passwords do not match."
        }, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "status": "failed",
            "message": "Username already exists."
        }, status=400)

    # Create user
    user = User.objects.create_user(username=username, password=password1)

    # Create Account profile
    Account.objects.create(
        user=user,
        nickname="",
        age=None,
        profile_picture="",
        roles="User",
    )

    return JsonResponse({
        "username": user.username,
        "status": "success",
        "message": "User created successfully!"
    }, status=200)
    
@csrf_exempt
def logout(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)
        
def is_admin(user):
    if not user.is_authenticated:
        return False

    try:
        return user.account.roles == "Admin"
    except:
        return False

@csrf_exempt
def account_json(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": False, "message": "Not authenticated"},
            status=401
        )

    accounts = Account.objects.select_related("user").all()

    data = []
    for acc in accounts:
        data.append({
            "user": acc.user.id,
            "nickname": acc.nickname,
            "age": acc.age,
            "profile_picture": acc.profile_picture,
            "roles": acc.roles,
            "favorites": list(acc.favorites.values_list("id", flat=True)),
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def admin_make_admin(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid method"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"status": False, "message": "Not authenticated"}, status=401)

    if not is_admin(request.user):
        return JsonResponse({"status": False, "message": "Forbidden"}, status=403)

    try:
        user_id = request.POST.get("user_id")

        user = User.objects.get(id=user_id)
        account, _ = Account.objects.get_or_create(user=user)
        account.roles = "Admin"
        account.save()

        return JsonResponse({
            "status": True,
            "message": f"{user.username} is now Admin"
        })
    except User.DoesNotExist:
        return JsonResponse({"status": False, "message": "User not found"}, status=404)


@csrf_exempt
def admin_remove_admin(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid method"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"status": False, "message": "Not authenticated"}, status=401)

    if not is_admin(request.user):
        return JsonResponse({"status": False, "message": "Forbidden"}, status=403)

    try:
        user_id = request.POST.get("user_id")

        user = User.objects.get(id=user_id)
        account, _ = Account.objects.get_or_create(user=user)
        account.roles = "User"
        account.save()

        return JsonResponse({
            "status": True,
            "message": f"{user.username} is no longer Admin"
        })
    except User.DoesNotExist:
        return JsonResponse({"status": False, "message": "User not found"}, status=404)
    

@csrf_exempt
def change_password(request):
    if request.method != 'POST':
        return JsonResponse({"status": False, "message": "Method not allowed"}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({"status": False, "message": "Not logged in"}, status=401)

    try:
        # HANYA ambil data password
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # 1. Cek Password Lama
        if not user.check_password(current_password):
            return JsonResponse({"status": False, "message": "Password lama salah"}, status=400)

        # 2. Cek Password Baru cocok
        if new_password != confirm_password:
             return JsonResponse({"status": False, "message": "Password baru tidak cocok"}, status=400)

        # 3. Update Password
        if new_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user) # Supaya tidak logout otomatis

        return JsonResponse({"status": True, "message": "Password berhasil diperbarui!"})

    except Exception as e:
        return JsonResponse({"status": False, "message": str(e)}, status=500)