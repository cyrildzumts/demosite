from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from accounts.models import UserProfile
from accounts.forms.forms import UserForm, UserProfileForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from demosite import settings, utils
from order.models import Order, OrderItem
from accounts.services import AccountService
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView

# GLOBAL Redirect url variable
REDIRECT_URL = settings.LOGIN_REDIRECT_URL

@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    #template_name = 'accounts/userprofile_form.html' : default name
    success_url = reverse_lazy('accounts:user_account')

    def get_object(self, queryset=None):
        profile = UserProfile.objects.get(user=self.request.user)
        return profile




# Create your views here.
def login(request):
    """
    Log in view
    """
    page_title = "Connexion d'utilisateur"
    template_name = 'registration/login.html'
    
    # template_name = 'tags/login_form.html'
    if request.method == 'POST':
        result = AccountService.process_login_request(request)
        if result['user_logged']:
            return redirect(result['next_url'])
    else:
        form = AccountService.get_authentication_form()
        register_form = AccountService.get_registration_form()
    
    context = {
        
        'page_title':page_title,
        'template_name':template_name,
        'form': form,
        'registration_form': register_form,
    }
    return render(request, template_name, context)


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
        result = AccountService.process_registration_request(request)
        if result['user_logged']:
            return result['next_url']

    else:
        # form = UserCreationForm()
        form = AccountService.get_registration_form()
    context = {
        'page_title': page_title,
        'template_name': template_name,
        'form': form,
    }
    return render(request, template_name, context)


@login_required
def user_account(request):
    """
     This method serves the default user account page.
     This page display an overview of the user's orders,
     user's infos ...  So this method have to provide these
     informations to the template.
    """
    template_name = "accounts/my-account.html"
    page_title = 'Mon Compte | ' + settings.SITE_NAME
    user = User.objects.get(username=request.user.username)
    name = user.first_name
    orders = user.order_set.order_by('-date').exclude(status=Order.FINISHED)[:2]
    context = {
        'name'      : name,
        'page_title':page_title,
        'template_name':template_name,
        'orders': orders,
    }
    return render(request, template_name, context)


@login_required
def edit_account(request, pk):
    template_name = "accounts/my-account.html"
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
        'order':order,
    }
    return render(request, template_name, context)
