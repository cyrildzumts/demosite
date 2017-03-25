"""demosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.views import login, logout
# from demosite import views

urlpatterns = [
    url(r'^order/', include('order.urls')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api/api-auth/', include('rest_framework.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('catalog.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
