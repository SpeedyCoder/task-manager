from django.conf import settings
from django.db import models

from model_utils.choices import Choices


class Task(models.Model):
    STATE = Choices(
        ('todo', 'TODO'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    state = models.CharField(choices=STATE, default=STATE.todo, max_length=20)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='completed_tasks', null=True, blank=True
    )

    def __str__(self):
        return self.name
