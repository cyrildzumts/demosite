from django import template
from cart import cart
from catalog.models import Category, Phone, Bag, Shoe, Parfum

register = template.Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    print("Calling cart_box ...")
    return {'cart_item_count': cart_item_count}


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.objects.filter(is_active=True)
    return {
            'active_categories': active_categories,
            'request_path': request_path
            }


@register.inclusion_tag("tags/phone_list.html")
def phone_list():
    print("phone_list tags called.")
    return {'recent_phones': Phone.objects.order_by('-created_at')[:5]}


@register.inclusion_tag("tags/bag_list.html")
def bag_list():
    return {'recent_bags': Bag.objects.order_by('-created_at')[:5]}


@register.inclusion_tag("tags/shoe_list.html")
def shoe_list():
    return {'recent_shoes': Shoe.objects.order_by('-created_at')[:5]}


@register.inclusion_tag("tags/parfum_list.html")
def parfum_list():
    return {'recent_parfums': Parfum.objects.order_by('-created_at')[:5]}
