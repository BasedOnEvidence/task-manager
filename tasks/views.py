from django.utils.translation import gettext_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from django_filters.views import FilterView

from task_manager.mixins import AuthRequiredMixin
from tasks.mixins import AccessRequiredMixin
from tasks.forms import TaskForm, TasksFilter
from tasks.models import Task


class TasksListView(AuthRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TasksFilter


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = gettext_lazy('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = gettext_lazy('Task successfully updated')


class TaskDeleteView(AuthRequiredMixin, AccessRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = gettext_lazy('Task successfully deleted')
    error_message = gettext_lazy('You have no access to delete this task')


class TaskView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/view.html'
