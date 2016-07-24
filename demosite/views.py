from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm


def not_found_404(request):
    template_name = '404.html'
    return render(request, template_name)


def server_error_500(request):
    template_name = '500.html'
    return render(request, template_name)


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    print("login_view called")
    if user is not None and user.is_active:
        # correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # show an error page
        return HttpResponseRedirect("/account/invalid/")


def logout_view(request):
    auth.logout(request)
    # Redirect to a succes page
    return HttpResponseRedirect("/account/loggedout/")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/polls/")
    else:
        form = UserCreationForm()
    return render(request, template_name="registration/register.html",
                  context=locals())
