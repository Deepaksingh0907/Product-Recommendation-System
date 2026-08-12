from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .services.recommendation_service import recommendation_service


@login_required
def home(request):
    if request.method == "POST":
        product_name = (request.POST.get("product_name") or "").strip()
        if not product_name:
            return render(
                request,
                "home.html",
                {"error": "Please enter a product name."},
            )

        product_list = recommendation_service.recommend(
            product_name=product_name,
            min_price=request.POST.get("min_price"),
            max_price=request.POST.get("max_price"),
            min_rating=request.POST.get("min_rating"),
        )

        if not product_list:
            return render(
                request,
                "home.html",
                {
                    "error": "No recommendations found for the given product and filters.",
                    "product_name": product_name,
                },
            )

        return render(
            request,
            "home.html",
            {"product_name": product_name, "product_list": product_list},
        )

    return render(request, "home.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        return render(request, "signup.html", {"error": "User already exists"})
    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


@login_required
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name") or ""
        category = request.POST.get("category") or ""
        about_product = request.POST.get("about_product") or ""
        combined = request.POST.get("combined") or f"{product_name} {category} {about_product}"

        new_product = {
            "product_id": request.POST.get("product_id"),
            "product_name": product_name,
            "category": category,
            "actual_price": request.POST.get("actual_price"),
            "rating": request.POST.get("rating"),
            "about_product": about_product,
            "img_link": request.POST.get("img_link"),
            "product_link": request.POST.get("product_link"),
            "combined": combined,
        }
        recommendation_service.add_product(new_product)
        return render(request, "add_product.html", {"success": True})

    return render(request, "add_product.html")


def logout_view(request):
    logout(request)
    return redirect("login")
