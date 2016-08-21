
from rest_framework import status, mixins, generics, permissions, viewsets
from catalog.models import BaseProduct, Phone, Parfum, Shoe, Bag, Category
from cart.models import Cart, CartItem
from api.serializers import CategorySerializer, ProductSerializer,\
    CartSerializer, CartItemSerializer


# Create your views here.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BaseProduct.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
