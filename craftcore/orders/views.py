from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from marketplace.models import Product
from .models import Order, OrderItem

@login_required(login_url="/login/")
def checkout_view(request):
    product_id = request.GET.get("product")

    if not product_id:
        messages.error(request, "No product selected.")
        return redirect("/products/")

    product = get_object_or_404(Product, id=product_id)

    if not product.is_active:
        messages.error(request, "This product is no longer available.")
        return redirect("/products/")

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect(f"/products/{product.id}/")


    if request.method == "POST":
        # Address fields (simple validation)
        full_name = request.POST.get("full_name", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        if not all([full_name, address, city, pincode]):
            messages.error(request, "Please fill all address fields.")
            return redirect(f"/checkout/?product={product.id}")

        # Create Order
        order = Order.objects.create(
            buyer=request.user,
            status="ordered"
        )

        # Create Order Item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price_at_purchase=product.price
        )

        product.stock -= 1
        product.save()


        return redirect(f"/order-confirmation/{order.id}/")

    context = {
        "product": product
    }
    return render(request, "orders/checkout.html", context)

@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})
