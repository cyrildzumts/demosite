from django import forms
from order.models import Order
import datetime
import re


class CheckoutForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(CheckoutForm, self).__init__(*args, **kwargs)
            # override default attributes
            for field in self.fields:
                self.fields[field].widget.attrs.update(
                    {'size': '30',
                     'class': 'form-control'}
                )
            self.fields['shipping_zip'].widget.attrs['size'] = '6'

        class Meta:
            model = Order
            exclude = ('status', 'ip_address', 'user', 'transaction_id',)
