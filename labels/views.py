from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from task_manager.mixins import AuthRequiredMixin
from labels.models import Label
from labels.forms import LabelForm


class LabelsListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully created')


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully updated')


class LabelDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully deleted')

    def form_valid(self, form):
        label = self.get_object()
        if label.tagged_tasks.all():
            messages.error(self.request, gettext_lazy(
                'Unable to delete label because its in use'
            ))
            return redirect(self.success_url)
        return super().form_valid(form)
