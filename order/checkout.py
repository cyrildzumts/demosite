from order.models import Order, OrderItem
from cart import cart_utils
from order.forms import CheckoutForm
from django.core import urlresolvers


# return the URL from th Checkout module for cart
def get_checkout_url(request):
    return urlresolvers.reverse('checkout')


def process(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    post_data = request.POST.copy()
    amount = cart.cart_subtotal(request)
    results = {}
    return 1


def create_order(request):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.user = request.user
    order.status = Order.SUBMITTED
    order.generate_order_refNum()
    order.save()
    # if order save succeeded
    if order.pk:
        cart_items = cart.get_cart(request.user).get_items()
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price()  # using @property
            oi.product = ci.product
            oi.save()
        # all set, empty cart
        # cart.empty_cart(request)

        return order
