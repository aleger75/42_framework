from .forms import LoginForm
from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.edit import CreateView


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
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.POST['next'])
                else:
                    messages.error(request, _('Your account is locked'))
                    return render(request, self.template_name, {'form': form})
            else:
                form.add_error('password', _('Invalid password'))
                form.add_error('username', _('Invalid username'))
                messages.error(request, _('Invalid combination of Username - Password. Try again'))
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
            return redirect('/')
        messages.error(request, _('Invalid informations. Try again'))
        form = self.get_form_class()
        return render(request, self.template_name, {'form': form})