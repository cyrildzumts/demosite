from django.shortcuts import render
from cart import cart
from demosite import settings

# Create your views here.


def show_cart(request):
    template_name = "cart/cart.html"
    if request.method == "POST":
        postdata = request.POST.copy()
        if postdata['submit'] == 'Supprimer':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Actualiser':
            cart.update_quantity(request)
    cart_items = cart.get_cart_items(request)
    page_title = 'Panier' + " - " + settings.SITE_NAME
    cart_subtotal = cart.cart_subtotal(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    return render(request, template_name, locals())
# Create your views here.
