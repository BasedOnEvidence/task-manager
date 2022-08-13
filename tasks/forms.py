from django.forms import ModelForm

from tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status', 'performer', 'description', 'labels']
