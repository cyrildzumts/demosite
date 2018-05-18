from django.shortcuts import render
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from order.forms import CheckoutForm
from django_email import mail
from order.models import Order, OrderItem
#from order import checkout
from cart.cart_service import CartService
from cart.models import Cart
from order.order_service import OrderService
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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
@login_required
def show_checkout(request):

    template_name = 'order/flat_checkout.html'
    r = request
    cart = CartService.get_user_cart(request)
    if cart.is_empty():
        print("show_checkout : Cart is empty")
        cart_url = urlresolvers.reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        order = OrderService.create_order(request)
        if order:
            request.session['order_number'] = order.pk
            receipt_url = urlresolvers.reverse('order:receipt')
            """ mail.dispatchEmail(subject="Confirmation de votre commande",
                                    content="Votre commande a bien été recue.  Dès reception "
                                    " du paiement votre commande sera livrée. Notez bien que votre commade "
                                    " sera annulée si elle n'est payé dans un delai de 7 jours à compter"
                                    " de maintenant.",
                                    from_email=None,
                                    to_email=["cyrildz@ymail.com"]) 
            """
                #order_items = order.getOrderItem()
            cart.delete()
            order.validate()
            return HttpResponseRedirect(receipt_url)
    else:
            # Method = GET . this an initial request. create a a new form
        cartitems = cart.get_items()

        form_context = fill_form(User.objects.get(
            username=request.user.username))
        form_context['ip_address'] = request.META.get('REMOTE_ADDR')
        print("Form Filled : Name =  " + form_context['name'])
        page_title = 'Checkout'
    
    context = {
        'user_cart': cart,
        'page_title': page_title,
        'form_context': form_context,
        'cartitems': cartitems,
        'template_name' : template_name
    }

    return render(request, template_name, context)


def receipt(request):
        template_name = 'order/thank_you.html'
        return render(request, template_name, locals())

