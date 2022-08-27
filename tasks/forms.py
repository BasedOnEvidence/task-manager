from django.forms import ModelForm, CheckboxInput
from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django.utils.translation import gettext_lazy

from tasks.models import Task, User, Label, Status


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
    status = ModelChoiceFilter(label=gettext_lazy('Status'), queryset=Status.objects.all())
    executor = ModelChoiceFilter(label=gettext_lazy('Performer'), queryset=User.objects.all())
    labels = ModelChoiceFilter(label=gettext_lazy('Labels'), queryset=Label.objects.all())
    current_user_tasks = BooleanFilter(
        widget=CheckboxInput(),
        method='filter_current_user',
        label=gettext_lazy('Only my tasks')
    )

    def filter_current_user(self, queryset, field_name, box_is_checked):
        current_user = self.request.user
        if not current_user.is_anonymous and box_is_checked:
            return queryset.filter(author=current_user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'current_user_tasks']
