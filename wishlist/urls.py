from django.conf.urls import url
from wishlist import views

app_name = 'wishlist'
urlpatterns = [
            url(r'^$', views.show_wishlist, name='show_wishlist'),
            url(r'^add_to_wishlist/(?P<item_id>\d+)/$', views.add_to_wishlist,
                name='add_to_wishlist'),
            url(r'^ajax_remove_from_wishlist/$', views.ajax_remove_from_wishlist, name='ajax_remove_from_wishlist'),
            url(r'^ajax_add_to_wishlist/$', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),
            
            url(r'^clear$', views.clear, name='clear'),
            url(r'^remove_from_wishlist/(?P<item_id>\d+)/$', views.remove_from_wishlist,
                name='remove_from_wishlist'),
]
