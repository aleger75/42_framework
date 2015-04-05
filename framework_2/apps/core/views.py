from .forms import LoginForm
from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from apps.admin_p.models import AdminLogs
from django.contrib.auth.views import logout
import ldap3
from django.conf import settings
import json
from django.http import HttpResponse


class Index(TemplateView):
    template_name = 'index.html'
    http_method_names = [u'get', u'post']

    def post(self, request, *args, **kwargs):
        login = request.POST['login']
        uid = 'uid=' + login
        base_dn = 'ou=paris,ou=people,dc=42,dc=fr'
        login_dn = 'uid=aleger,ou=september,ou=2013,ou=paris,ou=people,dc=42,dc=fr'
        server = ldap3.Server(use_ssl=True, host='ldaps://ldap.42.fr', port=636, get_info=ldap3.ALL)
        connection = ldap3.Connection(server,
                read_only=True,
                authentication=ldap3.AUTH_SIMPLE,
                check_names=True,
                auto_bind=True,
                user=login_dn,
                password=settings.LDAP_PASSWORD)
        try:
            connection.search(search_base=base_dn,
                    search_filter='('+uid+')',
                    search_scope=ldap3.SEARCH_SCOPE_WHOLE_SUBTREE,
                    attributes=ldap3.ALL_ATTRIBUTES)
            data = connection.response[0]['attributes']
        except:
            data = None
            return HttpResponse("None")
        response_data = {}
        response_data['full_name'] = data.get('cn')
        response_data['uid'] = data.get('uid')
        response_data['mobile'] = data.get('mobile')
        response_data['alias'] = login + '@student.42.fr'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        form = self.form_class()
        try:
            next = request.GET['next']
        except:
            next = '/'
        return render(request, self.template_name, {'form': form, 'next': next})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            year = form.cleaned_data.get('year')
            pool = form.cleaned_data.get('pool')
            base_dn = ',ou=paris,ou=people,dc=42,dc=fr'
            dn = 'uid='+username+',' + 'ou='+pool + ',ou='+year + base_dn
            server = ldap3.Server(use_ssl=True, host='ldaps://ldap.42.fr', port=636, get_info=ldap3.ALL)
            try:
                connection = ldap3.Connection(server, read_only=True, authentication=ldap3.AUTH_SIMPLE, check_names=True, auto_bind=True, user=dn, password=password)
            except ldap3.core.exceptions.LDAPBindError:
                connection = None
            if connection is not None:
                try:
                    user = User.objects.get(username=username)
                except:
                    user = None
                if user is None:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                log = AdminLogs(user=user, action=_('signed in'))
                log.save()
                return redirect(request.POST['next'])
        form.add_error('password', _('Invalid password'))
        form.add_error('username', _('Invalid username'))
        form.add_error('year', _('Invalid year'))
        form.add_error('pool', _('Invalid month'))
        messages.error(request, _('Invalid credentials. Try again'))
        return render(request, self.template_name, {'form': form, 'next': request.POST['next']})


class Register(CreateView):
    model = User
    fields = ['username', 'password', 'email', 'first_name', 'last_name']
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mail = form.cleaned_data.get('email')
            f_name = form.cleaned_data.get('first_name')
            l_name = form.cleaned_data.get('last_name')
            User.objects.create_user(username=username, email=mail, password=password, first_name=f_name,
                                     last_name=l_name)
            user = authenticate(username=username, password=password)
            login(request, user)
            l = AdminLogs(user=user, action=_('registered'))
            l.save()
            return redirect('/')
        messages.error(request, _('Invalid informations. Try again'))
        form = self.get_form_class()
        form.fields['password'].widget = forms.PasswordInput()
        return render(request, self.template_name, {'form': form})


def sign_out(request):
    l = AdminLogs(user=request.user, action=_('signed out'))
    l.save()
    return logout(request, next_page='/')
