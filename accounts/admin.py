from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from accounts.models import Customer


# Register your models here.
# Define an inline admin descriptor for Customer Model
# This acts like a singleton

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customers'


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
