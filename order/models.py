from django.db import models
from django_email import mail
# from django import forms
from django.contrib.auth.models import User
from catalog.models import Product
# from cart.models import Cart, CartItem
import decimal
# from enum import Enum
import datetime

# Global Variable counting


# Create your models here.
class Order(models.Model):
    # class Variable Counter :
    Order_Count = 0
    # Order Status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    BEINGPROCESSED = 5
    FINISHED = 6

    # Set of possibles order statuses
    ORDER_STATUSES = (
        (SUBMITTED, 'Submitted'),
        (PROCESSED, 'Processed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
        (BEINGPROCESSED, 'Being processed'),
        (FINISHED, 'FINISHED'),)

    # Order Infos
    date = models.DateTimeField(auto_now_add=True)
    paid_status = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    transaction_id = models.CharField(max_length=20, blank=True)
    ref_num = models.BigIntegerField(blank=True, null=True)

    # Contact Infos
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    # Shipping Infos
    shipping_name = models.CharField(max_length=50)
    shipping_address_1 = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=50)
    shipping_zip = models.CharField(max_length=10)

    def __unicode__(self):
        return 'Order #' + str(self.id)

    def __str__(self):
        return 'Order #' + str(self.id)

    @property
    def total(self):
        total = 0
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    def generate_order_refNum(self):
        """
        Generate a reference number in this format :
        CurrentYear_CurrentMonth_CurrentDay_Incrementing_Number
        """
        Order.Order_Count += 1
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = datetime.datetime.now().hour
        minu = datetime.datetime.now().minute

        ref_str = (str(year) + str(month) + str(day) + str(hour) +
                   str(minu) + str(Order.Order_Count))
        self.ref_num = int(ref_str)
        return ref_str

    def set_paid(self):
        self.paid_status = True
        self.paid_at = datetime.datetime.now

    def get_paid_status(self):
        return self.paid_status

    def get_paid_date(self):
        return self.paid_at

    def set_order_status(self, status):
        if self.status != status:
            self.status = status

    @property
    def get_status(self):
        """
         Return a string representation of the order
         status.
         """
        return Order.ORDER_STATUSES[self.status-1][1]

    def get_date(self):
        return date.date()

    def populate(self, user_cart):
        self.populate_from_item_list(user_cart.get_items())

    def populate_from_item_list(self, cartitems):
        if cartitems:
            for item in cartitems:
                oi = OrderItem()
                oi.product = item.product
                oi.quantity = item.quantity
                oi.price = oi.product.price
                oi.order = self
                oi.save()

    def sent_confirmation_mail(selft):
        pass
    
    def getOrderItem(self):
        return self.orderitem_set.all()
    
    def get_quantity(self):
        return self.orderitem_set.count()

    def validate(self):
        """
        This Method is called when an order has been
        sent by an user. The stock inventory will be updated.
        The content ordered will update the stock quantity of
        the order item so that when there is no more item left
        no user will be able place a new order containing that item. 
        if the remaining quantity of the item is 0 then that item 
        will be marked as inactive. 
        """
        orderitems = self.getOrderItem()
        for item in orderitems:
            item.product.set_sell_quantity(item.quantity)
            item.product.sell_date = datetime.datetime.now()
            item.product.save()
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order)
    # class Meta:
    #    db_table = 'order_items'

    @property
    def get_price(self):
        return int(self.price)

    @property
    def total(self):
        return int(self.quantity * self.price)

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def __str__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def set_quantty(self, quantity):
        self.quantity = quantity
    
    def image_url(self):
        return self.product.image.url
    
    def order_ref(self):
        return self.order.ref_num
