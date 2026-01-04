from django import template
from marketplace.models import ArtisanProfile

register = template.Library()

@register.filter
def has_artisan(user):
    return ArtisanProfile.objects.filter(user=user).exists()

@register.filter
def get_name_by_id(queryset, id):
    try:
        return queryset.get(id=id).name
    except:
        return ""

