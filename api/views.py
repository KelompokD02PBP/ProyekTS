from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.forms import ProfileUserForm

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    print(request.POST)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:

            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "id" : user.pk,
                "password" : password,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)


def logout(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)


def register(request):
    user_form = UserCreationForm(request.POST)
    profile_form = ProfileUserForm(request.POST or None, request.FILES or None)
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        profile = profile_form.save(commit=False)
        profile.user=user
        profile.save()
        return JsonResponse({
            "username": user.username,
            "status": True,
            "message": "Register sukses!"
            # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
        }, status=200)
    
    return JsonResponse({
        "status": False,
        "message": "Register gagal, tidak valid."
    }, status=401)
    