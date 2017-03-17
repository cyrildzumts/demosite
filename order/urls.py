from django.conf.urls import url
from order import views
from demosite import settings


app_name = 'order'

urlpatterns = [
    url(r'^$', views.show_checkout, name='checkout'),
    url(r'checkout/$', views.show_checkout, name='checkout'),
    url(r'receipt/$', views.receipt, name='receipt'),
]
