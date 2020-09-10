from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(
        User,
        related_name='my_groups'
    )

class Task(models.Model):
    name = models.CharField(max_length=150)
    desc = models.TextField(max_length=500)
    group = models.ForeignKey(
        Group,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        related_name='group_tasks'
    )
    in_charge = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    due_date = models.DateField()
    is_done = models.BooleanField(
        default=False
    )
