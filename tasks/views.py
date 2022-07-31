from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from tasks.models import Status
from tasks.forms import StatusForm


class StatusesListView(generic.ListView):
    model = Status
    template_name = 'tasks/statuses_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'tasks/statuses_create.html'
    success_url = reverse_lazy('statuses:statuses')


class StatusChangeView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'tasks/statuses_change.html'
    success_url = reverse_lazy('statuses:statuses')


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'tasks/statuses_delete.html'
    success_url = reverse_lazy('statuses:statuses')
