from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=150)

class Task(models.Model):
    name = models.CharField(max_length=150)
    desc = models.TextField(max_length=500)
    group = models.ManyToManyField(Group)
    in_charge = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    due_date = models.DateField()
    is_done = models.BooleanField(
        default=False
    )
