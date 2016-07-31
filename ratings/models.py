from django.db import models
from accounts.models import Customer
from catalog.models import BaseProduct
# Create your models here.
# A Rating Model represent only the Value available
# differentiated by the value
class Rating(models.Model):
    value = models.IntegerField(blank=True)

    def __str__(self):
        return "value : %s" % self.value

    class Meta:
        db_table = 'ratings'
        ordering = ['value']


class RatingEntry(models.Model):
    rating = models.ForeignKey(Rating)
    product = models.ForeignKey(BaseProduct)
    customer = models.ForeignKey(Customer, unique=False)

    def __str__(self):
        return "Rating for %s : %s" % (self.product.name, self.rating.value)

    class Meta:
        db_table = "rating_entries"
