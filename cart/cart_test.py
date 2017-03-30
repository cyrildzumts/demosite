from django.contrib.auth.models import User
from .models import Cart


def test_cart():
    user = User.objects.get(username='cyrildz')
    ucart = Cart.objects.get(user=user)
    ci_first = ucart.cartitem_set.first()
    print(ucart.contain_item(ci_first.product.pk))
    ucart.contain_item(0)
    ucart.contain_item(45)
    ucart.contain_item(-3)
    ucart.contain_item(-1)
