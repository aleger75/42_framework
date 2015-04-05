from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from apps.core.views import LoginView, Register, sign_out, Index

urlpatterns = patterns('',
                       url(r'^$', Index.as_view(), name='index'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^logout/$', sign_out, name='logout'),
                       url(r'^register/$', Register.as_view(), name='register'),
)
