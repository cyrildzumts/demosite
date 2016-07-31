from django.shortcuts import render
from models import *


# Create your views here.
def get_phones(request):
    return Phone.objects.all()


def get_bags(request):
    return Bag.objects.all()


def get_parfums(request):
    return Parfum.objects.all()


def get_shoes(request):
    return Shoe.objects.all()


# this function return a list of subcategory
# which are parts of a parent category
# if parent category is zero, then  we are looking
# for the root category.
def get_categories(request, parent_id):
    id = int(parent_id)
    return Category.objects.get(parent_category=id)
