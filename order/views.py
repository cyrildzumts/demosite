from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from order.forms import CheckoutForm

from order.models import Order, OrderItem
from order import order
from cart import cart


# Create your views here.
def show_checkout(request):
    template_name = 'order/checkout.html'
    print("show_checkout view called")
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            response = order.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = urlresolvers.reverse('receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = 'Correct the errors below'
    else:
        form = CheckoutForm()
    page_title = 'Checkout'
    return render(request, template_name, locals())


def receipt(request):
        template_name = 'order/receipt.html'
        order_number = request.session.get('order_number')
        if order_number:
            order = Order.objects.filter(id=order_number)[0]
            order_items = OrderItem.objects.filter(order=order)
            del request.session['order_number']
        else:
            cart_url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(cart_url)
        return render(request, template_name, locals())
