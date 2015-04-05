from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import LoginView, Register, Send
from .forms import ContactForm

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='index.html'), {'form': ContactForm()}, name='index'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
                       url(r'^register/$', Register.as_view(), name='register'),
                       url(r'^send/$', Send.as_view(), name='send'),
)
