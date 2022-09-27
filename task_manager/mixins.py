from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext
from django.shortcuts import redirect


class AuthRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, gettext('You need to log in to view this page'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class ProtectedDeleteMixin():

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
        except ProtectedError:
            messages.error(self.request, self.error_message)
        return redirect(self.success_url)
