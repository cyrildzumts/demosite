from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from accounts.forms import AuthenticationForm, RegistrationForm
from .models import UserProfile
from .forms.forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from demosite import settings
from order.models import Order, OrderItem


# GLOBAL Redirect url variable
REDIRECT_URL = settings.LOGIN_REDIRECT_URL


# Create your views here.
def login(request):
    """
    Log in view
    """
    page_title = "Connexion d'utilisateur"
    template_name = 'registration/login.html'
    # template_name = 'tags/login_form.html'
    print("login ...")
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect(REDIRECT_URL)
    else:
        form = AuthenticationForm()
    return render(request, template_name, locals())


def logout(request):
    """
    Log out view
    """
    auth.logout(request)
    return redirect(REDIRECT_URL)


def register(request):
    """
    User registration view
    """
    template_name = "registration/register.html"
    page_title = 'Creation de compte | ' + settings.SITE_NAME
    if request.method == 'POST':
        postdata = request.POST.copy()
        # form = UserCreationForm(postdata)
        form = RegistrationForm(data=request.POST.copy())
        if form.is_valid():
            # form.save()
            form.save()
            print("Register Form is valid...")
            # return redirect(REDIRECT_URL)
            username = request.POST['username']
            password = request.POST['password1']
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                return redirect(REDIRECT_URL)

        else:
            print("Register Form is invalid...")

    else:
        # form = UserCreationForm()
        form = RegistrationForm()
    return render(request, template_name, locals())


@login_required
def user_account(request):
    template_name = "registration/user_account.html"
    page_title = 'Mon Compte | ' + settings.SITE_NAME
    user = User.objects.get(username=request.user.username)
    user_profile = user.userprofile
    name = request.user.first_name
    return render(request, template_name, locals())


@login_required
def edit_account(request, pk):
    template_name = "registration/user_account.html"
    page_title = 'Modification du profile | ' + settings.SITE_NAME
    user = User.objects.get(pk=pk)
    user = request.user
    user_form = UserForm(instance=user)
    ProfileInlineFormSet = inlineformset_factory(User,
                                                 UserProfile,
                                                 fields=('country', 'city',
                                                         'province', 'address',
                                                         'zip_code', 'telefon',
                                                         'newsletter',
                                                         'is_active_account'))
    formset = ProfileInlineFormSet(instance=user)
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=user)
        formset = ProfileInlineFormSet(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            formset = ProfileInlineFormSet(request.POST, request.FILES, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                return HttpResponseRedirect(REDIRECT_URL)

    name = request.user.username
    return render(request, template_name, locals())

@login_required
def show_orders(request):
    page_title = "Mes Commandes" + " - " + settings.SITE_NAME
    template_name = "accounts/user_orders.html"
    user = request.user
    orders = user.order_set.order_by('-date')
    context = {
        'page_title':page_title,
        'template_name':template_name,
        'orders': orders,
    }
    return render(request, template_name, context)

# TODO add try  catch block and add a redirect
# in case of an exception
@login_required
def order_details(request, order_id):
    page_title = "Contenu de la commande" + " - " + settings.SITE_NAME
    template_name = "order/order_details.html"
    user = request.user
    id = int(order_id)
    order = None

    if(id):
        order = Order.objects.get(id=id)
    context = {
        'page_title':page_title,
        'template_name':template_name,
        'order_ref' : order.ref_num,
        'orderitems': order.orderitem_set.all(),
    }
    return render(request, template_name, context)
