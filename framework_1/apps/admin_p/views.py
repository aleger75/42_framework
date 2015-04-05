from apps.forum.models import Category, SubCategory
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


class ForumAdmin(ListView):
    model = Category
    template_name = 'forum_admin.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = SubCategory.objects.all()

        return context


class ForumAddMeta(SuccessMessageMixin, CreateView):
    template_name = 'forum_add_category.html'
    success_message = _('%(name)s was successfully created')
    success_url = reverse_lazy('forum_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['title'].required = True

        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, name=self.object.title)


class ForumAddCategory(ForumAddMeta):
    model = Category
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sc'] = False

        return context


class ForumAddSubCategory(ForumAddMeta):
    model = SubCategory
    fields = ['title', 'parent_category']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['parent_category'].required = True
        context['is_sc'] = True

        return context


class ForumUpdateMeta(SuccessMessageMixin, UpdateView):
    template_name = 'forum_update_category.html'
    success_url = reverse_lazy('forum_admin')
    success_message = _('%(name)s was successfully updated')
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            new_title = title if title or title != self.object.title else None
            if title:
                self.object.title = new_title
                self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, name=self.object.title)


class ForumUpdateCategory(ForumUpdateMeta):
    model = Category
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sc'] = False

        return context


class ForumUpdateSubCategory(ForumUpdateMeta):
    model = SubCategory
    fields = ['title', 'parent_category']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sc'] = True

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            parent_category = form.cleaned_data.get('parent_category')
            new_parent_category = parent_category if parent_category != self.object.parent_category.title else None
            if new_parent_category:
                self.object.parent_category = new_parent_category
            return super().post(request, *args, **kwargs)
        else:
            return self.form_invalid(form)


class ForumDeleteMeta(DeleteView):
    success_url = reverse_lazy('forum_admin')
    template_name = 'forum_delete_category.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Category was successfully deleted')
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class ForumDeleteCategory(ForumDeleteMeta):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sc'] = False

        return context


class ForumDeleteSubCategory(ForumDeleteMeta):
    model = SubCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sc'] = True

        return context
