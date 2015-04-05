from .views import *
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', AdminView.as_view(), name='admin_view'),

                       url(r'users/$', UserView.as_view(), name='user_view'),
                       url(r'user/create/$', UserCreate.as_view(), name='user_create'),
                       url(r'user/(?P<pk>\d+)/update/$', UserUpdate.as_view(), name='user_update'),
                       url(r'user/(?P<pk>\d+)/delete/$', UserDelete.as_view(), name='user_delete'),
)
