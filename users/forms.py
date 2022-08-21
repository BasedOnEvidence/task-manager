from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']
