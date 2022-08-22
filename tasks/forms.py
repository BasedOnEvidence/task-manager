from django.forms import ModelForm
from django_filters import FilterSet
from django.utils.translation import gettext_lazy

from tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status', 'executor', 'description', 'labels']
        labels = {
            'name': gettext_lazy('Name'),
            'status': gettext_lazy('Status'),
            'executor': gettext_lazy('Performer'),
            'description': gettext_lazy('Description'),
            'labels': gettext_lazy('Labels')
        }


class TasksFilter(FilterSet):
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
        labels = {
            'status': gettext_lazy('Status'),
            'executor': gettext_lazy('Performer'),
            'labels': gettext_lazy('Labels')
        }
