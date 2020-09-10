from django.contrib.auth.models import User
from rest_framework import serializers

from grouptasks.models import Group, Task

class UserSerializer(serializers.ModelSerializer):
    my_groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='group-detail'
    )

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
            'my_groups',
        )

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )

    group_tasks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='task-detail'
    )

    class Meta:
        model = Group
        fields = (
            'url',
            'name',
            'group_tasks',
            'members',
        )

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name = 'group-detail'
    )

    in_charge = serializers.HyperlinkedRelatedField(
        read_only = True,
        view_name = 'user-detail'
    )

    class Meta:
        model = Task
        fields = (
            'url',
            'name',
            'desc',
            'group',
            'in_charge',
            'due_date',
            'is_done',
        )