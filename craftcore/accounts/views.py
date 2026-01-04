from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from marketplace.models import ArtisanProfile, Product
from orders.models import Order, OrderItem

def login_view(request):
    next_url = request.GET.get("next")
    
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect(request.path + (f"?next={next_url}" if next_url else ""))

        # Try to find existing user
        try:
            user = User.objects.get(username=email)
            # User exists → try login
            user = authenticate(request, username=email, password=password)

            if user is None:
                messages.error(request, "Incorrect password.")
                return redirect(request.path + (f"?next={next_url}" if next_url else ""))

            login(request, user)
            return redirect(next_url or "/products/")

        except User.DoesNotExist:
            # New user → create account
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            login(request, user)
            return redirect("/onboarding/")

    return render(request, "accounts/login.html")

@login_required
def onboarding_view(request):
    next_url = request.GET.get("next")
    user = request.user

    # If user already has name, skip onboarding
    if user.first_name and user.last_name:
        return redirect("/products/")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if not first_name or not last_name:
            messages.error(request, "Both fields are required.")
            return redirect("/onboarding/")

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect(next_url or "/products/")

    return render(request, "accounts/onboarding.html")

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def profile_view(request):
    user = request.user

    # ---------------- BUYER ORDERS ----------------
    orders = Order.objects.filter(buyer=user).order_by("-created_at")

    # Prepare order display data

    for order in orders:
        first_item = order.items.first()  # OrderItem
        product = first_item.product if first_item else None

        orders = Order.objects.filter(buyer=user).order_by("-created_at")


    # ---------------- SELLER CHECK ----------------
    is_seller = False
    products_data = []
    total_products = 0
    total_orders = 0
    total_earned = 0

    try:
        artisan = user.artisanprofile
        is_seller = True

        products = Product.objects.filter(artisan=artisan, is_active=True)
        total_products = products.count()

        order_items = OrderItem.objects.filter(product__artisan=artisan)
        total_orders = order_items.count()

        for product in products:
            product_order_count = OrderItem.objects.filter(product=product).count()
           
            products_data.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image_url": product.image.url if product.image else "",
                "order_count": product_order_count,
            })

        total_earned = (
            order_items
            .aggregate(
                total=Sum('price_at_purchase')
            )['total'] or 0
        )

    except ArtisanProfile.DoesNotExist:
        pass

    context = {
        "orders": orders,
        "is_seller": is_seller,
        "products": products_data,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_earned": total_earned,
    }

    return render(request, "accounts/profile.html", context)