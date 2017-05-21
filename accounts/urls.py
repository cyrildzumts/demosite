from django.conf.urls import url
# from demosite import settings
from django.contrib.auth.views import login, logout
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_account/$', views.user_account, name='user_account'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^orders/$', views.show_orders, name='orders'),
    url(r'^orders/(?P<order_id>\d+)/$', views.order_details,
        name='order_details'),
]
