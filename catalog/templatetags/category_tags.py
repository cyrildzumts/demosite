from django import template
from catalog.models import Category, BaseProduct
# import datetime

register = template.Library()


@register.simple_tag
def subcategory(category=None):
    return Category.objects.filter(parent=category)


@register.simple_tag
def products_from_cat(category):
    return list(BaseProduct.objects.filter(parent=category))
