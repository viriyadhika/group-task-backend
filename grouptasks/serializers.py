from django.contrib.auth.models import User
from rest_framework import serializers

from grouptasks.models import Group, Task, Membership

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
            'pk',
            'username',
            'email',
            'my_groups',
        )

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
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
            'pk',
            'name',
            'group_tasks',
            'members',
        )

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    in_charge = UserSummarySerializer()

    class Meta:
        model = Task
        fields = (
            'url',
            'pk',
            'name',
            'desc',
            'group',
            'in_charge',
            'due_date',
            'is_done',
        )


class GroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'pk',
            'name'
        )


class TaskSummarySerializer(serializers.ModelSerializer):
    group = GroupSummarySerializer()

    class Meta:
        model = Task
        fields = (
            'pk',
            'name',
            'desc',
            'group',
            'in_charge',
            'due_date',
            'is_done',
        )

class TaskListofAUserSerializer(serializers.HyperlinkedModelSerializer):
    my_tasks = TaskSummarySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'my_tasks',
        )

class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'name',
            'desc',
            'group',
            'in_charge',
            'due_date',
        )

class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    class Meta:
        model = Membership
        fields = (
            'url',
            'user',
            'group',
        )
