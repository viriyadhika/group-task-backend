from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User

from grouptasks.serializers import UserSerializer, GroupSerializer
from grouptasks.models import Group, Task

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user_list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user_detail'

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    name = 'group_list'

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    name = 'group_detail'

# Create your views here.
