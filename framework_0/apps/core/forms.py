from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=100, required=True)
    password = forms.CharField(label=_('Password'), max_length=100, widget=forms.PasswordInput(), required=True)


class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=255, required=True)
    message = forms.CharField(label='Message', max_length=1000, widget=forms.Textarea(), required=True)
