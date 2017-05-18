from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact'
        ordering = ['-created_at']
        verbose_name_plural = 'contacts'

    def __str__(self):
        return str(self.created_at + " " + self.user.username)
