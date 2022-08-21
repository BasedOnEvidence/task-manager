from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView

from django_filters.views import FilterView

from task_manager.mixins import LoginAndAccessPermissionMixin, LoginPermissionMixin
from tasks.forms import TaskForm, TasksFilter
from tasks.models import Task
from users.models import User


class TasksListView(LoginPermissionMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TasksFilter


class TaskCreateView(LoginPermissionMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully created'

    def form_valid(self, form):
        form.instance.author = User.objects.get(id=self.request.user.pk)
        return super().form_valid(form)


class TaskUpdateView(LoginPermissionMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully updated'


class TaskDeleteView(LoginAndAccessPermissionMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully deleted'
    error_url = reverse_lazy('users')
    error_message = 'You have no access to delete this task'

    def test_func(self):
        return self.request.user.pk == self.get_object().author.pk


class TaskView(LoginPermissionMixin, DetailView):
    model = Task
    template_name = 'tasks/view.html'
