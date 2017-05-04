from django.shortcuts import render
from catalog.models import Product
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.urls import reverse, resolve
from cart import cart
# from cart.models import Cart, CartItem
from demosite import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from order import checkout
import json
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


# ajax-add To cart view
@csrf_exempt
def ajax_add_to_cart(request):

    response = {}
    response['state'] = False
    added = False
    if len(request.POST) > 0:
        postdata = request.POST.copy()
        product_id = postdata['product_id']
        quantity = postdata['quantity']
        if product_id:
            print("Ajax Add : product_id : ", product_id)
            print("Ajax Add : quantity : ", quantity)
            user_cart = cart.get_user_cart(request)
            p = Product.objects.get(pk=product_id)
            added = user_cart.add_to_cart(product=p, quantity=int(quantity))
            if added is True:
                response['state'] = True
                response['total_count'] = user_cart.items_count()
            else:
                return HttpResponseBadRequest()
    return HttpResponse(json.dumps(response),
                        content_type="application/json")


# ajax cart update view.
@csrf_exempt
def ajax_cart_update(request):
    """
    This method is called from JQuery.  it updates the Cart
    """
    response = {}
    done = False
    if len(request.POST) > 0:
        postdata = request.POST.copy()
        product_id = int(postdata['product_id'])
        quantity = int(postdata['quantity'])
        if product_id is not None and quantity is not None:
            print("Ajax Update : product_id : ", product_id)
            print("Ajax Update : quantity : ", quantity)
            user_cart = cart.get_user_cart(request)
            done = user_cart.update_cart(item_id=product_id, quantity=quantity)
            if done is True:
                response['state'] = True
                response['total_count'] = user_cart.items_count()
                response['count'] = quantity
            else:
                return HttpResponseBadRequest()
    return HttpResponse(json.dumps(response),
                        content_type="application/json")
