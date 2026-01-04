from django.shortcuts import redirect
from django.contrib import messages
from .models import ArtisanProfile

def require_active_artisan(request):
    try:
        artisan = request.user.artisanprofile
    except ArtisanProfile.DoesNotExist:
        messages.error(request, "You must become an artisan first.")
        return None

    if not artisan.is_active:
        messages.error(
            request,
            "Your seller account is deactivated. You cannot perform seller actions."
        )
        return None

    return artisan
