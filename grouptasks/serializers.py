from django.contrib.auth.models import User
from rest_framework import serializers

from grouptasks.models import Group, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
        )

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = Group
        fields = (
            'url',
            'name',
            'members',
        )
