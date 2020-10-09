from django.contrib.auth.models import User
from rest_framework import serializers

from grouptasks.models import Group, Task, Membership

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'email',
        )

class GroupSummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'url',
            'pk',
            'name',
        )
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    in_charge = UserSerializer()
    group = GroupSummarySerializer()

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

class MyTasksSerializer(serializers.HyperlinkedModelSerializer):
    my_tasks = TaskSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'my_tasks'
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

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    members = UserSerializer(many=True)
    group_tasks = TaskSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'url',
            'pk',
            'name',
            'group_tasks',
            'members',
        )

class MyGroupSerializer(serializers.HyperlinkedModelSerializer):
    my_groups = GroupSummarySerializer()
    
    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'my_groups',
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
