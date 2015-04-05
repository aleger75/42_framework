from django.contrib.auth.models import User
from apps.admin_p.models import AdminLogs

class ImpersonateMiddleware(object):
    def process_request(self, request):
        if request.user.is_staff and "__impersonate" in request.GET:
            request.session['impersonate_id'] = int(request.GET["__impersonate"])
            request.session['old_user'] = request.user.id
        if request.user.is_staff and 'impersonate_id' in request.session:
            request.user = User.objects.get(id=request.session['impersonate_id'])


class LoggerMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            user = request.user
            path = request.path
            new_log = AdminLogs(user=user, action='visited %s' % path)
            new_log.save()
