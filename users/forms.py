from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except Exception:
            return username
        raise forms.ValidationError(f'Email {username} is already in use')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.get(email=email)
        except Exception:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')


class AuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Invalid username or password')


class UserAccountForm(forms.ModelForm):

    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.exclude(id=self.instance.id).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.exclude(id=self.instance.id).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')

    def save(self, commit=True):
        account = super(UserAccountForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        # account.password = self.cleaned_data['password']
        if commit:
            account.save()
        return account
