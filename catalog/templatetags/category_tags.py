from django import template
from catalog.models import Category, Product
# import datetime

register = template.Library()


@register.simple_tag
def subcategory(category=None):
    return Category.objects.filter(parent=category)


@register.simple_tag
def products_from_cat(category):
    return Product.objects.filter(parent=category).order_by('-created_at')


@register.simple_tag
def get_default_products():
    return Product.objects.all()[:9]

@register.simple_tag
def banners():
    return Product.objects.all()[:5]