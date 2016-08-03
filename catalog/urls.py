from django.conf.urls import url
from catalog import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.show_category,
        name='catalog_category'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product,
        name='product_details'),

]
