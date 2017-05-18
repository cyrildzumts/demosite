from django.shortcuts import render
from contact.models import Contact
from contact.forms import ContactForm
from django.http import HttpResponse
# Create your views here.


def index(reques):
    return HttpResponse("Contact called from you !!!")
