from django.forms import ModelForm, CheckboxInput
from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django.utils.translation import gettext_lazy

from tasks.models import Task, User, Label, Status


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status', 'executor', 'description', 'labels']


class TasksFilter(FilterSet):
    status = ModelChoiceFilter(label=gettext_lazy('Status'), queryset=Status.objects.all())
    executor = ModelChoiceFilter(label=gettext_lazy('Performer'), queryset=User.objects.all())
    labels = ModelChoiceFilter(label=gettext_lazy('Label'), queryset=Label.objects.all())
    current_user_tasks = BooleanFilter(
        widget=CheckboxInput(),
        method='filter_task_author',
        label=gettext_lazy('Only my tasks')
    )

    def filter_task_author(self, queryset, field_name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'current_user_tasks']
