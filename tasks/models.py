from django.db import models
from django.utils.translation import gettext_lazy

from users.models import User
from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author_tasks')
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executable_tasks',
        verbose_name=gettext_lazy('Performer')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Status')
    )
    description = models.TextField(blank=True, verbose_name=gettext_lazy('Description'))
    creation_date = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        blank=True,
        through='TaskLabelsRelations',
        through_fields=('task', 'label'),
        verbose_name=gettext_lazy('Labels')
    )

    def __str__(self):
        return self.name


class TaskLabelsRelations(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
