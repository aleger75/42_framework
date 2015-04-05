from django.conf.urls import patterns, url
from django.contrib.auth.decorators import user_passes_test
from .views import TicketsView, TicketsCreate, TicketsAnswer, TicketsOpen, TicketsClose, TicketsAssign

urlpatterns = patterns('',
                       url(r'^$', TicketsView.as_view(), name='tickets_view'),
                       url(r'^create/$', TicketsCreate.as_view(), name='tickets_create'),
                       url(r'^view/(?P<pk>\d+)/$', TicketsAnswer.as_view(), name='tickets_answer'),
                       url(r'^view/(?P<pk>\d+)/open/$', TicketsOpen.as_view(), name='tickets_open'),
                       url(r'^view/(?P<pk>\d+)/close/$', TicketsClose.as_view(), name='tickets_close'),
                       url(r'^view/(?P<pk>\d+)/assign/$',
                           user_passes_test(lambda u: u.is_staff, login_url='/login/')(TicketsAssign.as_view()),
                           name='tickets_assign'),
)
