from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from functools import partial

# https://djangosnippets.org/snippets/2607/ - include decorators


def required(wrapping_functions, patterns_rslt):
    """
    Used to require 1..n decorators in any view returned by a url tree

    Usage:
      urlpatterns = required(func,patterns(...))
      urlpatterns = required((func,func,func),patterns(...))

    Note:
      Use functools.partial to pass keyword params to the required
      decorators. If you need to pass args you will have to write a
      wrapper function.

    Example:
      from functools import partial

      urlpatterns = required(
          partial(login_required,login_url='/accounts/login/'),
          patterns(...)
      )
    """
    if not hasattr(wrapping_functions, '__iter__'):
        wrapping_functions = (wrapping_functions,)

    return [
        _wrap_instance__resolve(wrapping_functions, instance)
        for instance in patterns_rslt
    ]


def _wrap_instance__resolve(wrapping_functions, instance):
    if not hasattr(instance, 'resolve'): return instance
    resolve = getattr(instance, 'resolve')

    def _wrap_func_in_returned_resolver_match(*args, **kwargs):
        rslt = resolve(*args, **kwargs)
        if not hasattr(rslt, 'func'): return rslt
        f = getattr(rslt, 'func')
        for _f in reversed(wrapping_functions):
            # @decorate the function from inner to outter
            f = _f(f)
        setattr(rslt, 'func', f)
        return rslt

    setattr(instance, 'resolve', _wrap_func_in_returned_resolver_match)

    return instance


urlpatterns = patterns('',
       url(r'^admin/', include(admin.site.urls)),
       url(r'stop_logas/$', 'apps.admin_p.views.custom_unimpersonate', name='stop_log_as'),
       url(r'', include('apps.core.urls')),
)

urlpatterns += required(
    partial(login_required, login_url='/login/'),
    patterns('',
             (r'^tickets/', include('apps.tickets.urls')),
             (r'^forum/', include('apps.forum.urls')),
    )
)

urlpatterns += required(
    (
        partial(login_required, login_url='/login/'),
        partial(staff_member_required, login_url='/login/')
    ),
    patterns('',
             (r'^admin_p/', include('apps.admin_p.urls')),
    )
)
