from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/")

        return render(request, "accounts/login.html", {
            "error": "Tên đăng nhập hoặc mật khẩu không đúng!"
        })

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(request, "accounts/register.html", {
                "error": "Mật khẩu nhập lại không khớp!"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Tên đăng nhập đã tồn tại!"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("accounts:login")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("/")

    return render(request, "accounts/admin.html")