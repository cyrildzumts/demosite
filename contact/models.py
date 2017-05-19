from django.db import models
# Create your models here.


class Contact(models.Model):
    username = models.CharField(max_length=50, blank=True)
    sender = models.EmailField(blank=True)
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    cc_myself = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact'
        ordering = ['-created_at']
        verbose_name_plural = 'contacts'

    def __str__(self):
        return str(self.created_at + " " + self.user.username)
