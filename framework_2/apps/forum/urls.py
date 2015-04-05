from .views import ForumView, ForumViewCategory, ForumViewSubCategory, ForumViewThread, ForumAnswer, ForumComment, \
    ForumNewThread
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', ForumView.as_view(), name='forum_view'),
                       url(r'^category/(?P<pk>\d+)/$', ForumViewCategory.as_view(), name='forum_view_category'),
                       url(r'^(?P<c_pk>\d+)/subcategory/(?P<sc_pk>\d+)/$', ForumViewSubCategory.as_view(),
                           name='forum_view_subcategory'),

                       url(r'^category/(?P<c_pk>\d+)/thread/(?P<t_pk>\d+)/$',
                           ForumViewThread.as_view(), name='forum_view_category_thread'),
                       url(r'^(?P<c_pk>\d+)/subcategory/(?P<sc_pk>\d+)/thread/(?P<t_pk>\d+)/$',
                           ForumViewThread.as_view(), name='forum_view_subcategory_thread'),

                       url(r'^category/(?P<c_pk>\d+)/thread/(?P<t_pk>\d+)/answer/$',
                           ForumAnswer.as_view(), name='forum_answer_category_thread'),
                       url(r'^(?P<c_pk>\d+)/subcategory/(?P<sc_pk>\d+)/thread/(?P<t_pk>\d+)/answer/$',
                           ForumAnswer.as_view(), name='forum_answer_subcategory_thread'),

                       url(r'^category/(?P<c_pk>\d+)/thread/(?P<t_pk>\d+)/comment/(?P<a_pk>\d+)/$',
                           ForumComment.as_view(), name='forum_comment_category_thread'),
                       url(r'^(?P<c_pk>\d+)/subcategory/(?P<sc_pk>\d+)/thread/(?P<t_pk>\d+)/comment/(?P<a_pk>\d+)/$',
                           ForumComment.as_view(), name='forum_comment_subcategory_thread'),

                       url(r'^category/(?P<c_pk>\d+)/create_thread/$', ForumNewThread.as_view(),
                           name='forum_new_category_thread'),
                       url(r'^category/(?P<c_pk>\d+)/subcategory/(?P<sc_pk>\d+)/create_thread/$',
                           ForumNewThread.as_view(), name='forum_new_subcategory_thread'),
)
