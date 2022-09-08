from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.urls import reverse_lazy

from users.models import User
from tasks.models import Task


class AuthRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            self.login_url = 'login'
            self.error_message = gettext('You need to log in to view this page')
            messages.error(self.request, self.error_message)
            return super().handle_no_permission()
        else:
            messages.error(self.request, self.error_message)
            return redirect(self.error_url)


class AccessRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        target_object = self.get_object()
        if type(target_object) is User:
            self.error_url = reverse_lazy('users')
            return self.request.user.pk == target_object.pk
        elif type(target_object) is Task:
            self.error_url = reverse_lazy('tasks')
            return self.request.user.pk == target_object.author.pk
        return False
