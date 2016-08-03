from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from accounts.forms import AuthenticationForm, RegistrationForm
from demosite import settings


# GLOBAL Redirect url variable
REDIRECT_URL = settings.LOGIN_REDIRECT_URL


# Create your views here.
def login(request):
    """
    Log in view
    """
    page_title = "Connexion d'utilisateur"
    template_name = 'registration/login.html'
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
    page_title = 'Creation de compte'
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
    page_title = 'Mon Compte'
    name = request.user.username
    return render(request, template_name, locals())
