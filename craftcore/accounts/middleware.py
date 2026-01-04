from django.shortcuts import redirect
from django.urls import reverse

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            onboarding_url = reverse("onboarding")
            allowed_paths = [
                onboarding_url,
                reverse("logout"),
                reverse("admin:login")
            ]

            if (not request.user.first_name and request.path not in allowed_paths):
                return redirect(onboarding_url)

        return self.get_response(request)