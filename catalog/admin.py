from django.contrib import admin
from catalog.models import BaseProduct
from catalog.models import Phone, Parfum, Shoe, Bag, Category, Size, Color


# Register your models here.
admin.site.register(BaseProduct)
admin.site.register(Phone)
admin.site.register(Parfum)
admin.site.register(Shoe)
admin.site.register(Bag)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)
