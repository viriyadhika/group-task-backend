from django.contrib import admin
from grouptasks.models import Task, Membership, Group

admin.site.register(Task)
admin.site.register(Membership)
admin.site.register(Group)
# Register your models here.
