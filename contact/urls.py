from django.conf.urls import url
from contact import views


app_name = 'contact'
urlpatterns = [
            url(r'^$', views.index, name='index'),
]
