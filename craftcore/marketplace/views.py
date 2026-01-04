from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from .models import ArtisanProfile, Product, Category, Material
from .utils import require_active_artisan

@login_required(login_url="/login/?next=/become-artisan/")
def become_artisan_view(request):
    # Prevent duplicate artisan profiles
    if ArtisanProfile.objects.filter(user=request.user).exists():
        return redirect("/profile/")

    if request.method == "POST":
        display_name = request.POST.get("display_name", "").strip()
        location = request.POST.get("location", "").strip()
        story = request.POST.get("story", "").strip()
        profile_image = request.FILES.get("profile_image") 

        # Validation
        if not display_name or not location or not story:
            messages.error(request, "All fields are required.")
            return redirect("/become-artisan/")

        if len(story) < 20:
            messages.error(request, "Please write a slightly longer story.")
            return redirect("/become-artisan/")

        # Create Artisan Profile
        ArtisanProfile.objects.create(
            user=request.user,
            display_name=display_name,
            location=location,
            story=story,
            profile_image=profile_image,
            is_active=True
        )

        messages.success(request, "You are now an artisan on CraftCore!")
        return redirect("/profile/")

    return render(request, "marketplace/become_artisan.html")

@login_required
def update_artisan_view(request):
    try:
        artisan = request.user.artisanprofile
    except ArtisanProfile.DoesNotExist:
        messages.error(request, "You are not an artisan.")
        return redirect("/become-artisan/")

    if request.method == "POST":
        display_name = request.POST.get("display_name", "").strip()
        location = request.POST.get("location", "").strip()
        story = request.POST.get("story", "").strip()
        profile_pic = request.FILES.get("profile_pic")

        # Validation
        if not all([display_name, location, story]):
            messages.error(request, "All fields except profile picture are required.")
            return redirect("/artisan/update/")

        artisan.display_name = display_name
        artisan.location = location
        artisan.story = story

        # Image update ONLY if uploaded
        if profile_pic:
            artisan.profile_pic = profile_pic

        artisan.save()

        messages.success(request, "Artisan profile updated successfully.")
        return redirect("/profile/")

    context = {
        "artisan": artisan,
        "is_edit": True
    }

    return render(request, "marketplace/become_artisan.html", context)

@login_required
def deactivate_artisan_view(request):
    try:
        artisan = request.user.artisanprofile
    except ArtisanProfile.DoesNotExist:
        messages.error(request, "You are not a seller.")
        return redirect("/profile/")

    if request.method != "POST":
        return redirect("/profile/")

    with transaction.atomic():
        # 1. Deactivate artisan
        artisan.is_active = False
        artisan.save()

        # 2. Deactivate ALL products (not delete)
        Product.objects.filter(
            artisan=artisan,
            is_active=True
        ).update(is_active=False)

    messages.success(
        request,
        "You are no longer a seller. Your products are no longer visible, "
        "but your past orders and earnings are preserved."
    )

    return redirect("/profile/")

@login_required
def add_product_view(request):
    artisan = require_active_artisan(request)
    if not artisan:
        return redirect("/profile/")
    
    categories = Category.objects.all()
    materials = Material.objects.all()

    context = {
        "categories": categories,
        "materials": materials,
        "is_edit": False
    }

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category")
        material_id = request.POST.get("material")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")

        try:
            category = Category.objects.get(id=category_id)
            material = Material.objects.get(id=material_id)
        except (Category.DoesNotExist, Material.DoesNotExist):
            messages.error(request, "Invalid category or material.")
            return redirect("/seller/products/add/")

        # Validation
        if not all([name, description, price, stock, image]):
            messages.error(request, "All fields are required.")
            return redirect("/seller/products/add/")

        if float(price) <= 0:
            messages.error(request, "Price must be greater than zero.")
            return redirect("/seller/products/add/")

        Product.objects.create(
            artisan=artisan,
            name=name,
            description=description,
            category=category,
            material=material,
            price=price,
            stock=stock,
            image=image
        )

        messages.success(request, "Product added successfully.")
        return redirect("/profile/")

    return render(request, "marketplace/add_product.html", context)

@login_required
def edit_product_view(request, product_id):
    artisan = require_active_artisan(request)
    if not artisan:
        return redirect("/profile/")
    
    artisan = request.user.artisanprofile
    product = get_object_or_404(Product, id=product_id, artisan=artisan)

    categories = Category.objects.all()
    materials = Material.objects.all()

    if request.method == "POST":
        product.name = request.POST.get("name", "").strip()
        product.description = request.POST.get("description", "").strip()
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.category_id = request.POST.get("category")
        product.material_id = request.POST.get("material")

        image = request.FILES.get("image")
        if image:
            product.image = image  # only replace if uploaded

        product.save()

        messages.success(request, "Product updated successfully.")
        return redirect("/profile/")

    context = {
        "product": product,
        "categories": categories,
        "materials": materials,
        "is_edit": True,
    }

    return render(request, "marketplace/add_product.html", context)

@login_required
def delete_product_view(request, product_id):
    artisan = require_active_artisan(request)
    if not artisan:
        return redirect("/profile/")
    
    artisan = request.user.artisanprofile
    product = get_object_or_404(Product, id=product_id, artisan=artisan)

    if request.method == "POST":
        product.is_active = False
        product.save()
        messages.success(request, "Product deleted successfully.")
        return redirect("/profile/")

    return render(request, "marketplace/confirm_delete.html", {
        "product": product
    })

def products_list_view(request):
    products = Product.objects.filter(is_active=True).select_related("artisan")

    selected_categories = request.GET.getlist("category")
    selected_materials = request.GET.getlist("material")
    sort = request.GET.get("sort")
    query_params = request.GET.copy()

    if selected_categories or selected_materials:
        query = Q()

        if selected_categories:
            query |= Q(category_id__in=selected_categories)

        if selected_materials:
            query |= Q(material_id__in=selected_materials)

        products = products.filter(query)

    # SORTING
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")

    context = {
        "products": products,
        "categories": Category.objects.all(),
        "materials": Material.objects.all(),
        "selected_categories": selected_categories,
        "selected_materials": selected_materials,
        "selected_sort": sort,
    }

    context.update({
        "base_query": query_params,
    })

    return render(request, "marketplace/products.html", context)

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    inactive = not product.is_active
    out_of_stock = product.stock <= 0

    artisan = product.artisan

    # Similar products: same category OR same material
    similar_products = (
        Product.objects
        .filter(is_active=True)
        .filter(
            Q(category=product.category) |
            Q(material=product.material)
        )
        .exclude(id=product.id)
        .distinct()
        [:4]
    )

    # More by artisan
    artisan_products = (
        Product.objects
        .filter(artisan=artisan, is_active=True)
        .exclude(id=product.id)
        [:4]
    )

    inactive = not product.is_active

    context = {
        "product": product,
        "artisan": artisan,
        "similar_products": similar_products,
        "artisan_products": artisan_products,
        "inactive": inactive,
        "out_of_stock": out_of_stock,
    }

    return render(request, "marketplace/product_detail.html", context)

def artisan_profile_view(request, artisan_id):
    artisan = get_object_or_404(ArtisanProfile, id=artisan_id, is_active=True)

    # Products by this artisan
    products = Product.objects.filter(artisan=artisan, is_active=True).order_by("-created_at")

    # Other artisans (exclude current)
    other_artisans = (
        ArtisanProfile.objects
        .filter(is_active=True)
        .exclude(id=artisan.id)[:8]
    )

    context = {
        "artisan": artisan,
        "products": products,
        "other_artisans": other_artisans,
    }

    return render(request, "marketplace/artisan_profile.html", context)