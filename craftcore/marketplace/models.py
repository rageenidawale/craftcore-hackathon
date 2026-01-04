from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ArtisanProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="artisanprofile"
    )
    display_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    profile_image = models.ImageField(
        upload_to="artisans/",
        blank=True,
        null=True,
        default="artisans/user-default.png"
    )

    @property
    def profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, "url"):
            return self.profile_image.url
        return settings.MEDIA_URL + "artisans/user-default.png"


    story = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_seller(self):
        return self.is_active

    def __str__(self):
        return self.display_name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    artisan = models.ForeignKey(
        "marketplace.ArtisanProfile",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    stock = models.PositiveIntegerField(default=1)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_out_of_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
