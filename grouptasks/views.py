from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User

from grouptasks.serializers import (
    UserSerializer, 
    GroupSerializer,
    TaskSerializer,
)
from grouptasks.models import Group, Task
from grouptasks.custompermissions import IsInTaskGroup, IsGroupMember

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'users' : reverse(UserList.name, request=request),
            'groups' : reverse(GroupList.name, request=request),
        })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    name = 'group-list'

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    name = 'group-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        IsGroupMember,
    )

class TaskCreate(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-create'

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    name = 'task-detail'
    permission_classes = (
        IsInTaskGroup,
    )

# Create your views here.
