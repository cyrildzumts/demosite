from django.shortcuts import render
from catalog.models import Category, Product
from django.core import urlresolvers  # , serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
# from django.template import RequestContext
from cart import cart
from cart.forms import ProductAddToCartForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from demosite import settings
from django.views.generic.detail import DetailView
# Create your views here.

# this function return a list of subcategory
# which are parts of a parent category
# if parent category is zero, then  we are looking
# for the root category.


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_details.html"
    #context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        name = super(ProductDetailView, self).get_object().name
        context['page_title'] = name
        return context


def get_categories(parent_id):
    id = int(parent_id)
    return {'categories': Category.objects.get(parent_category=id)}


def index(request):
    template_name = "catalog/index.html"
    page_title = 'Acceuille | ' + settings.SITE_NAME
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
    # c.view_count = c.view_count + 1
    # c.save()
    template_name = "catalog/category.html"
    product_list = c.get_products()
    page_title = c.name + ' | ' + settings.SITE_NAME
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
        'current_category': c,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'products': products,
    }
    return render(request, template_name, context)


# product with POST and GET detection
def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    p.view_count = p.view_count + 1
    p.save()
    page_title = p.name + ' | ' + settings.SITE_NAME
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # HTTP methods evaluation:
    if request.method == 'POST':
        # add to cart. create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if the postdata is valid
        if form.is_valid():
            # action = postdata.get('action')
            print("Add to Cart form is Valid")
            # add to cart and redirect to cart page
            user_cart = cart.get_user_cart(request)
            # get product slug from postdata, return blank if empty
            product_slug = postdata.get('product_slug')
            # get quantity added, return 1 if empty
            quantity = postdata.get('quantity', 1)

            p = get_object_or_404(Product, slug=product_slug)
            user_cart.add_to_cart(product=p, quantity=int(quantity))
            # return JsonResponse({'status': 'ok'})
            # if test cookie worked, get rid of it

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('cart:show_cart')
            return HttpResponseRedirect(url)

        else:
            print("Add to Cart form is inValid")
            return JsonResponse({'status': 'error'})
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product_slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET
    request.session.set_test_cookie()
    return render(request, template_name, locals())
