from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy

from users.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=gettext_lazy('Name'), required=True)
    last_name = forms.CharField(label=gettext_lazy('Last name'), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
