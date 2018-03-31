# Create your models here.
import datetime
from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from wishlist.wishlist_service import WishlistService

# Create your models here.

class Wishlist(models.Model):
    """
    A wishlist allow the user to save a list
    of interresting items to be consulted at another
    time.
    The user must be able Add a new Item into this list.
    The user must be able to an Item from the list.
    The user must be able to add the items from this list into the 
    Cart.
    """
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
        Add a new product into the Wishlist.
        If the product is already in the list, does nothing.
        If not then create a new WishlistItem and set
        appropriate value for its variable and save.
        """
        product_id = int(product_id)
        start_time = datetime.datetime.now()
        #items = self.get_items()
        added = False
        duplicate = WishlistService.contains_item(self.id, product_id)
        #for item in items:
        #    if item.product.pk == product_id:
        #        item_in_wishlist = True
        #        duplicate = True
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Wishlist : add() check processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        if not duplicate:
            # create and save a new Wishlist item
            product = Product.objects.get(id=product_id)
            item = WishlistItem(product=product)
            item.save()
            # item.set_product(product)
            self.wishlistitem_set.add(item)
            added = True
        return {"added": added, "duplicated": duplicate }


    def get_item(self, item_id):
        """
        Return a WishlistItem object when found
        """
        return self.wishlistitem_set.get(id=item_id)

    def remove(self, item_id):
        """
        Delete the WishlistItem corresponding to item_id.
        """
        flag = True
        try:
            item = self.get_item(item_id)
            item.delete()
            print("item removed from wishlist")
        except ObjectDoesNotExist:
            flag = False
        return flag
            

    def get_items(self):
        """
        Return all the items present in the Wishlist.
        """
        return self.wishlistitem_set.all()

    def items_count(self):
        """
        Return the number of items present in the Wishlist.

        """
        count = 0
        start_time = datetime.datetime.now()
        count = WishlistService.items_count(self.id)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Wishlist : items_count() check processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        return count

    def get_user(self):
        """
        Return the Wishlist's owner
        """
        return self.user

    def get_id(self):
        """
        Return the Wishlist's ID
        """
        return self.id

    def clear(self):
        """
        This method clear the Wishlist content. This action
        is not reversible.
        """
        self.get_items().delete()


class WishlistItem(models.Model):
    """
    WishlistItem represents the an Item present in a Wishlist.
    WishlistItem is generic representation of the Product class,
    so much of all message send to this instance is delegated to
    the associated product member.
    """
    wishlists = models.ManyToManyField(Wishlist)
    product = models.ForeignKey('catalog.Product', unique=False)

    class Meta:
        db_table = 'wishlistitems'

    #def __init__():
        
        #if(product):
        #    print("Product not None")
        #    self.product = product
        #else :
        #    print("Product is None")
        #if(wishlist):
        #    print("Wishlist not None")
        #    self.wishlists.add(wishlist)
        #else :
        #    print("Wishlist is None")
        
    def set_product(self, product):
        """
        set the product associated with this WishlistItem
        """
        self.product = product

    def get_product(self):
        """
            Return the Product associated with this WishlistItem.
            Note that any changes applied to this product instance
            will be write into the database.

        """
        return self.product

    @property
    def name(self):
        """
        Return the name of the associated Product
        """
        return self.product.name
    
    @property
    def price(self):
        """
        Return the price of the associated Product
        """
        return self.product.price

    def get_absolute_url(self):
        """
        Return the URL of the associated Product
        """
        return self.product.get_absolute_url()


    def image_url(self):
        """
        Return the image URL of the associated Product
        """
        return self.product.image.url

