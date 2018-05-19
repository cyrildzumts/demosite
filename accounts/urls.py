from django.conf.urls import url
# from demosite import settings
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_account/$', views.user_account, name='user_account'),
    url(r'^edit_user_infos/$', views.UserProfileUpdateView.as_view(), name='edit_user_infos'),
    #url(r'^login', views.login, name='login'),
    #url(r'^logout', views.logout, name='logout'),
    url(r'^login', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^orders/$', views.show_orders, name='orders'),
    url(r'^orders/(?P<order_id>\d+)/$', views.order_details,name='order_details'),
    url('^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url('^password_change/done$', auth_views.PasswordChangeView.as_view(), name='password_change_done'),
    url('^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url('^password_reset/done$', auth_views.PasswordResetView.as_view(), name='password_reset_done'),
]
