from django import forms
from django.forms import ModelForm
from django_filters import FilterSet, BooleanFilter
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

    current_user_tasks = BooleanFilter(
        label=gettext_lazy('Only my tasks'),
        widget=forms.CheckboxInput(),
        method='filter_current_user',
        field_name='current_user_tasks'
    )

    def filter_current_user(self, queryset, field_name, box_is_checked):
        current_user = self.request.user
        if not current_user.is_anonymous and box_is_checked:
            return queryset.filter(author=current_user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'current_user_tasks']
        labels = {
            'status': gettext_lazy('Status'),
            'executor': gettext_lazy('Performer'),
            'labels': gettext_lazy('Labels')
        }
