from django.contrib import admin
from catalog.models import Product
from catalog.models import Phablet, Parfum, Category, Color, ProductType


# Register your models here.
admin.site.register(Product)
admin.site.register(Phablet)
admin.site.register(Parfum)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(ProductType)
