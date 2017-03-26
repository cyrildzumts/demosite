from catalog.models import Category, Product
from cart.models import Cart, CartItem
from api.serializers import CategorySerializer, ProductSerializer,\
    CartSerializer, CartItemSerializer
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import urlresolvers
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from demosite import settings


# Create your views here.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


# defining login function api for ajax calls
def ajax_login(request):
    """
    AJAX Log in view
    """
    data = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],
                                 password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                data['status'] = 200
                data['redirect_url'] = settings.LOGIN_REDIRECT_URL
        else:
            data['status'] = 404
    return JsonResponse(data)
