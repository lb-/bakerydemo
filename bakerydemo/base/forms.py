from django import forms
from wagtail.admin.forms.auth import LoginForm


class CustomLoginForm(LoginForm):
    captcha = forms.CharField(required=True)
