from django import forms
from order.models import Order
import datetime
import re


# Checkout Options
PAID_TYPE = (
                        ('SMS', 'SMS'),
                        ('OrangeMoney', 'OrangeMoney'),
                        ('MTNMoney', 'MTNMoney'),
                        ('AirtelMoney', 'AirtelMoney'),)


class CheckoutForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(CheckoutForm, self).__init__(*args, **kwargs)
            # override default attributes
            for field in self.fields:
                self.fields[field].widget.attrs['size'] = '30'
            self.fields['shipping_state'].widget.attrs['size'] = '3'
            self.fields['shipping_zip'].widget.attrs['size'] = '6'
            self.fields['billing_state'].widget.attrs['size'] = '3'
            self.fields['billing_zip'].widget.attrs['size'] = '6'
            self.fields['shipping_state'].widget.attrs['size'] = '3'

        class Meta:
            model = Order
            exclude = ('status', 'ip_address', 'user', 'transaction_id',)
        payement_type = forms.CharField(widget=forms.Select(choices=PAID_TYPE))
