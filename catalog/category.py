from django.db import models
from catalog.models import Category, BaseProduct


class CategoryEntry:
    def __init__(self, category):
        self.current = category
        self.children = self.current.get_categories

    def is_parent(self):
        return self.children is not None

    def products(self):
        return BaseProduct.objects.filter()


class CategoryTree(object):
    pass


def has_children(category):
    if Category.objects.filter(parent=category) is None:
        return False
    return True


def get_children_categories(category, cat_list=[]):
    if has_children(category):
        cat_list.append()
