from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

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

    def form_valid(self, form):
        status = self.get_object()
        if status.status_tasks.all():
            messages.error(self.request, gettext_lazy(
                'Unable to delete status because its in use'
            ))
            return redirect(self.success_url)
        return super().form_valid(form)
