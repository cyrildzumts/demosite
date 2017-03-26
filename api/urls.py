from django.conf.urls import url, include
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, ProductViewSet, CartItemViewSet, CartViewSet
from demosite import settings
from api import views
app_name = 'api_app'

categories = CategoryViewSet.as_view({
    'get': 'list'
})

products = ProductViewSet.as_view({
    'get': 'list'
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve'
})

router = DefaultRouter(schema_title=settings.SITE_NAME, schema_renderers=[
    renderers.CoreJSONRenderer]
    )
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cartItems', CartItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ajax/ajax_login/$', views.ajax_login, name='ajax_login'),
]
