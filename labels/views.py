from django.utils.translation import gettext_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy

from task_manager.mixins import LoginPermissionMixin
from labels.models import Label
from labels.forms import LabelForm


class LabelsListView(LoginPermissionMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginPermissionMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully created')


class LabelUpdateView(LoginPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully updated')


class LabelDeleteView(LoginPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = gettext_lazy('Label successfully deleted')
