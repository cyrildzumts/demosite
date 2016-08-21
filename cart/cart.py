from .models import CartItem, Cart, UserSession
from catalog.models import BaseProduct
from django.shortcuts import get_object_or_404, Http404
from django.http import HttpResponseRedirect
import decimal
import random

CART_ID_SESSION_KEY = 'cart_id'


def get_cart(user):
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart()
        cart.user = user
        cart.save()
    return cart


def get_user_cart(request):
    if request.user.is_authenticated():
        return get_cart(request.user)
    else:
        raise Http404("Vous devez être connecter pour \
        pouvoir utiliser le Panier.")

# get current user's cart id, set new one if blank


def _cart_id(request):
    """
    If the user is logged in, retrieve the user
    associated cart_id from the database.
    If the user is anonym, then use the session
    to retrieve the cart_id.
    """

    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\
                  1234567890!@#$%&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id


# return all the items froms the user's cart
def get_cart_items(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        items = []
    return items


# add an item to the cart
def add_to_cart(request):
    postdata = request.POST.copy()
    # get product slug from postdata, return blank if empty
    product_slug = postdata.get('product_slug')
    # get quantity added, return 1 if empty
    quantity = postdata.get('quantity', 1)
    # fetch the product or return a missing page error
    p = get_object_or_404(BaseProduct, slug=product_slug)
    # get products in cart
    cart_products = get_cart_items(request)
    product_in_cart = False
    # check to see item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # update quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:
        # create and save a new cart item
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


# return the total number of items in the user's cart
def cart_distinct_item_count(request):
    return get_cart_items(request).count()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem,
                             id=item_id,
                             cart_id=_cart_id(request))


def update_quantity(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


# remove a single item from cart
def remove_from_cart(request):
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


# get the total cost for the current cart
def cart_subtotal(request):
    cart_total = decimal.Decimal('0')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total
