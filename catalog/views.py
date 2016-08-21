from django.shortcuts import render
from catalog.models import BaseProduct, Phone, Parfum, Shoe, Bag, Category
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from cart import cart
from cart.forms import ProductAddToCartForm
from datetime import datetime
from catalog.script_test import print_session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

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
    session = request.session
    # get the number of visits to the site

    if request.session.get('last_visit'):
        last_visit_time = session.get('last_visit')
        visits = session.get('visits', 0)
        delta = (datetime.now()-datetime.strptime(last_visit_time[:-7],
                 "%Y-%m-%d %H:%M:%S")
                 ).seconds
        if delta > 10:
            session['visits'] = visits + 1
            session['last_visit'] = str(datetime.now())
    else:
        session['last_visit'] = str(datetime.now())
        session['visits'] = 1
    return render(request, template_name, locals())


def show_category(request, category_slug):
    c = get_object_or_404(Category, slug=category_slug)
    template_name = "catalog/category.html"
    product_list = c.get_products()
    page_title = c.name
    # show 9 product per page
    paginator = Paginator(product_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # page is not a not a number,
        # deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # if page is ou of range (eg. 9999),
        # deliver the last page of results
        products = paginator.page(paginator.num_pages)
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    context = {
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'products': products,
    }
    return render(request, template_name, context)


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
            user_cart = cart.get_user_cart(request)
            # get product slug from postdata, return blank if empty
            product_slug = postdata.get('product_slug')
            # get quantity added, return 1 if empty
            quantity = postdata.get('quantity', 1)
            p = get_object_or_404(BaseProduct, slug=product_slug)
            user_cart.add_to_cart(product=p, quantity=int(quantity))
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
