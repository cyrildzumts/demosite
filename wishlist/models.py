from django.db import models

# Create your models here.
from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404

# Create your models here.

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'wishlists'
        ordering = ['-created_at']

    def __str__(self):
        return "Wishlist id : %d\nUser :%s" % (self.id, self.user)

    def add(self, product_id):
        """
        Add a new product into the Shopping Cart.
        If the product is already in the cart then
        update the quantity.
        If not then create a new CartItem and set
        appropriate value for its variable and save.
        """
        product_id = int(product_id)
        item_in_cart = False
        items = self.get_items()
        for item in items:
            if item.product.pk == product_id:
                item_in_cart = True
        if not item_in_cart:
            # create and save a new cart item
            product = Product.objects.get(id=product_id)
            item = WishlistItem(self, product)
            item.save()

    def get_item(self, item_id):
        """
        Return a WishlistItem object when found
        """
        return self.wishlistitem_set.get(id=item_id)

    def remove(self, item_id):
        """
        Delete the CartItem corresponding to item_id.
        """
        item = self.get_item(item_id)
        if item:
            item.delete()

    def get_items(self):
        """
        Return all the items present in the Cart.
        """
        return self.wishlistitem_set.all()

    def items_count(self):
        """
        Return the number of items present in the Cart.
        """    
        return self.wishlistitem_set.count

    def get_user(self):
        return self.user

    def get_id(self):
        return self.id


class WishlistItem(models.Model):
    """
    WishlistItem represents the an Item present in a Wishlist.
    WishlistItem is generic representation of the Product class,
    so much of all message send to this instance is delegated to
    the associated product member.
    """
    wishlists = models.ManyToManyField(Wishlist, unique=False)
    product = models.ForeignKey('catalog.Product', unique=False)

    class Meta:
        db_table = 'wishlistitems'

    def __init__(wishlist=None, product=None):
        if(wishlist):
            self.wishlists.add(wishlist)
        if(product):
            self.product = product
        
    def set_product(self, product):
        self.product = product

    def get_product(self):
        return self.product

    @property
    def name(self):
        return self.product.name
    
    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()
    
    def image_url(self):
        return self.product.image.url