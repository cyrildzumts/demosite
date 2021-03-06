from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from order.forms import CheckoutForm
from django_email import mail
from order.models import Order, OrderItem
from order import checkout
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
    template_name = 'order/flat_checkout.html'
    r = request
    if cart.is_empty(request):
        print("show_checkout : Cart is empty")
        cart_url = urlresolvers.reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CheckoutForm(postdata)
        if form.is_valid():
            order = checkout.create_order(r)
            if order:
                request.session['order_number'] = order.pk
                receipt_url = urlresolvers.reverse('order:receipt')
                ''' mail.dispatchEmail(subject="Confirmation de votre commande",
                                   content="Votre commande a bien été recue.  Dès reception "
                                   " du paiement votre commande sera livrée. Notez bien que votre commade "
                                   " sera annulée si elle n'est payé dans un delai de 7 jours à compter"
                                   " de maintenant.",
                                   from_email=None,
                                   to_email=["cyrildz@ymail.com"]) '''
                #order_items = order.getOrderItem()
                user_cart = cart.get_cart(request.user)
                user_cart.delete()
                order.validate()
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = 'Correct the errors below'
            print("Error data from form : ", form.errors.as_data())
    # else:
    # Method = GET . this an initial request. create a a new form
    user_cart = None
    cartitems = None
    if request.user.is_authenticated():
        user_cart = cart.get_cart(request.user)
        cartitems = user_cart.get_items()

    form_context = fill_form(User.objects.get(username=request.user.username))
    form_context['ip_address'] = request
    print("Form Filled : Name =  " + form_context['name'])
    page_title = 'Checkout'
    return render(request, template_name, locals())


def receipt(request):
        template_name = 'order/thank_you.html'
        return render(request, template_name, locals())

