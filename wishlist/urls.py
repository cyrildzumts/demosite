from django.conf.urls import url
from wishlist import views

app_name = 'wishlist'
urlpatterns = [
            url(r'^$', views.show_wishlist, name='show_wishlist'),
            url(r'^add_to_wishlist/$', views.add_to_wishlist,
                name='add_to_wishlist'),
            url(r'^remove_from_wishlist/$', views.remove_from_wishlist,
                name='remove_from_wishlist'),
]
