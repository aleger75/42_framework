from .views import *
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', AdminView.as_view(), name='admin_view'),
                       url(r'logas/$', LoginAs.as_view(), name='log_as'),

                       url(r'users/$', UserView.as_view(), name='user_view'),
                       url(r'user/create/$', UserCreate.as_view(), name='user_create'),
                       url(r'user/(?P<pk>\d+)/update/$', UserUpdate.as_view(), name='user_update'),
                       url(r'user/(?P<pk>\d+)/delete/$', UserDelete.as_view(), name='user_delete'),

                       url(r'forum/$', ForumAdmin.as_view(), name='forum_admin'),
                       url(r'forum/add/category/$', ForumAddCategory.as_view(), name='forum_add_category'),
                       url(r'forum/add/subcategory/$', ForumAddSubCategory.as_view(), name='forum_add_subcategory'),
                       url(r'forum/category/(?P<pk>\d+)/update/$', ForumUpdateCategory.as_view(),
                           name='forum_update_category'),
                       url(r'forum/subcategory/(?P<pk>\d+)/update/$', ForumUpdateSubCategory.as_view(),
                           name='forum_update_subcategory'),
                       url(r'forum/category/(?P<pk>\d+)/delete/$', ForumDeleteCategory.as_view(),
                           name='forum_delete_category'),
                       url(r'forum/subcategory/(?P<pk>\d+)/delete/$', ForumDeleteSubCategory.as_view(),
                           name='forum_delete_subcategory'),
)
