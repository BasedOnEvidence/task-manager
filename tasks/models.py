from django.db import models

from users.models import User
from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='performer')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, related_name='labels', blank=True)

    def __str__(self):
        return self.name
