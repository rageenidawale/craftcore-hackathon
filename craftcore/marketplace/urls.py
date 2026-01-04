from django.urls import path
from .views import (
    become_artisan_view,
    update_artisan_view,
    deactivate_artisan_view,
    add_product_view,
    products_list_view,
    product_detail_view,
    artisan_profile_view,
    edit_product_view,
    delete_product_view,
)

urlpatterns = [
    path("become-artisan/", become_artisan_view, name="become_artisan"),
    path("artisan/update/", update_artisan_view, name="update_artisan"),
    path("seller/products/add/", add_product_view, name="add_product"),
    path("products/", products_list_view, name="products"),
    path("products/<int:product_id>/", product_detail_view, name="product_detail"),
    path("artisans/<int:artisan_id>/", artisan_profile_view, name="artisan_profile"),
    path("seller/products/<int:product_id>/edit/", edit_product_view, name="edit_product"),
    path("seller/products/<int:product_id>/delete/", delete_product_view, name="delete_product"),
    path("artisan/deactivate/", deactivate_artisan_view, name="deactivate_artisan"),
]
