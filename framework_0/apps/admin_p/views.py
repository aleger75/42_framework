from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView


class AdminView(TemplateView):
    template_name = 'admin.html'


class UserView(ListView):
    template_name = 'users.html'
    model = User
    context_object_name = 'users'


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    success_url = reverse_lazy('user_view')
    success_message = _('User was successfully updated')
    template_name = 'user_update.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            form.instance.set_password(password)
            return self.form_valid(form)
        else:
            messages.error(request, _('Could not update profile. Try again'))
            return self.form_invalid(form)


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user_view')
    success_message = _('User was successfully deleted')
    template_name = 'user_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class UserCreate(SuccessMessageMixin, CreateView):
    model = User
    fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff']
    template_name = 'user_create.html'
    success_url = reverse_lazy('user_view')
    success_message = _('%(name)s was successfully created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['password'].widget = forms.PasswordInput()
        context['form'].fields['password'].required = True

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if password is not None:
                form.instance.set_password(password)
                return self.form_valid(form)
        messages.error(request, _('Could not create profile. Try again'))
        return self.form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, name=self.object)
