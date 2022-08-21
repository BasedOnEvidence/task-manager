from django.utils.translation import gettext_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy

from task_manager.mixins import LoginPermissionMixin
from statuses.models import Status
from statuses.forms import StatusForm


class StatusesListView(LoginPermissionMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginPermissionMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully created')


class StatusUpdateView(LoginPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully updated')


class StatusDeleteView(LoginPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully deleted')
