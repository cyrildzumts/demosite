from cart.models import Cart, CartItem, LineItem, LineItemManager
from django.db import models
from django.contrib.auth.models import User
import datetime
from order.models import Order
"""
class Order (models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    ref = models.CharField(max_length=10)
    paid_status = models.BooleanField(default=False)
    paid_at = models.DateTimeField()
    delevery_status = models.BooleanField(default=False)
    delivered_at = models.DateTimeField()
    order_charge = models.IntegerField(default=0)
    items = models.ForeignKey(LineItem)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return "Order id : %d\nUser :%s" % (self.id, self.user)

    def get_paid_status(self):
        return self.paid_status

    def set_paid(self):
        self.paid_status = True
        self.set_paid_date(datetime.datetime.now)

    def get_paid_date(self):
        return self.paid_at

    def set_paid_date(self, date):
        self.paid_at = date

    def get_charge(self):
        return self.order_charge

    def get_lineItems(self):
        return None

    def set_delivered(self):
        self.delevery_status = True

    def set_delivered_date(self, date):
        self.delivered_at = date

    def get_reference_number(self):
        return self.ref

    def set_reference_number(self, ref_num):
        self.ref = ref_num

    def get_user(self):
        return user

    def get_creation_date(self):
        return self.created_at
"""


class OrderManager():
    order_counter = 0

    def validate_form(postdata):
        pass


#    def create_invoice(self):
