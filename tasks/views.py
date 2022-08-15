from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from django_filters.views import FilterView

from tasks.forms import TaskForm, TasksFilter
from tasks.models import Task
from users.models import User


class TasksListView(FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TasksFilter


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully created'

    def form_valid(self, form):
        form.instance.author = User.objects.get(id=self.request.user.pk)
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully updated'


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully deleted'


class TaskView(DetailView):
    model = Task
    template_name = 'tasks/view.html'
