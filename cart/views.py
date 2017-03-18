from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, resolve
from cart import cart
# from cart.models import Cart, CartItem
from demosite import settings
from django.views.decorators.csrf import csrf_protect
from order import checkout

# Create your views here.


@csrf_protect
def show_cart(request):
    template_name = "cart/cart.html"
    user_cart = cart.get_user_cart(request)
    # checkout_url = checkout.get_checkout_url(request)
    match = resolve('/order/checkout/')

    if request.method == "POST":
        postdata = request.POST.copy()
        item_id = postdata['item_id']
        quantity = postdata['quantity']
        if postdata['submit'] == 'Supprimer':
            user_cart.remove_from_cart(item_id)
        if postdata['submit'] == 'Actualiser':
            user_cart.update_quantity(item_id=item_id, quantity=int(quantity))
        if postdata['submit'] == 'Checkout':
            print("Checkout clicked from cart")
            return HttpResponseRedirect(match.url_name)
    cart_items = user_cart.get_items()
    page_title = 'Panier' + " - " + settings.SITE_NAME
    cart_subtotal = user_cart.subtotal()
    cart_item_count = user_cart.items_count()

    context = {'cart_items': cart_items,
               'page_title': page_title,
               'cart_item_count': cart_item_count,
               'cart_subtotal': cart_subtotal,
               'checkout_url': match.url_name,
               }
    return render(request=request,
                  template_name=template_name,
                  context=context)
# Create your views here.
