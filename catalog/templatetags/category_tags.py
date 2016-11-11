from django import template
from catalog.models import Category, Product
# import datetime

register = template.Library()


@register.simple_tag
def subcategory(category=None):
    # print("subcategory called... category = %s" % (category))
    return Category.objects.filter(parent=category)


@register.simple_tag
def products_from_cat(category):
    return Product.objects.filter(parent=category).order_by('-created_at')
