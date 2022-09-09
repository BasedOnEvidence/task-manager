from django.db import models

from users.models import User
from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author_tasks')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executable_tasks')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='status_tasks')
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, related_name='tagged_tasks', blank=True)

    def __str__(self):
        return self.name
