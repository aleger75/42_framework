from django import forms
from django.utils.translation import ugettext_lazy as _


class AnswerForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(), label=_('Your answer'))


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(), label=_('Comment'))


class NewThreadForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(), required=True, label=_('Title'))
    body = forms.CharField(widget=forms.Textarea(), required=True, label=_('Body'))
