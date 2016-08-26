from django import template
from cart.models import Cart
from catalog.models import Category, Phone, Bag, Shoe, Parfum
import datetime
register = template.Library()


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.objects.filter(is_active=True)
    return {
            'active_categories': active_categories,
            'request_path': request_path
            }


@register.inclusion_tag("tags/phone_list.html")
def phone_list():
    print("phone_list tags called.")
    return {'recent_phones': Phone.objects.all()}


@register.inclusion_tag("tags/bag_list.html")
def bag_list():
    return {'recent_bags': Bag.objects.all()}


@register.inclusion_tag("tags/shoe_list.html")
def shoe_list():
    return {'recent_shoes': Shoe.objects.all()}


@register.inclusion_tag("tags/parfum_list.html")
def parfum_list():
    return {'recent_parfums': Parfum.objects.all()}


@register.simple_tag
def current_time(format_string=''):
    if format_string:
        return datetime.datetime.now().strftime(format_string)
    return datetime.datetime.now().strftime("%d / %m / %Y - %H : %M")


@register.simple_tag
def display_session(request):
    print("Request Scheme : %s " % (request.scheme))
    print("Request Method : %s " % (request.method))
    print("Request Path : %s " % (request.path))
    session = request.session
    print("Session Object: ")
    print("Session Expire Age : %d" % (session.get_expiry_age()))

    print("Session Content :")
    for k in session.keys():
        print("Key : %s" % (k))
    return request.session
