from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext
from django.shortcuts import redirect


class AuthRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, gettext('You need to log in to view this page'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
