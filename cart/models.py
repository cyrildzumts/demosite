from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from cart.cart_exceptions import QuantityError
# Create your models here.

"""
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session)


def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
    )

user_logged_in.connect(user_logged_in_handler)


def delete_user_session(user):
    user_sessions = UserSession.objects.filter(user=user)
    for user_session in user_sessions:
        user_session.session.delete()

"""


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']

    def __str__(self):
        return "Cart id : %d\nUser :%s" % (self.id, self.user)

    def add_to_cart(self, product, quantity=1):
        """
        Add a new product into the Shopping Cart.
        If the product is already in the cart then
        update the quantity.
        If not then create a new CartItem and set
        appropriate value for its variable and save.
        """
        item_in_cart = False
        items = self.cartitem_set.all()
        for item in items:
            if item.product.pk == product.pk:
                q = item.get_quantity() + quantity
                self.update_quantity(item.pk, q)
                item_in_cart = True
        if not item_in_cart:
            # create and save a new cart item
            item = CartItem()
            item.set_product(product)
            item.set_quantity(quantity)
            item.set_cart(self)
            item.save()

    def get_item(self, item_id):
        """
        Return a CartItem object when found
        """
        return get_object_or_404(CartItem,
                                 pk=item_id,
                                 cart=self)

    def update_quantity(self, item_id, quantity):
        """
        Update the CartItem quantity to the value
        of quantity.
        If quantity = 0, the corresponding CartItem will
        be deleted.
        """
        item = self.get_item(item_id)
        if item:
            if quantity > 0:

                item.set_quantity(quantity)
                item.save()
            else:
                self.remove_from_cart(item_id)

    def remove_from_cart(self, item_id):
        """
        Delete the CartItem corresponding to item_id.
        """
        item = self.get_item(item_id)
        if item:
            item.delete()

    def subtotal(self):
        """
        Return the subtotal amount for the
        items available in the Cart.
        """
        cart_total = 0
        items = self.get_items()
        for item in items:
            cart_total += item.total_price()
        return cart_total

    def get_items(self):
        """
        Return all the items present in the Cart.
        """
        return self.cartitem_set.all()

    def items_count(self):
        """
        Return the number of items present in the Cart.
        """
        count = 0
        items = self.get_items()
        for item in items:
            count += item.quantity
        return count

    def refresh(self):
        pass

    def get_user(self):
        return self.user

    def get_id(self):
        return self.id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, unique=False, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('catalog.Product', unique=False)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def set_quantity(self, quantity):
        if quantity <= self.product.quantity:
            self.quantity = quantity
        else:
            raise QuantityError(available=self.product.quantity,
                                value=quantity)

    def get_quantity(self):
        return self.quantity

    def set_product(self, product):
        self.product = product

    def get_product(self):
        return self.product

    def set_cart(self, cart):
        self.cart = cart

    def get_cart(self):
        return self.cart

    def get_quantity(self):
        return self.quantity

    def total(self):
        return self.product.price * self.quantity

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def total_price(self):
        return self.product.price * self.quantity

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def change_quantity(self, quantity):
        if quantity <= self.product.quantity:
            self.quantity = quantity
            self.save()
        else:
            raise QuantityError(available=self.product.quantity,
                                value=quantity)


class LineItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(
                type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(LineItemManager, self).get(*args, **kwargs)


class LineItem(models.Model):
    unit_price = models.IntegerField()
    quantity = models.PositiveIntegerField()

    # defining product as a generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LineItemManager()

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ['-created_at']

    def __str__(self):
        return "%d pieces de %s" % (
            self.quantity, self.product.__class__.__name__)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    # product definition
    @property
    def product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    @product.setter
    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk
