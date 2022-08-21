from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext


class LoginPermissionMixin(LoginRequiredMixin):
    error_message = None
    login_url = None
    request = None

    def handle_no_permission(self):
        self.error_message = gettext('You need to log in to view this page')
        self.login_url = 'login'
        messages.error(self.request, self.error_message)
        return super().handle_no_permission()


class LoginAndAccessPermissionMixin(LoginPermissionMixin, UserPassesTestMixin):
    error_message = None
    error_url = None
    request = None

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, self.error_message)
        return redirect(self.error_url)
