from django.forms import ModelForm

from django_filters import FilterSet

from tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status', 'performer', 'description', 'labels']


class TasksFilter(FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'performer', 'labels']
