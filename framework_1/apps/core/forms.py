from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=100, required=True)
    password = forms.CharField(label=_('Password'), max_length=100, widget=forms.PasswordInput(), required=True)
