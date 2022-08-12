from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from statuses.models import Status
from statuses.forms import StatusForm


class StatusesListView(generic.ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')


class StatusChangeView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/change.html'
    success_url = reverse_lazy('statuses')


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
