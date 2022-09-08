from django.utils.translation import gettext_lazy, gettext
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from task_manager.mixins import AuthRequiredMixin, AccessRequiredMixin
from users.forms import RegistrationForm
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
    success_message = gettext_lazy(
        'Registration successfuly completed. Use your username and password to login'
    )


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')
    success_message = gettext_lazy('You have successfully logged in')


class UserLogoutView(LogoutView):
    model = User
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, gettext('You have successfully logged out'))
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(AuthRequiredMixin, AccessRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/update.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('users')
    success_message = gettext_lazy('You have successfully updated profile')
    error_message = gettext_lazy('You have no access to edit this profile')


class UserDeleteView(AuthRequiredMixin, AccessRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = gettext_lazy('Profile have been deleted')
    error_message = gettext_lazy('You have no access to delete this profile')
