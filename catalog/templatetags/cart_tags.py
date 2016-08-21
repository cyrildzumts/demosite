from django import template
from cart.cart import get_cart


register = template.Library()


@register.simple_tag
def cart_box(request):
    print("Calling cart_box ...")
    if request.user.is_authenticated():
        cart = get_cart(request.user)
        count = cart.items_count()
    else:
        count = 0
    return count
