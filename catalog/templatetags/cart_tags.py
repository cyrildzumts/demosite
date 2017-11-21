from django import template
from cart.cart import get_cart


register = template.Library()


@register.simple_tag
def cart_box(request):
    context = {}
    if request.user.is_authenticated():
        cart = get_cart(request.user)
        count = cart.items_count()
        cartItems = cart.get_items()
    else:
        count = 0
        cartItems = None
    context = {'count' : count,
               'cartItems' : cartItems}
    return context
