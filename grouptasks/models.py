from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(
        User,
        related_name='my_groups',
        through='Membership'
    )

class Membership(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        on_delete = models.CASCADE
    )
    class Meta:
        unique_together = ('user', 'group')

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
        on_delete = models.CASCADE,
        related_name='my_tasks'
    )
    due_date = models.DateField()
    is_done = models.BooleanField(
        default=False
    )
    def clean(self, *args, **kwargs):
        if self.in_charge not in self.group.members.all():
            raise ValidationError("The in charge doesn't belong to this group")
        super(Task, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Task, self).save(*args, **kwargs)
