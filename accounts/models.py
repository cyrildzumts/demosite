from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, username, date_of_birth, email, password=None):
        """
        Creates and saves a user with the given parametters
        """
        if not username and not date_of_birth and not email:
            raise ValueError('Veuillez remplir tous les champs')
        user = self.model(username=username,
                          email=self.normalize_email(email),
                          date_of_birth=date_of_birth,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, username, date_of_birth, email, password):
        user = self.create_user(username, date_of_birth, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class Customer(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50)
    # password = models.CharField()
    email = models.EmailField('adresse email', unique=True, db_index=True)
    date_of_birth = models.DateField()

    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    objects = CustomerManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FILDS = ['date_of_birth']

    def __str__(self):
        return self.username

    class Meta:
        db_table = "customers"

    def get_full_name(self):
        return "%s %s" % (self.firstname, self.lastname)

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
