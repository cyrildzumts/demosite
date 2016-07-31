from django.conf import settings
from django.contrib.auth.models import check_password
from accounts.models import Customer


class EmailAuthBackend(object):
    """
    A custom authentication backend.
    It allows users to log with their email address
    """
    def authenticate(self, email=None, password=None):
        """
        authentication method
        """
        try:
            user = Customer.objects.get(email=email)
            if user.check_password(password):
                return user
        except Customer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Customer.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except Customer.DoesNotExist:
            return None
