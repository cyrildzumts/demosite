from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import Customer, UserProfile


# Register your models here.
# Define an inline admin descriptor for Customer Model
# This acts like a singleton


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profiles'


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customers'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,  )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
