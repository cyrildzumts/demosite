from django.shortcuts import render
from catalog.models import BaseProduct, Phone, Parfum, Shoe, Bag, Category
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from cart import cart
from cart.forms import ProductAddToCartForm


# Create your views here.
def get_phones():
    return {'phones': Phone.objects.all()}


def get_bags():
    return {'bags': Bag.objects.all()}


def get_parfums():
    return {'parfums': Parfum.objects.all()}


def get_shoes():
    return {'shoes': Shoe.objects.all()}


# this function return a list of subcategory
# which are parts of a parent category
# if parent category is zero, then  we are looking
# for the root category.
def get_categories(parent_id):
    id = int(parent_id)
    return {'categories': Category.objects.get(parent_category=id)}


def index(request):
    template_name = "catalog/index.html"
    page_title = 'Catalogue' + " - "

    return render(request, template_name, locals())


def show_category(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)
    template_name = "catalog/category.html"
    products = c.baseproduct_set.all()
    page_title = c.name + " - "
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, template_name, locals())


# product with POST and GET detection
def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(BaseProduct, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name + " - "
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # HTTP methods evaluation:
    if request.method == 'POST':
        # add to cart. create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if the postdata is valid
        if form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('cart:show_cart')
            return HttpResponseRedirect(url)
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product_slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET
    request.session.set_test_cookie()
    return render(request, template_name, locals())
