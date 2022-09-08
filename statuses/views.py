from django.utils.translation import gettext_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy

from task_manager.mixins import AuthRequiredMixin
from statuses.models import Status
from statuses.forms import StatusForm


class StatusesListView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully created')


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully updated')


class StatusDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = gettext_lazy('Status successfully deleted')
