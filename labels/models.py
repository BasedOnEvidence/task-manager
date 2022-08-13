from django.db import models


class Label(models.Model):
    name = models.CharField(unique=True, max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
