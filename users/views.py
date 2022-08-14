from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from users.forms import RegistrationForm, LoginForm
from users.models import User


class UsersList(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Registration successfuly completed. Use your username and password to login'


class UserLoginView(SuccessMessageMixin, LoginView):
    model = User
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')
    success_message = 'You have successfully logged in'


class UserLogoutView(LogoutView):
    model = User
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have successfully logged out')
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'users/update.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('users')
    success_message = 'You have successfully updated profile'


class UserDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('home')
    success_message = 'Profile have been deleted'

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
