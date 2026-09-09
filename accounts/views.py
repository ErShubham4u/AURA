
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Username validation
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Username already exists."}
            )

        # Email validation
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Email is already registered."}
            )

        # Password length
        if len(password) < 8:
            return render(
                request,
                "accounts/register.html",
                {"error": "Password must be at least 8 characters."}
            )

        # Password match
        if password != confirm_password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match."}
            )

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Automatically login
        login(request, user)

        return redirect("home")

    return render(request, "accounts/register.html")


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def password_reset_request(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()

        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(
                force_bytes(user.pk)
            )

            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                f"/accounts/password-reset/{uid}/{token}/"
            )

            print("PASSWORD RESET LINK:")
            print(reset_link)

        except User.DoesNotExist:
            pass

        return render(
            request,
            "accounts/password_reset_done.html"
        )

    return render(
        request,
        "accounts/password_reset.html"
    )
