from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    country = models.CharField(default='', max_length=50, blank=True)
    city = models.CharField(max_length=50)
    # joined = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    country = models.CharField(default='', max_length=50, blank=True)
    city = models.CharField(max_length=50)
    province = models.CharField(default='', max_length=50)
    address = models.CharField(default='', max_length=50)
    zip_code = models.CharField(max_length=15)
    telefon = models.CharField(default='', max_length=15)
    newsletter = models.BooleanField(default=False)
    is_active_account = models.BooleanField(default=True)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profil = UserProfile(user=user)
        user_profil.save()
post_save.connect(create_profile, sender=User)
