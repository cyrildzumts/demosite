from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from order.forms import CheckoutForm

from order.models import Order, OrderItem
from order import order
from cart import cart
from django.contrib.auth.models import User
from accounts.models import UserProfile


def fill_form(user):
    form = {}
    user_p = UserProfile.objects.get(user=user)
    form['email'] = user.email
    form['phone'] = user_p.telefon
    form['name'] = user_p.user.first_name + ' ' + user_p.user.last_name
    form['address'] = user_p.address
    form['city'] = user_p.city
    form['country'] = user_p.country
    form['zip'] = user_p.zip_code
    return form


# Create your views here.
def show_checkout(request):
    template_name = 'order/checkout.html'
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
    # else:
    # Method = GET . this an initial request. create a a new form
    form_context = fill_form(User.objects.get(username=request.user.username))
    form_context['ip_address'] = request
    print("Form Filled : Name =  " + form_context['name'])
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
