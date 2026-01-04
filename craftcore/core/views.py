from django.shortcuts import render
from marketplace.models import Product, ArtisanProfile

def home_view(request):
    # Show latest products (limit for clean UI)
    products = (
        Product.objects
        .filter(is_active=True, stock__gt=0, artisan__is_active=True)
        .select_related("artisan")
        .order_by("-created_at")[:6]
    )

    # Show active artisans
    artisans = (
        ArtisanProfile.objects
        .filter(is_active=True)
        .order_by("-created_at")[:4]
    )

    context = {
        "products": products,
        "artisans": artisans,
    }

    return render(request, "core/home.html", context)
