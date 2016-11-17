from cart.models import Cart, CartItem, LineItem, LineItemManager
from django.db import models
from django.contrib.auth.models import User


class Order (models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return "Order id : %d\nUser :%s" % (self.id, self.user)
