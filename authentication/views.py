from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from account.models import Account


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

    # Login OK
    auth_login(request, user)

    return JsonResponse({
        "username": user.username,
        "nickname": user.account.nickname,
        "age": user.account.age,
        "profile_picture": user.account.profile_picture,
        "favorites": list(user.account.favorites.values_list('id', flat=True)),
        "role": user.account.roles,
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
        roles="user",
    )

    return JsonResponse({
        "username": user.username,
        "status": "success",
        "message": "User created successfully!"
    }, status=200)
