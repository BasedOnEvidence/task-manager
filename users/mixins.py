from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class AccessRequiredMixin(UserPassesTestMixin):
    error_url = reverse_lazy('users')

    def handle_no_permission(self):
        messages.error(self.request, self.error_message)
        return redirect(self.error_url)

    def test_func(self):
        user = self.get_object()
        return self.request.user.pk == user.pk
