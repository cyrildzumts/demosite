from rest_framework import serializers
from catalog.models import Product, Category, Parfum, Phablet
from accounts.models import Customer
from cart.models import Cart, CartItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # cart = serializers.PrimaryKeyRelatedField(
    #    many=False,
    #    queryset=Cart.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'brand', 'description', 'price',
            'old_price', 'quantity', 'sku', 'image'
        ]


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user']


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=False, read_only=True)
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'quantity', 'product']
