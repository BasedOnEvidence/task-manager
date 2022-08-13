from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView

from tasks.forms import TaskForm
from tasks.models import Task
from users.models import User


class TasksListView(ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Task successfully created'

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
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
