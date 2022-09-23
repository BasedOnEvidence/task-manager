from django.db import models
from django.utils.translation import gettext_lazy


class Status(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name=gettext_lazy('Name'))
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
